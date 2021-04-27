# Authors and acknowledgment
- YANG ZICHUN (Isaac Yang)
- Stu_ID: 2009705
- Email : cm20952@bristol.ac.uk

# Introduction
This document is to record the planning idea and exploration process tracking of my indivudual part of Mini-Project. The document is divided into English version and Chinese version. Note that this document is not a prototype of the final delivered report, so it has no any present significance and is only contributing to indivudual tracking of progress during the project.

文档是为了记录我对Mini-Project的独立部分的计划和探索过程跟踪。文档分为英文版和中文版。请注意，该文档不是最终交付报告的原型，因此它没有汇报意义，仅用于项目期间的进度跟踪。

# English Version
1
2
3
4
5

# Chinese-Simplified Version
### 一、初步计划

- 1、level 2 行情数据理解：什么是 level 2 行情数据；行情数据储存结构
- 2、基础的时序数据分析：数据清洗、数据提取、数据检验
- 3、文献查找调研：关于 level 2 行情数据的使用案例归纳总结
- 4、模型选择及构建：基于数据分析及调研，进行具象的模型选择
- 5、确定最终的模型评价标准
- 6、搭建回测环境，进行模型鲁棒性分析

### 二、数据清理首次尝试

1. 清理 level2 数据

    (1). 针对【tapes】类文件，获取文件内的日期、标的、时间戳（相对开盘时间的时间戳）、价格字段，留作后用
    
    (2). 针对【LOBs】类文件。获取文件内的时间戳（相对开盘时间的时间戳）、bid【数组形式，包含价格和数量】、ask【数组形式，包含价格和数量】，然后对每一个时间戳内的 bid 以及 ask 做特征工程，分别取价格、数量的最大、最小、平均值、中位数、方差，则每一个时间戳将会得到 2\*5 一共 10 个特征。

    (3). 结合同一个日期的同一个标的的【LOBs】文件以及【tapes】文件，确定【LOB】文件内某一个时间戳，标的的实际价格。确定的规则为：【tapes】时间戳小于【LOBs】时间戳的价格列表中的最后一个数值（即小于 LOBs 且最接近 LOBs 时间戳的时间的标的价格）

    (4). 对比【LOBs】价格中的一列，获取时间戳价格的变动方向，相对上一个时间点增加，则标记为【1】，否则标记为【0】

2. 使用 xgboost 模型，以 LOB 文件中的 10 个特征作为输入，以 LOB 文件中价格变动方向作为输出，训练模型。最终达到 99%的精准度。

3. 优化数据清洗的速度

4. 优化模型参数
