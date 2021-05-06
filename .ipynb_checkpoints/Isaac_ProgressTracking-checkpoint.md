# Authors and acknowledgment
- YANG ZICHUN (Isaac Yang)
- Stu_ID: 2009705
- Email : cm20952@bristol.ac.uk

# Introduction
This document is to record the planning idea and exploration process tracking of my indivudual part of Mini-Project. The document is divided into English version and Chinese version. Note that this document is not a prototype of the final delivered report, so it has no any present significance and is only contributing to indivudual tracking of progress during the project.

文档是为了记录我对Mini-Project的独立部分的计划和探索过程跟踪。文档分为英文版和中文版。请注意，该文档不是最终交付报告的原型，因此它没有汇报意义，仅用于项目期间的进度跟踪。

# English Version
### 一、Plan

- 1、[Preliminary] to know how stock trading works; to know what is Level 2 data, level 2 data structure. 

- 2、[Preliminary] Poor math background->Study statistics, as courses going on, study machine learning, deep learning etc...

- 3、[Target]:

        1st attempt is to predict rise and fall, classification.
        2nd attempt is to make a regression solution.
        
- 4、☆[Implementation]：

         
- 5、[Visualization and analysis]

- 7、[Result]：

- 8、[Challenge]: 

# Chinese-Simplified Version

### 一、计划

- 1、[Preliminary] level 2 行情数据理解：什么是 level 2 行情数据；行情数据储存结构，基本了解。 

- 2、[Preliminary] 随着课程的深入，补充统计学的知识，没有统计学背景；我学习了监督式，非监督式、回归。。。。。。。。。。。。AI方面和统计学的基础知识

- 3、[Target] 确立目标:

        第1阶段的目标为预测涨和跌，分类任务；
        第2阶段的任务为回归任务，由易到难
        
- 4、[Implementation] ★实施：

         4.1 [Data processing] 原始数据，清洗，整理，归类; 应用特征工程
         4.2 [Model Selection] 第1阶段->为什么选择Xgboost和LSTM,给出justification
                               第2阶段-> 回归任务的模型选择
         4.3 [Trainning data]  训练数据
         
- 5、[Visualization and analysis]可视化3个结果，并且分析

- 7、[Result]：如果指导用户根据曲线，进行投资措施。

- 8、[Challenge]: 讨论 1. 拿到数据不知道如何处理？ attempt: 用所有数据作为特征--->数量太大
                        2. 第1次尝试后发现分类任务无法应用到实际股票市场，
                         比如，股民或者用户拿我产出的这些有什么意义？solution: 进行第2次尝试，做回归任务，打造价格曲线，有实际意义
                         3. 计算资源不够？ attempt: 截取小部分数据e.g. 01.04~01.10 (agile methodology)先跑起来，慢慢加

### 二、数据清理首次尝试

1. 清理 level2 数据

    (1). 针对【tapes】类文件，获取文件内的日期、标的、时间戳（相对开盘时间的时间戳）、价格字段，留作后用
    
    (2). 针对【LOBs】类文件。获取文件内的时间戳（相对开盘时间的时间戳）、bid【数组形式，包含价格和数量】、ask【数组形式，包含价格和数量】，然后对每一个时间戳内的 bid 以及 ask 做特征工程，分别取价格、数量的最大、最小、平均值、中位数、方差，则每一个时间戳将会得到 2\*5 一共 10 个特征。

    (3). 结合同一个日期的同一个标的的【LOBs】文件以及【tapes】文件，确定【LOB】文件内某一个时间戳，标的的实际价格。确定的规则为：【tapes】时间戳小于【LOBs】时间戳的价格列表中的最后一个数值（即小于 LOBs 且最接近 LOBs 时间戳的时间的标的价格）

    (4). 对比【LOBs】价格中的一列，获取时间戳价格的变动方向，相对上一个时间点增加，则标记为【1】，否则标记为【0】

2. 使用 xgboost 模型，以 LOB 文件中的 10 个特征作为输入，以 LOB 文件中价格变动方向作为输出，训练模型。最终达到 99%的精准度。

3. 优化数据清洗的速度

4. 优化模型参数
