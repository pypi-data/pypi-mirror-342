* 文档首页
/ByteHouse云数仓版/用户指南/数据建模/表引擎/唯一键表

ByteHouse云数仓版的CnchMergeTree表引擎支持在建表时设置唯一键（UNIQUE KEY），创建一个唯一键表，本文为您介绍唯一键表的能力细节和使用示例。

能力概述

唯一键表即指定唯一键（UNIQUE KEY）的 CnchMergeTree 表，具有以下特点：

* 用户通过 UNIQUE KEY 配置唯一键，支持 upsert 更新写语义，查询时自动返回每个唯一键的最新值。
* 在保证实时更新能力的情况下，依然保持较高的查询性能。
* 唯一键（UNIQUE KEY）支持多字段和表达式。
* 唯一键表支持多种去重粒度（如分区级去重、bucket 去重等）。
* 支持自定义版本字段，写入低版本数据时自动忽略。
* 支持根据 UNIQUE KEY 实时删除数据。
* 支持根据 UNIQUE KEY 进行部分列更新操作。

## 唯一键表与非唯一键表能力对比

| 对比项 | 唯一键表 | 非唯一键表 |
| --- | --- | --- |
| 唯一键约束 | 保证 | 不保证 |
| [更新语句 (UPDATE)](/docs/6517/1359471) | 支持 | 不支持同步更新 可以通过 alter 语句实现异步更新 |
| [删除语句 (DELETE)](/docs/6517/1359473) | 支持 | 不支持同步删除 可以通过 alter 语句实现异步删除 |
| [部分列更新](/docs/6517/1331034) | 支持 | 不支持 |
| UPSERT / [INSERT THROW](/docs/6517/1359469#16a2fc23)/ [INSERT IGNORE](/docs/6517/1359469#2c3c55f2) | 支持  说明  当使用唯一键表进行 insert 时，默认会实现 upsert 语义，即保留每个唯一键的最新值。 | 不支持 |

## 唯一键支持的类型

| 常用 Unique Key 字段类型 | 其他 Unique key 的字段类型 |
| --- | --- |
| String, UInt8, UInt16, UInt32, UInt64, Int8, Int16, Int32, Int64 | Decimal32, Decimal64, Date, Date32, DateTime, DateTime64, Time |

如果希望使用不支持的字段类型用作 Unique key 字段，可以尝试使用 `sipHash64()` 将对应字段类型转化为 UInt64。

说明

`sipHash64` 是一种快速且低冲突率的哈希函数，实践中未遇到 hash 冲突的场景。

去重粒度：分区级唯一&Bucket唯一

Bytehouse 唯一键表默认提供分区级唯一作为去重粒度，当 cluster by 所需列为 unique key 字段所需列子集时，去重粒度可以优化到 bucket 唯一。不同的去重粒度能够在元数据级别限制待去重的数据量，进而满足用户不同的写入诉求：

注意

唯一键表在写入时，需要通过唯一键，找到每条记录原来所在的位置，因此待去重的存量数据行数越多，写入 rps 越低；通常，在存量数据为 50,000,000 时，写入 rps 为 20,000。

| 对比项 | 分区级唯一+非bucket去重优化 | 分区级唯一+bucket去重优化 |
| --- | --- | --- |
| 去重说明 | 分区级别去重，新写入的数据会跟对应分区中所有的存量数据进行去重。 | 分区级别的 bucket 去重，新写入的数据会跟表中对应分区，相同 bucket 的存量数据去重。 |
| 去重存量数据示例 | Image   * 去重粒度为分区级 * 新写入数据的 partition = 2020-10-29 | Image**cluster by 所需列为 unique key 字段所需列的子集** 图例中：   * 去重粒度为Bucket级 * Bucket 数量为 5 * 新写入数据的 partition = 2020-10-29 * 新写入数据的 bucket = 0 |

数据删除/更新原理

唯一键表使用了 Delete-and-Insert 策略，当更新数据到来时，通过唯一键，先找到每条记录原来所在的位置，将该条记录标记为删除，然后将最新的数据作为新记录写入到新的数据文件中。读取时，根据删除标记，将已删除的旧版本数据过滤掉，从而查询到唯一键的最新值。

例如，以下示例中表为分区级唯一，PK 为 partition key，UK 为 unique key，delete bitmap 为标记删除列。
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/68f983433f944d84b3e1c4bc4aab0054~tplv-goo7wpa0wc-image.image)

