唯一键引擎（HaUniqueMergeTree） 是 ByteHouse 自研的一款既保留了 ClickHouse 高效的查询性能、又支持主键更新的表引擎。它解决了社区版 ClickHouse 不能支持高效更新操作的痛点，帮助业务更简单地开发实时分析应用。

引擎优势

1. 用户通过 UNIQUE KEY 配置唯一键，提供 upsert 更新写语义，查询自动返回每个唯一键的最新值。（和社区的 ReplacingMergeTree 相比，ReplacingMergeTree 在数据导入后需要等待 Merge 完成，才可以查到去重后的数据，而 HaUniqueMergeTree 则是即导入后立即去重）。
2. 性能：单 Shard 写入吞吐一般可以达到 50k + rows/s。对于海量数据的场景，建议通过数据源治理后，并行导入不同分区来实现线性增速。
3. 唯一键支持多字段和表达式。
4. 支持分区级别唯一和表级别唯一两种模式。
5. 支持自定义版本字段，写入低版本数据时自动忽略。
6. 多副本部署，通过主备异步复制保障数据可靠性。
7. 支持根据UNIQUE KEY实时删除数据。

建表示例
## SQL 建表

### 建表语法

```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1] [TTL expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2] [TTL expr2],
    ...
) ENGINE = HaUniqueMergeTree(shard, replica, version_column) -- 默认为 '/clickhouse/bytehouse/库名.表名/{shard}','{replica}'
PARTITION BY toYYYYMM(EventDate)
ORDER BY expr
[PARTITION BY expr]
UNIQUE KEY expr
[SAMPLE BY expr]
[TTL expr
    [DELETE|TO DISK 'xxx'|TO VOLUME 'xxx' [, ...] ]
    [WHERE conditions]
    [GROUP BY key_expr [SET v1 = aggr_func(v1) [, v2 = aggr_func(v2) ...]] ] ]
[SETTINGS name=value, ...]

```

* Unique Key设置：支持多个字段（但不支持 Nullable，也不支持 Map，Array 等复合类型），也支持表达式，例如：`UNIQUE KEY (product_id, sipHash64(city))`

注意

建议 Unique key 设置不超过5个，以避免可能产生的性能影响：

1. 在使用 memory index 的场景下，会占用大量内存；
2. 会延长存储数据对象的序列化和反序列化时间。

* version\_column（版本字段）: 选择一个字段作为版本控制的依据，用于根据版本更新，使用示例可查看例2。在设计表结构时，建议优先考虑分区值作为版本，减少内存占用。

其他的字段设置，如 `Order By`，`Partition By`等，和 MergeTree 家族的其他引擎的设置规则一致。

### Settings 设置项

| **参数名** | 常用字段 | **默认值** | **说明** |
| --- | --- | --- | --- |
| partition\_level\_unique\_keys | 是 | 1 | 0：UNIQUE KEY 表粒度唯一 1：UNIQUE KEY 分区粒度唯一 推荐选择：优选分区粒度唯一（即默认值）。如果业务语义必须使用表粒度唯一，考虑设置更短的 TTL、采用更粗粒度的分区（例如按月分区）等方式减少分区数量。 |
| enable\_unique\_partial\_update | 是 | 0 | 允许部分列更新写入（需要新引擎版本支持） |
| enable\_disk\_based\_unique\_key\_index | 是 | 1 | 0：in-memory mode。在此方式下，系统会在每张unique表维护一个in-memory key index，因此能支撑的数据量受限于内存 ； 1：disk-based mode。在此方式下，不限制数据量，但是性能比 in-memory 方式低 10-30%（插入数据越频繁，导入速度损失越大） 推荐选择：建议 整体数据量 < 1亿条\*集群 Shard 数时，选择 in-memory 模式，此外都选择 disk-based 模式。 |

使用示例
## 例1：分区级别唯一键

假设表Schema如下：

