/ByteHouse云数仓版/用户指南/数据建模/表引擎/CnchMergeTree
## 表引擎介绍

表引擎即表的类型，决定了：

* 数据的组织和存储方式
* 索引的方式以及索引类型
* 支持哪些查询以及如何支持
* 一些其他特定的功能和配置

ByteHouse 云数仓版最常用的表引擎是 CnchMergeTree，除此之外也有其他特殊类型的表引擎包括 Hive外表、Kafka表等。本文重点分享 CnchMergeTree 表引擎的原理。

## CnchMergeTree 表引擎

CNCHMergeTree 是最常用的表引擎，核心思想和LSM-Tree类似，数据按分区键(partition by)进行分区，然后排序键(order by)进行有序存储。主要有如下特点：
**1. 逻辑分区**

如果指定了分区键的话，数据会按分区键划分成了不同的逻辑数据集（逻辑分区，Partition)。

每一个逻辑分区可以存在零到多个数据片段（DataPart）。如果查询条件可以裁剪分区，通常可以加速查询。如果没有指定分区键，全部数据都在一个逻辑分区里。
**2. 数据片段**

数据片段里的数据按排序键排序。每个数据片段还会存在一个min/max索引，来加速分区选择。
**3. 数据颗粒（Granule）**

每个数据片段被逻辑的分割成颗粒（granule），默认的Granule为8192行（由表的index\_granularity配置决定）。颗粒是 ByteHouse 中进行数据查询时的最小不可分割数据集。每个颗粒的第一行通过该行的主键值进行标记， ByteHouse 会为每个数据片段创建一个索引文件来存储这些标记。对于每列，无论它是否包含在主键当中，ByteHouse 都会存储类似标记。这些标记让您可以在列文件中直接找到数据。Granule作为ByteHouse 稀疏索引的索引目标，也是在内存中进行数据扫描的单位。
**4. 后台 Merge**

后台任务会定时对同一个分区的DataPart进行合并，并保持按排序键有序。后台的合并减少了 Part 的数目，以便更高效存储，并提升了查询性能。

## CnchMergeTree 建表语句和相关配置

CnchMergeTree 表引擎支持的建表语义如下：

```
CREATE TABLE [IF NOT EXISTS] [db.]table_name
(
    name1 [type1] [DEFAULT|ALIAS expr1] [compression_codec] [TTL expr1],
    name2 [type2] [DEFAULT|ALIAS expr2] [compression_codec] [TTL expr2],
    ...
    INDEX index_name1 expr1 TYPE type1(...) GRANULARITY value1,
    INDEX index_name2 expr2 TYPE type2(...) GRANULARITY value2，
) ENGINE = CnchMergeTree()
ORDER BY expr
[PARTITION BY expr]
[CLUSTER BY (column, expression, ...) INTO value1 BUCKETS SPLIT_NUMBER value2 WITH_RANGE]
[PRIMARY KEY expr]
[UNIQUE KEY expr]
[SAMPLE BY expr]
[TTL expr]
[SETTINGS name=value, ...]

```
## 配置参数说明

### 设计分区键（PARTITION BY)

分区键定义分区，分区是在一个表中通过指定的规则划分而成的逻辑数据集。可以按任意标准进行分区，如按日期。为了减少需要操作的数据，每个分区都是分开存储的。查询时，ByteHouse 尽量使用这些分区的最小子集。建表时候通过 `PARTITION BY expr` 子句指定。分区键可以是表中列的任意表达式。例如，指定按月分区，表达式为 `toYYYYMM(date)`；或者按表达元组，如`(toMonday(date), EventType)`等。

需要注意，表中分区表达式计算出的取值范围不能太大（推荐不超过一万），太多分区会占用比较大的内存以及带来比较多的 IO 和计算开销。

合理的设计分区键可以极大减少查询时需要扫描的数据量，一般考虑将查询中最常用的条件同时取值范围不超过一万的列设计为分区键（如日期等）

### 设计排序键（ORDER BY）

可以是一组列的元组或任意的表达式。 例如: `ORDER BY (OrderID, Date)`。

如果不需要排序，可以使用 `ORDER BY tuple()`，DataPart将按照数据插入的顺序存储。

### 主键(PRIMARY KEY)