Delete bitmap 列为 1 的数据被标记删除，在增量数据写入后，最新数据为：

```
2020-10-29，1，m
2020-10-29，2，n
2020-10-30，1，z
2020-10-30，2，k

```
使用限制

唯一键表由于去重特性，为了进行高效的数据写入，对于数据量和 Unique Key 数量具有如下使用限制：

* 建议 Unique Key 字段设置不超过 5 个；如果多个字段组合构成唯一键，可以使用它们的 sipHash64 哈希作为唯一键。
* 建议去重粒度的数据量控制在 1 亿以下。

使用示例

以下为您提供两个典型使用示例，更多示例可参见[ByteHouse Unique 表最佳实践](/docs/6517/145505)。

## 分区级唯一示例

```
CREATE TABLE t1
(
  `event_time` DateTime,
  `product_id` UInt64,
  `city` String,
  `category` String,
  `amount` UInt32,
  `revenue` UInt64
)
ENGINE = CnchMergeTree
PARTITION BY toDate(event_time)
ORDER BY (city, category)
UNIQUE KEY product_id;

INSERT INTO t1 VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200),
('2020-10-29 23:40:00', 10003, 'Beijing', '男装', 1, 100);

-- 写入相同 key 的数据可以实现更新(upsert语义)
INSERT INTO t1 VALUES
('2020-10-29 23:50:00', 10002, 'Beijing', '男装', 4, 400),
('2020-10-29 23:50:00', 10003, 'Beijing', '男装', 2, 200),
('2020-10-29 23:50:00', 10004, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10001, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10002, 'Beijing', '男装', 2, 200);

-- 查询自动返回每个key最新的数据
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
## 分区级唯一+bucket 唯一示例

当唯一键表单分区数据量达到一定量级，会影响写入效率。此时可以使用 cluster by 将分区级的数据量打散到不同的分桶，当 cluster by 所需的列全部包含在 unique key 中时，可以达到分区级唯一的效果，同时享受 bucket 唯一优化。

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
ENGINE = CnchMergeTree
PARTITION BY toDate(event_time)
ORDER BY (city, category)
CLUSTER BY product_id INTO 10 BUCKETS
UNIQUE KEY product_id;

INSERT INTO t2 VALUES
('2020-10-29 23:40:00', 10001, 'Beijing', '男装', 5, 500),
('2020-10-29 23:40:00', 10002, 'Beijing', '男装', 2, 200),
('2020-10-29 23:40:00', 10003, 'Beijing', '男装', 1, 100);

-- 写入相同 key 的数据可以实现更新(upsert语义)
INSERT INTO t2 VALUES
('2020-10-29 23:50:00', 10002, 'Beijing', '男装', 4, 400),
('2020-10-29 23:50:00', 10003, 'Beijing', '男装', 2, 200),
('2020-10-29 23:50:00', 10004, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10001, 'Beijing', '男装', 1, 100),
('2020-10-30 00:00:05', 10002, 'Beijing', '男装', 2, 200);

-- 查询自动返回每个key最新的数据
select * from t2 order by toDate(event_time), product_id;
┌──────────event_time─┬─product_id─┬─city────┬─category─┬─amount─┬─revenue─┐
│ 2020-10-29 23:40:00 │      10001 │ Beijing │ 男装     │      5 │     500 │
│ 2020-10-29 23:50:00 │      10002 │ Beijing │ 男装     │      4 │     400 │
│ 2020-10-29 23:50:00 │      10003 │ Beijing │ 男装     │      2 │     200 │
│ 2020-10-29 23:50:00 │      10004 │ Beijing │ 男装     │      1 │     100 │
│ 2020-10-30 00:00:05 │      10001 │ Beijing │ 男装     │      1 │     100 │
│ 2020-10-30 00:00:05 │      10002 │ Beijing │ 男装     │      2 │     200 │
└─────────────────────┴────────────┴─────────┴──────────┴────────┴─────────┘

```