```
-- 引擎默认保证 unique key 在分区内的唯一性
-- 注：UNIQUE KEY 不支持 Nullable
CREATE TABLE t1
(
  `event_time` DateTime,
  `product_id` UInt64,
  `city` String,
  `category` String,
  `amount` UInt32,
  `revenue` UInt64
)
ENGINE = HaUniqueMergeTree('/clickhouse/default/t1/{shard}', '{replica}')
PARTITION BY toDate(event_time)
ORDER BY (city, category)
UNIQUE KEY product_id;

```

插入数据。此时，写入相同 key 的数据可以实现更新(upsert语义)。

```
INSERT INTO t1 VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200),
('2020-10-29 23:40:00', 10003, 'Beijing', '男装', 1, 100);

INSERT INTO t1 VALUES
('2020-10-29 23:50:00', 10002, 'Beijing', '男装', 4, 400),
('2020-10-29 23:50:00', 10003, 'Beijing', '男装', 2, 200),
('2020-10-29 23:50:00', 10004, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10001, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10002, 'Beijing', '男装', 2, 200);

```

查询自动返回每个key最新的数据：

```
select * from t1 order by toDate(event_time), product_id;
┌──────────event_time─┬─product_id─┬─city────┬─category─┬─amount─┬─revenue─┐
│ 2020-10-29 23:40:00 │      10001 │ Beijing │ 男装     │      5 │     500 │
│ 2020-10-29 23:50:00 │      10002 │ Beijing │ 男装     │      4 │     400 │
│ 2020-10-29 23:50:00 │      10003 │ Beijing │ 男装     │      2 │     200 │
│ 2020-10-29 23:50:00 │      10004 │ Beijing │ 男装     │      1 │     100 │
│ 2020-10-30 00:00:05 │      10001 │ Beijing │ 男装     │      1 │     100 │
│ 2020-10-30 00:00:05 │      10002 │ Beijing │ 男装     │      2 │     200 │
└─────────────────────┴────────────┴─────────┴──────────┴────────┴─────────┘

```

UNIQUE KEY 也可以包含多个字段和表达式，如下面以两个字段：product\_id, sipHash64(city)为例：

```
-- UNIQUE KEY 可以包含多个字段和表达式
CREATE TABLE t1m
(
  `event_time` DateTime,
  `product_id` UInt64,
  `city` String,
  `category` String,
  `amount` UInt32,
  `revenue` UInt64
)
ENGINE = HaUniqueMergeTree('/clickhouse/default/t1m/{shard}', '{replica}')
PARTITION BY toDate(event_time)
ORDER BY (city, category)
UNIQUE KEY (product_id, sipHash64(city));

INSERT INTO t1m VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200),
('2020-10-29 23:40:00', 10003, 'Beijing', '男装', 1, 100),
('2020-10-29 23:50:00', 10002, 'Shanghai', '男装', 4, 400),
('2020-10-29 23:50:00', 10003, 'Beijing', '男装', 2, 200),
('2020-10-29 23:50:00', 10004, 'Beijing', '男装', 1, 100);

select * from t1m;
┌──────────event_time─┬─product_id─┬─city─────┬─category─┬─amount─┬─revenue─┐
│ 2020-10-29 23:40:00 │      10001 │ Beijing  │ 男装     │      5 │     500 │
│ 2020-10-29 23:40:00 │      10002 │ Beijing  │ 男装     │      2 │     200 │
│ 2020-10-29 23:50:00 │      10003 │ Beijing  │ 男装     │      2 │     200 │
│ 2020-10-29 23:50:00 │      10004 │ Beijing  │ 男装     │      1 │     100 │
│ 2020-10-29 23:50:00 │      10002 │ Shanghai │ 男装     │      4 │     400 │
└─────────────────────┴────────────┴──────────┴──────────┴────────┴─────────┘

```
## 例2：表级别唯一键

假设表Schema如下：