默认情况不需要显式指定，ByteHouse 将使用排序键作为主键。当有特殊场景主键和排序键不一致时，主键必须为排序键的最左前缀。如排序键为(OrderID, Date)，主键必须为OrderID，不能为Date。

ByteHouse 会在主键上建立以 Granule 为单位的稀疏索引，（与之对比，所谓稠密索引则是每一行都会建立索引信息）。

如果查询条件能匹配主键索引的最左前缀，通过主键索引可以快速过滤出可能需要读取的数据颗粒，相比扫描整个 DataPart，通常要高效很多。
**另外需要注意，PRIMARY KEY不能保证唯一性，所以可以插入主键重复的数据行。**

分区（PARTITION BY）和主键(PRIMARY KEY)是两种不同的加速数据查询的方式，定义的时候应当尽量错开使用不同的列来定义两者，来覆盖更多的查询场景。例如order by的第一个列一定不要重复放到partition by里。下面是如何选择主键的一些考虑：

* 是否是查询条件里常用的列
* 不是非分区键的第一个列
* 这个列的选择性，例如性别、是/否这种可选值太少的列不建议放入主键中
* 假如现在的主键是（a，b)，如果在大多数情况下给定（a，b）对应的数据范围很大（包含多个Granule），可以考虑把一个新的查询常用列附加到主键中，这样可以过滤更多的数据。
* 过长的主键会对插入性能和内存消耗有负面影响，但对查询性能没有影响。

### 唯一键(UNIQUE KEY)

ByteHouse的主键（PRIMARY KEY）不能保证唯一性，如果有唯一键去重的需求，需要在建表时设置唯一键索引。设置唯一键之后，ByteHouse 提供 upsert 更新写语义，可以根据唯一键高效更新数据行，或者在upsert的时候通过设置虚拟列 `_delete_flag_=1` ，可以用来删除指定的 key。查询自动返回每个唯一键的最新值。

唯一键可以是一组列的元组或任意的表达式，如`UNIQUE KEY (product_id, sipHash64(city))`。

通过唯一键查询时会用上唯一键索引过滤数据加速查询，所以通常排序主键可以设置和唯一键不一样列，覆盖更多的查询条件。

更多唯一键索引和唯一键表的介绍详情可参考[唯一键表](/docs/6517/1451290)、 [ByteHouse Unique 表最佳实践](/docs/6517/145505)。

注意

**Primary key 和 Unique key 的区别？**

Primary key会自带稀疏索性加速查询，Unique key会保证数据唯一（同一个分区中，如果unique key相同的情况，后写进去的数据会覆盖前面的数据），建议选择这两种key的时候从需求考虑，查询会作为过滤条件的字段可以考虑做为Primary key。

### 分桶 Bucketing (Cluster By)