```
CREATE TABLE t2
(
  `event_time` DateTime,
  `product_id` UInt64,
  `city` String,
  `category` String,
  `amount` UInt32,
  `revenue` UInt64
)
ENGINE = HaUniqueMergeTree('xxxxxxx')
PARTITION BY toDate(event_time) --分区字段
ORDER BY (city, category) --排序字段
UNIQUE KEY product_id --唯一键
SETTINGS partition_level_unique_keys = 0; --设置表级别唯一

```

顺序插入以下测试数据：

```
INSERT INTO t2 (event_time, product_id, city, category, amount, revenue) VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200),
('2020-10-29 23:40:00', 10003, 'Beijing', '男装', 1, 100);

INSERT INTO t2 (event_time, product_id, city, category, amount, revenue) VALUES
('2020-10-29 23:50:00', 10002, 'Beijing', '男装', 4, 400),
('2020-10-29 23:50:00', 10003, 'Beijing', '男装', 2, 200),
('2020-10-29 23:50:00', 10004, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10001, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10002, 'Beijing', '男装', 2, 200);

```

可以看到，10001，10002，10003 这三个产品都更新到了最新数据，且10001，10002 都从 2020-10-29 分区更新到了 2020-10-30 分区。

```
select * from t2 order by toDate(event_time), product_id;
┌──────event_time─┬product_id─┬─city──┬category─┬amount─┬revenue─┐
│ 2020-10-29 23:50:00 │      10003 │ Beijing │ 男装     │      2 │     200 │
│ 2020-10-29 23:50:00 │      10004 │ Beijing │ 男装     │      1 │     100 │
│ 2020-10-30 00:00:05 │      10001 │ Beijing │ 男装     │      1 │     100 │
│ 2020-10-30 00:00:05 │      10002 │ Beijing │ 男装     │      2 │     200 │
└─────────────┴───────┴─────┴──────┴─────┴─────┘

```
## 例3：自定义版本字段使用

默认情况下，相同 unique key 后写入的数据会覆盖已有的数据。这可能会带来以下问题

* 回溯上游数据时，老数据可能覆盖新数据，导致查询到的数据结果出现回退
* Lambda 架构下，如果离线和实时任务同时写一个分区，最终保留哪条数据取决于任务的执行顺序

为了解决上面的问题，HaUniqueMergeTree 支持将表中的某个字段指定为版本字段。引擎保证写入相同 key 的数据时，只有数据版本 >= 已有版本时，才会进行覆盖。版本字段支持所有UInt类型和Data/DateTime，且不能为 Nullable。

说明

使用版本字段时有以下限制：

* 如需要使用整数作为版本字段，建议使用兼容UInt64的无符号整数
* 支持Date、Datetime时间类型作为版本字段
* 不支持float、Decimal、DateTime64等浮点数类型作为版本字段

假设schema如下：

```
CREATE TABLE t3
(
  `event_time` DateTime,
  `product_id` UInt64,
  `city` String,
  `category` String,
  `amount` UInt32,
  `revenue` UInt64
)
ENGINE = HaUniqueMergeTree('/clickhouse/default/t3/{shard}', '{replica}', event_time) --event_time为版本字段
PARTITION BY toDate(event_time) --分区字段
ORDER BY (city, category) --排序字段
UNIQUE KEY product_id; --唯一键

```

顺序插入以下数据：

```
INSERT INTO t3 (event_time, product_id, city, category, amount, revenue) VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200),
('2020-10-29 23:50:00', 10001, 'Beijing', '男装', 8, 800),
('2020-10-29 23:50:00', 10002, 'Beijing', '男装', 5, 500);

```

结果保留后两条。

```
select * from t3 order by toDate(event_time), product_id;
┌──────event_time─┬product_id─┬─city──┬category─┬amount─┬revenue─┐
│ 2020-10-29 23:50:00 │      10001 │ Beijing │ 男装     │      8 │     800 │
│ 2020-10-29 23:50:00 │      10002 │ Beijing │ 男装     │      5 │     500 │
└─────────────┴───────┴─────┴──────┴─────┴─────┘

```

若在此时重新导入回溯前两条数据。

```
INSERT INTO t3 (event_time, product_id, city, category, amount, revenue) VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200);

```

由于版本 < 已有版本，写入时自动跳过。10001 和 10002 的版本没有回退。

```
select * from t3 order by toDate(event_time), product_id;
┌──────────event_time─┬─product_id─┬─city────┬─category─┬─amount─┬─revenue─┐
│ 2020-10-29 23:50:00 │      10001 │ Beijing │ 男装     │      8 │     800 │
│ 2020-10-29 23:50:00 │      10002 │ Beijing │ 男装     │      5 │     500 │
└─────────────────────┴────────────┴─────────┴──────────┴────────┴─────────┘

```
## 例4：使用分区值作为版本

考虑以下Lambda架构的需求场景：

* 表按天分区，需要基于某个字段实现表粒度去重
* 实时任务写T+0分区，可能将一些数据从 T+N 分区更新到 T+0 分区
* 离线任务每天重写 T+1 分区
* 每个 key 的最新数据需要从其所在的最新分区读取

我们可以将分区字段（日期）作为版本字段来实现该场景，然而这需要额外存储一个日期字段。由于分区下所有数据的日期都是一样的，这样做显然存在资源浪费。

为了优化该场景，HaUniqueMergeTree 支持直接使用分区表达式作为版本。当引擎发现版本字段为分区字段时，会自动从元数据中读取版本，避免额外的数据读写。

```
-- 创建一张按天分区、表粒度唯一的 unique 表，使用分区字段作为版本
CREATE TABLE t4
(
  `event_time` DateTime,
  `product_id` UInt64,
  `city` String,
  `category` String,
  `amount` UInt32,
  `revenue` UInt64
)
ENGINE = HaUniqueMergeTree('/clickhouse/default/t4/{shard}', '{replica}', toDate(event_time))
PARTITION BY toDate(event_time)
ORDER BY (city, category)
UNIQUE KEY product_id
SETTINGS partition_level_unique_keys = 0;

-- 10-29 实时任务数据写入
INSERT INTO t4 VALUES
('2020-10-29 10:00:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 10:00:00', 10002, 'Beijing', '男装', 2, 200),
('2020-10-29 10:10:00', 10001, 'Beijing', '男装', 8, 800),
('2020-10-29 10:10:00', 10002, 'Beijing', '男装', 5, 500);
-- 10-30 实时任务数据写入，将 10002 更新到 10-30 分区
INSERT INTO t4 VALUES
('2020-10-30 08:00:00', 10002, 'Beijing', '男装', 10, 1000),
('2020-10-30 08:00:00', 10003, 'Beijing', '男装', 3, 300);
-- 10-30 离线任务重写 10-29 数据
INSERT INTO t4 VALUES
('2020-10-29 10:10:00', 10001, 'Beijing', '男装', 7, 700),
('2020-10-29 10:10:00', 10002, 'Beijing', '男装', 5, 500);
-- 离线任务只会覆盖 10001 数据，10002 保留 10-30 中的最新数据
select * from t4 order by toDate(event_time), product_id;
┌──────────event_time─┬─product_id─┬─city────┬─category─┬─amount─┬─revenue─┐
│ 2020-10-29 10:10:00 │      10001 │ Beijing │ 男装     │      7 │     700 │
│ 2020-10-30 08:00:00 │      10002 │ Beijing │ 男装     │     10 │    1000 │
│ 2020-10-30 08:00:00 │      10003 │ Beijing │ 男装     │      3 │     300 │
└─────────────────────┴────────────┴─────────┴──────────┴────────┴─────────┘

```
## 例5：删除字段使用

在某些应用场景下，用户希望在INSERT时加上一个字段来标识是否删除来扩展INSERT语义。