分桶常用于以下场景，具体请参考 [应用案例](/docs/6517/166175#%E5%BA%94%E7%94%A8%E6%A1%88%E4%BE%8B)。

1. **通用场景:** 数据分布不均匀
   * **定义及原理**：当分区无法实现数据的均匀分布时，可以利用分桶字段。 分桶字段保证一列数据均匀分布在集群的每个节点下。 这可以最大限度地提高查询的集群性能。 分区字段的合理设置也有助于解决数据倾斜问题，保证数据分布更加均匀。
   * **字段限制**：不支持 Nullable。
   * **配置建议**：选择分组依据中经常出现的字段。
   * 表创建成功后，该字段不允许修改列类型。
2. **特定场景**：重复数据删除速度慢
   * **定义和原理**：当设置了Unique Key并且单个分区中的数据过多（例如超过1亿行）时，数据摄取的速度将会受到影响。 这是因为需要获取锁才能进行重复数据删除。 在这种情况下，您可以将分区划分为存储桶以提高数据摄取速度。
   * **字段限制**：不支持 Nullable。
   * **配置建议**：Bucket Key需要与Unique Key相同。 （每个桶应小于1000万行）

注意

更改现有表以添加存储桶只会影响新分区，但不会影响现有分区。

### 采样

用于抽样的表达式，该配置为可选项。

如果要用抽样表达式，主键中必须包含这个表达式。例如： `SAMPLE BY intHash32(UserID) ORDER BY (CounterID, EventDate, intHash32(UserID))`。

### 列和表的 TTL

指定行存储的持续时间并定义数据片段在硬盘和卷上的移动逻辑的规则列表，可选项。

表达式中必须存在至少一个 `Date` 或 `DateTime` 类型的列，比如：
`TTL date + INTERVAl 1 DAY`。

### 压缩

compression\_codec字段可以用于配置编解码器，该配置为可选项，默认值为 LZ4。

ByteHouse支持通用目的编码和特定编码，通用编解码器更像默认编解码器(LZ4, ZTSD)及其修改版本。特定编解码器是为了利用数据的特定特征使压缩更有效而设计的。

1. **通用编码**

* NONE : 无压缩。
* LZ4 : 默认值，无损[极速压缩算法](https://github.com/lz4/lz4)。
* LZ4HC[(level)] : 具有可配置级别的LZ4HC高压缩率算法。level默认值为9，支持值[1 ~ 12]，推荐选用[4 ~ 9]。
* ZSTD[(level)] : 具有可配置级别的ZSTD压缩算法。level默认值为1，支持[1 ~ 22]。

2. **特定编码算法**

* Delta(delta\_bytes) : 增量编码，即保留第一位并存储后续每两个值之间差值的算法。默认值为 sizeof(type)， 可选值为1、2、4或8，若为其他值则视为1。

3. **多编解码器**

   使用上述多个编解码器。压缩将根据编解码器声明的顺序进行，解压则按相反的顺序进行。

举例参考：

```
CREATE TABLE codec_example
(
    date Date CODEC(Delta, ZSTD),
    ts DateTime CODEC(LZ4HC),
    float_value Float32 CODEC(NONE),
    double_value Float64 CODEC(LZ4HC(9))
)
ENGINE = CnchMergeTree
PARTITION BY tuple()
ORDER BY date

```
### 更多配置

更多建表相关配置，例如 Unique 表，分桶表等，可以参考[最佳实践](/docs/6517/145504)中的对应文档。

## 架构优劣势说明

CnchMergeTree 合并的核心价值在于零存整取：数据分不同批次导入表中，但可以通过合并减少文件数，并让数据顺序存储。使得 ByteHouse 能最大限度运用磁盘强大的顺序读能力，带来极优的查询性能。

但合并的问题也显而易见：如果后台的写入太过零碎（如每次只插入几百行，几十行），则带来非常多的 Part，Merge 任务会导致 CPU 开销、内存占用提升，带来查询任务的性能下降升值出错。此外，如果过多的小文件导致合并变慢，也会导致查询最新的数据时，Part 还没来得及合并，也会导致查询性能降低。

## 常见问题

### 为什么不建议使用 `Select *`?

由于 ByteHouse 为列式存储数据库，数据存放在不同的列存文件（.bin）中，这一设计是为了查询指定列时只需要读取有限的文件数，加速查询。

如果`select *`，后台需要读取所有的`.bin`列存文件，相当于放弃了列存带来的优势。

### 为什么不建议 `Insert Into`插入数据？

一次`Insert Into`会新建一个 part 文件夹，而不断调用`Insert Into`则会带来很多 part，且每个 part 的数据量很小，后台需要长时间的合并才能减少 part 数量。带来的问题：

* 在此期间，查询极慢，因为一个范围查询可能跨若干个 part 中的列存文件。
* 长时间 Merge 不完，占用系统资源。

### 为什么建议查询时加限制分区字段的条件？

限制分区后，查询只会扫描有限的 part 目录，减少扫描数据量，可以大大加速查询。

### 为什么分区字段建议设置为日期字段？

目前 ByteHouse 仅支持可以转为日期的字段（int，string，data，datatime）来配置分区键。因为从业务视角上看，每天的数据量 / 每小时的数据量接近，日期字段分区可以带来每个分区的大小比较均衡，不会造成单个查询的延迟剧烈波动；

### 为什么排序索引建议设置为查询中最常用的字段？

前文中可以看到在每个 block 内会按照排序索引进行排序，并且基于该字段建立了稀疏索引。查询条件中只要带有排序索引，MergeTree 引擎会通过索引中标记的行与数据的对应关系裁剪不必要读取的 granule，扫描行数降低，查询性能提升。

如果查询不带排序索引，则只能进行全文件的扫描，效率很低。