在HaUniqueMergeTree引擎中，为每张表都添加了一个保留字段`_delete_flag_`，可在 INSERT / INSERT SELECT 时指定，其类型为`UInt8`， 0 表示数据写入，非 0 表示数据删除。

需要注意的是，`_delete_flag_`字段仅可在 INSERT / INSERT SELECT 或者创建物化视图时指定，不可以在 CREATE TABLE 时指定，也不可查询该字段。

说明

删除行功能可以在对底表为HaUniqueMergeTree的分布式表进行操作，前提是分布式表需要配置参数**remote\_table\_is\_ha\_unique = 1。**

用法示例如下：

假设schema如下：

```
CREATE TABLE t1
(
  `event_time` DateTime,
  `product_id` UInt64,
  `city` String,
  `category` String,
  `amount` UInt32,
  `revenue` UInt64,
)
ENGINE = HaUniqueMergeTree(xxxx)
PARTITION BY toDate(event_time)
ORDER BY (city, category)
UNIQUE KEY product_id; --唯一键

```

导入以下数据：

> 注：需要选择单个节点，并插入本地表来使用 delete flag 做数据删除

```
INSERT INTO t1_local (event_time, product_id, city, category, amount, revenue, _delete_flag_) VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500, 0),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200, 0),
('2020-10-29 23:40:00', 10003, 'Beijing', '男装', 1, 100, 0),
('2020-10-29 23:50:00', 10001, 'Beijing', '男装', 4, 400, 5),
('2020-10-29 23:50:00', 10002, 'Beijing', '男装', 2, 200, 1),
('2020-10-29 23:50:00', 10004, 'Beijing', '男装', 1, 100, 0);

```

查询结果中包含了新加入的一行数据，并删除了两行旧数据:

```
select * from t1 order by toDate(event_time), product_id;
┌──────event_time─┬─product_id┬─city──┬─category┬amount─┬revenue─┐
│ 2020-10-29 23:40:00 │      10003 │ Beijing │ 男装     │      1 │     100 │
│ 2020-10-29 23:50:00 │      10004 │ Beijing │ 男装     │      1 │     100 │
└─────────────┴───────┴─────┴──────┴─────┴─────┘

```

针对某个 where 条件对多行数据进行批量删除的方式如下：

```
insert into `t1_local` (*, _delete_flag_) select *, 1 as _delete_flag_ from `t1_local` where product_id=10001;

```
## 例6：部分列更新

**使用条件：**

1. **当前仅支持部分列更新功能。**
2. **不支持表级唯一**的部分列更新，仅支持分区级唯一的部分列更新。
3. 如果是用Kafka导入数据，需要对Unique表打开开关 **enable\_unique\_partial\_update = 1。**
4. 可以对底表为HaUniqueMergeTree的分布式表进行操作，前提是分布式表需要配置参数**remote\_table\_is\_ha\_unique = 1。**

**行更新模式：缺省列采用默认值填充**
**部分列更新模式：缺省列如果有原值则保留，否则填充默认值**

1. unique表指定变量**enable\_unique\_partial\_update = 1**后允许写入以部分列更新模式进行，默认关闭。
2. 部分列写入模式当且仅当unique表开启了部分列更新功能才有效，否则等效为行更新模式：

   1. 对于交互式写入，Unique表默认为部分列更新模式，指定会话变量**enable\_unique\_partial\_update** = 0后切换到行更新模式。即参数**enable\_unique\_partial\_update**默认值为1。
   2. 对于Kafka实时写入，kafka表新增**enable\_unique\_partial\_update**参数(默认值为1)，1表示kafka消费使用部分列更新模式，0表示使用行更新模式。
3. 类型的默认值

   1. 数值类型：0
   2. 字符串类型：''
   3. Nullable类型：null
   4. Map类型(更新规则比较特殊，详见下方 **5.列更新规则-Map类型**)：{}
   5. Array类型：[]
4. 部分列更新写入模式时如果表包含版本字段

   1. 写入版本<当前版本，忽略写入行
   2. 写入版本>=当前版本，应用列更新规则
   3. 写入未指定版本时，版本字段取默认值
5. 列更新规则

   1. 方式一：按功能列\_update\_columns\_(String类型)区分更新列方案的列更新规则

      1. \_update\_columns\_中的内容是需要更新的列，以**逗号分隔各列名**，引擎在解析时**不会处理列名前后的特殊字符**，如空格、Tab、换行符等，且**不支持正则表达式**。
      2. **当\_update\_columns\_为空时表示更新所有列**
      3. 非Map类型：写入非默认值表示更新，不允许更新为默认值
      4. Map类型：**partial\_update\_enable\_merge\_map = true**时对有旧值的key进行更新，对无旧值的key进行写入；为false时直接替换value
      ```
      CREATE TABLE t1 (
        k Int32,
        c1 Int32,
        c2 Nullable(Float64),
        c3 Nullable(String),
        c4 Nullable(Int64),
        m1 Map(String, Int32),
        a1 Array(String))
      ENGINE = HaUniqueMergeTree('/clickhouse/default/t1/{shard}', '{replica}')
      UNIQUE KEY k ORDER BY k SETTINGS enable_unique_partial_update = 1,
      partial_update_enable_specify_update_columns = 1,
      partial_update_enable_merge_map = 0;

      SET enable_unique_partial_update = 1;

      INSERT INTO t1 (k, c1, c2, m1, a1) VALUES (1, 10, 3.14, {'k1':1}, ['hello']);
      -- 此时解析时会填充_update_columns_为'k,c1,c2,m1,a1'
      ┌─k─┬─c1─┬───c2─┬─c3───┬───c4─┬─m1───────┬─a1────────┐
      │ 1 │ 10 │ 3.14 │ ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ │ {'k1':1} │ ['hello'] │
      └───┴────┴──────┴──────┴──────┴──────────┴───────────┘

      INSERT INTO t1 (k, c1, c2, m1, a1, _update_columns_) VALUES (1, 20, 31.4, {'k2':2}, ['world'], 'k,c1,m1,a1');
      ┌─k─┬─c1─┬───c2─┬─c3───┬───c4─┬─m1───────┬─a1────────┐
      │ 1 │ 20 │ 3.14 │ ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ │ {'k2':2} │ ['world'] │
      └───┴────┴──────┴──────┴──────┴──────────┴───────────┘

      INSERT INTO t1 (k, c1, c3, m1) VALUES (1, 0, 'foo', {'k3':3});
      -- 此时解析是会填充_update_columns_为'k,c1,c3,m1'
      -- 等价于INSERT INTO t1 (k, c1, c3, m1, _update_columns_) VALUES (1, 0, 'foo', {'k2':2}, 'k, c1, c3, m1');
      -- 此时c1会强制更新为0，c3强制更新为'foo'，m1强制更新为'k3':3
      ┌─k─┬─c1─┬───c2─┬─c3──┬───c4─┬─m1───────┬─a1────────┐
      │ 1 │  0 │ 3.14 │ foo │ ᴺᵁᴸᴸ │ {'k3':3} │ ['world'] │
      └───┴────┴──────┴─────┴──────┴──────────┴───────────┘

      INSERT INTO t1 (k, c1, c2, c3, c4, m1, a1, _update_columns_) VALUES (1, 10, 31.4, 'goo', 15, {'k4': 4}, ['hello', 'world'], '');
      -- _update_columns_为空时表示更新所有列
      ┌─k─┬─c1─┬───c2─┬─c3──┬─c4─┬─m1───────┬─a1────────────────┐
      │ 1 │ 10 │ 31.4 │ goo │ 15 │ {'k4':4} │ ['hello','world'] │
      └───┴────┴──────┴─────┴────┴──────────┴───────────────────┘

      ```
   2. 方式二：按类型默认值区分更新列方案的列更新规则

      1. 非Map类型：写入非默认值表示更新，不允许更新为默认值
      2. Map类型：**partial\_update\_enable\_merge\_map = true**时对有旧值的key进行更新，对无旧值的key进行写入；为false时直接替换value
   ```
   CREATE TABLE t1 (
     k Int32,
     c1 Int32,
     c2 Nullable(Float64),
     c3 Nullable(String),
     c4 Nullable(Int64),
     m1 Map(String, Int32),
     a1 Array(String))
   ENGINE = HaUniqueMergeTree('/clickhouse/default/t1/{shard}', '{replica}')
   UNIQUE KEY k ORDER BY k SETTINGS enable_unique_partial_update = 1,
   partial_update_enable_specify_update_columns = 0,
   partial_update_enable_merge_map = 1;

   SET enable_unique_partial_update = 1;

   INSERT INTO t1 (k, c1, c2, m1, a1) VALUES (1, 10, 3.14, {'k1':1}, ['hello']);
   ┌─k─┬─c1─┬───c2─┬─c3───┬───c4─┬─m1───────┬─a1────────┐
   │ 1 │ 10 │ 3.14 │ ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ │ {'k1':1} │ ['hello'] │
   └───┴────┴──────┴──────┴──────┴──────────┴───────────┘

   INSERT INTO t1 (k, c1, c3, m1) VALUES (1, 0, 'foo', {'k2':2});
   -- 对于未指定字段
   -- - c1为非组合类型，但写入的是默认值，因此保留旧值
   -- - c2/c4为Nullable类型，保留旧值
   -- - a1为Array空值，保留旧值
   -- 对于m1，更新m1{'k2'}，保留m1{'k1'}
   ┌─k─┬─c1─┬───c2─┬─c3──┬───c4─┬─m1──────────────┬─a1────────┐
   │ 1 │ 10 │ 3.14 │ foo │ ᴺᵁᴸᴸ │ {'k1':1,'k2':2} │ ['hello'] │
   └───┴────┴──────┴─────┴──────┴─────────────────┴───────────┘

   INSERT INTO t1 (k, c1, c2, c3, c4, m1, a1) VALUES (1, 20, null, 'bar', 30, {'k2':0, 'k3':3}, ['world']);
   -- c1不是默认值，更新
   -- c2为null，保留旧值；c3/c4不为null，更新
   -- 更新m1{'k2'}, m1{'k3'}，保留m1{'k1'}
   -- a1不为空值，更新
   ┌─k─┬─c1─┬───c2─┬─c3──┬─c4─┬─m1─────────────────────┬─a1────────┐
   │ 1 │ 20 │ 3.14 │ bar │ 30 │ {'k1':1,'k2':0,'k3':3} │ ['world'] │
   └        ───┴────┴──────┴─────┴────┴────────────────────────┴───────────┘

   ```

   【注意】使用这种方式在建表时 **慎用默认值！**

   在建表时可以在字段后指定默认值，默认值可以为表达式。如果用户指定了默认值，那么写入时对于缺省的列会按照建表时指定的方式进行填充，而部分列更新判断是否为默认值时是按照引擎内数据类型的默认值进行判断，因此可能会产生不符合预期的行为。下面将举个例子进行说明

   ```
   CREATE TABLE t1 (
     k Int32,
     c1 Int32 DEFAULT k + 1,
     c2 Nullable(Float64))
   ENGINE = HaUniqueMergeTree('/clickhouse/default/t1/{shard}', '{replica}')
   UNIQUE KEY k ORDER BY k SETTINGS enable_unique_partial_update = 1,
   partial_update_enable_specify_update_columns = 0;

   insert into t1 values (1, 10, 3.14);
   ┌─k─┬─c1─┬───c2─┐
   │ 1 │ 10 │ 3.14 │
   └───┴────┴──────┘

   insert into t1 (k, c2) values (1, 31.4);
   ┌─k─┬─c1─┬───c2─┐
   │ 1 │  2 │ 31.4 │
   └───┴────┴──────┘
   -- 如果在建表时没有指定从c1的默认值，那么这条写入的语义是将k=1的那条数据的c2被更新为31.4，但是由于建表指定了默认值，等价于insert into t1 values (1, 2，31.4)，因此c1也被更新为了2。这种情况下为了达到仅更新c2的目的，可以有以下两种方式：1. 建表时不要使用默认值；2. 显示指定默认值，即insert into t1 values (1, 0，31.4)
   -- ┌─k─┬─c1─┬───c2─┐
   -- │ 1 │ 10 │ 31.4 │
   -- └───┴────┴──────┘

   ```

性能

在使用 in-memory 模式下，HaUniqueMergeTree 的导入性能约是 HaMergeTree 或 社区的 MergeTree 引擎的一半，为 10k rows/s/shard，或 20 MB/s。性能相比社区的 ReplacingMergeTree 也接近一致。

但查询性能上，HaUniqueMergeTree 的性能和 HaMergeTree 或 MergeTree 引擎一致。

在使用 disk-based 模式下，HaUniqueMergeTree 的导入性能约是 HaMergeTree 或 社区的 MergeTree 引擎的 30-40%，为 6-8k rows/s/shard，或 12-16 MB/s。查询性能依旧不变。

引擎限制

* 在 Kafka 导入时，用户需要保证相同唯一键的数据写入同一个的 Topic Partition，并禁用 Topic 扩容；
* 唯一键所在的集群暂不支持扩容；
* 内存索引模式下，内存使用与唯一键大小及基数成正比，不适合单节点数据量超过 1 亿的表，如果使用不当会导致节点OOM；需要启用磁盘索引模式。

最佳使用实践
## 建表参数推荐

### In-memory 与 Disk-based 选择

目前unique 表有两种key index使用方式：in-memory 和 disk-based。由表级参数`enable_disk_based_unique_key_index`控制。

* Disk-based 的使用方式不限制全表数据量，但是性能比 in-memory 模式的导入地低 40%。约为 6 MB/s Shard。
* In-memory 性能更好，可达 10MB/s，但会限制数据量，建议如下：
  + 【表粒度唯一】时，所有分区的内存索引都需要常驻内存，因此不建议对单节点超过1亿条数据的表启用唯一键。如果集群有20个分片，那么最多支持20亿条数据。
  + 【分区粒度唯一】时，这种情况只有最近有数据写入的分区需要加载内存索引。因此如果业务只会更新最近 N 天的数据，那么只要单节点上 N 天的数据条数不超过1亿，就可以使用 in-memory 模式。

### 唯一键选择

如果包含很多字段，考虑使用哈希值。例：`UNIQUE KEY sipHash64(val1,val2,val3....)`

### 唯一键级别

优先使用默认的分区级别唯一。

如果业务场景必须使用表级别唯一，考虑设置 TTL、采用更粗粒度的分区（例如按月分区）等方式减少分区数量。

### 版本字段选择

如果需要指定版本字段，优先考虑分区值作为版本，减少内存占用。

## 表修改

1. Detach partition 和 Attach partiton 操作只能在 leader 节点执行；
2. 实时删除功能与唯一键级别、版本的作用规则：
   * 实时删除级别和唯一键级别 保持一致，即唯一键级别为分区时删除仅会删除对应分区的数据。
   * 当指定版本(非0)时，实时删除会遵循版本规则；当不指定版本或者指定版本为0时，实时. 删除不会遵循版本规则。
3. ByteHouse unique 表建立后，唯一键和唯一键列的类型均不可修改。

## Kafka 导入

Consumer 会直接写本地 shard。因此

* 业务需要保证**相同 unique key 的数据写入同一个 topic partition**
* 为了保证 key -> shard 的映射不变，**topic 需要设置固定大小的分区数，并禁用自动加减分区**
* 如果要同时通过批式和流式导入数据到同一张表，可以采用 批数据源 -> Kafka -> CH 的方式，保证离线数据的 sharding 方式与实时相同。