import pandas as pd
import json
from tqdm import tqdm
import numpy as np
import gc 

# @Author : Isaac YANG ZICHUN 
# @Stu_ID: 2009705
# @Email : cm20952@bristol.ac.uk
# @File : dataProcessing.py
# @Interpreter: Python 3.7 on Google Colab
# @Desc: this python file is used for data cleaning, data processing


def price_values(dataList):
    """
    1.To get all prices of LOB.txt in one day
    e.g. ask: [234,1], [232,2], [231,3]... ---Processing---> [234,232,231...]
 
    2.To get the Maximum, Minimum, Mean, Variance and Standard Deviation of it.
    return: [Maximum, Minimum, Mean, Variance, Standard Deviation]
    """
    dataList = np.array(dataList)
    if len(dataList)>0:
        maxValue = dataList[0][0]
        minValue = dataList[-1][0]
        meanValue = np.mean(dataList[:,0])
        medianValue = np.median(dataList[:,0])
        stdValue = np.std(dataList[:,0])
        return [maxValue, minValue,meanValue,medianValue,stdValue]
    else:
        return None,None,None,None,None

def amount_values(dataList):
    """
    1. To get all amount of LOB.txt in one day
    e.g. ask:[[234,1],[232,2],[231,3]] ---Processing---> [1, 2, 3...]
   
    2.To get the Maximum, Minimum, Mean, Variance and Standard Deviation of it.
    return: [Maximum, Minimum, Mean, Variance, Standard Deviation]
    """
    dataList = np.array(dataList)
    if len(dataList)>0:
        maxValue = np.max(dataList[:,1])
        minValue = np.min(dataList[:,1])
        meanValue = np.mean(dataList[:,1])
        medianValue = np.median(dataList[:,1])
        stdValue = np.std(dataList[:,1])
        return [maxValue, minValue,meanValue,medianValue,stdValue]
    else:
        return None,None,None,None,None

def combine_price_amount_values(dataList):
    """
    1. To get combination of prices and amounts of LOB.txt in one day
    e.g. ask:[[234,1],[232,2],[231,3]] ---Processing---> [234，232，232，231，231，231]
   
    2.To get the Maximum, Minimum, Mean, Variance and Standard Deviation of it.
    return: [Maximum, Minimum, Mean, Variance, Standard Deviation]
    """
    if len(dataList)>1:
        tmp = []
        for i in dataList:
            tmp+=[i[0]]*i[1]
        dataList = np.array(tmp)
        if len(dataList)>1:
            maxValue = dataList[0]
            minValue = dataList[-1]
            meanValue = np.mean(dataList)
            medianValue = np.median(dataList)
            stdValue = np.std(dataList)
            return maxValue, minValue,meanValue,medianValue,stdValue
    else:
        return None,None,None,None,None

def mark_diff(x):
    """
    Gets the label value.
    For example,   
                    ...        ...     ...
                    09:31:01   $250     0
                    09:31:02   $251     1          #Comparing to 9:31:01, $251>$250, so label is 1
                    09:31:03   $230     0          #Comparing to 9:31:02, $230<$250, so label is 0
    1 represents rising and 0 represents falling
    return: 1/0
    """
    if x>0:
        return 1
    elif x<=0:
        return 0
    else:
        return 0

def get_data(fileName,interval):
    """
    To extract original data to be targeted
    First 10 columns are features with the 11th column is label, the 12th column is date.
    Params: 
        fileName: LOB path and Tapes path
        interval: Given a time interval to pick up data from huge data, this can be modified based on computing capacity
                    I give it to be 5 as default, normally every running time is 4 hours to complete on Google Colab free account.
                        The larger interval is, the running time will be more.
    return: a dataframe -> 126	5	79.4	    105	    44.38400613	 146	 677	 277.0384615	 155	 194.0621393	0	    TstB02_2022-03-16
                           144	24	109.8863636	128	    35.59763521	 145	 656	 258.25	         167	 184.0076048	1	    TstB02_2022-03-16
                           142	11	117.0185185	133.5	33.38800558	 147	 788	 372.6415094	 192	 237.6046418	1	    TstB02_2022-03-16
                           ...
                           ...
                           ...
    """
    tapesPath = './DataSet_B02/%stapes.csv'%(fileName)
    LOBPath = './DataSet_B02/%sLOBs.txt'%(fileName)
    tapes = pd.read_csv(tapesPath,header=None)
    tapes.rename(columns={0:'date',1:'stock',2:'time',3:'price'},inplace=True)
    with open(LOBPath) as f:
        lob  = f.readlines()
    times = []
    bid = []
    ask = []
    # get bid and ask price e.g. ["time", 1.258, ["bid", [[220, 4]]], ["ask", [[328, 3], [800, 1]]]]
    for i in lob:
        lobdata = json.loads(i)
        times.append(lobdata[1]) # [1.258,]
        bid.append(lobdata[2][1]) # [[220,4],...]
        ask.append(lobdata[3][1]) # [[328,3],[800,1]]
    totalData = pd.DataFrame({'times':times,'bid':bid,'ask':ask}) 
    
    """
    e.g. totalData is :
    
         times                                                bid                                 ask
    0    881.195  [[267, 2], [259, 3], [258, 2], [257, 2], [256,...     [[269, 1], [273, 4], [275, 3], [276, 1], [278,...    
    1    881.212  [[267, 2], [259, 3], [258, 2], [257, 2], [256,...     [[269, 1], [273, 4], [275, 3], [276, 1], [278,...      
    2    881.229  [[267, 2], [259, 3], [258, 2], [257, 2], [256,...     [[269, 1], [273, 4], [275, 3], [276, 1], [278,...     
    3    881.246  [[267, 2], [259, 3], [258, 2], [257, 2], [256,...     [[269, 1], [273, 4], [275, 3], [276, 1], [278,...     
    4    881.263  [[267, 2], [259, 3], [258, 2], [257, 2], [256,...     [[269, 1], [273, 4], [275, 3], [276, 1], [278,...   
    
    """
    del times,bid,ask,lob
    gc.collect() #clean memory
    
    
    # pick up data according to interval given, because data is too huge, every running process will cost much time
    def get_most_close_value(x):
        index = (np.abs(totalData['times']-x)).argmin()
        return totalData['times'][index]
    v = pd.DataFrame({'tmpTimes':np.arange(1,totalData['times'].max(),interval)})
    v['times'] = v['tmpTimes'].apply(get_most_close_value)
    """  
    V['tmpTimes']：
           tmpTimes    
    0         1.0  
    1         6.0  
    2        11.0  
    3        16.0  
    4        21.0  
    5        26.0  
    6        31.0  
    """
    mergedData = pd.merge(v,totalData,how='left',on=['times'])
    del totalData
    gc.collect()
    print('7')
    
    def getTapPrice(times):
        try:
            price = tapes[tapes['time']<=times]['price'].values[-1]
        except:
            price =None
        return price
        
    mergedData['price'] = mergedData['times'].apply(getTapPrice)
    del tapes
    gc.collect()
    print('9')
    
    # Combine processed data 
    mergedData['x_bid'] = mergedData['bid'].apply(lambda x :combine_price_amount_values(x))
    mergedData['x_ask'] = mergedData['ask'].apply(lambda x :combine_price_amount_values(x))
    mergedData['x'] = mergedData['x_bid'] + mergedData['x_ask']

    a = [i for i in mergedData['price'][1:].values - mergedData['price'][:-1].values]
    a.append(np.NAN)
    mergedData['diff'] = a
    mergedData['diff'] = mergedData['diff'].apply(lambda x :mark_diff(x))
    mergedData['date'] = [fileName]*len(mergedData)
    return mergedData
    
import os
files = list(set([i[0:17] for i in os.listdir('./DataSet_B02') if i[0:17]  !='.ipynb_checkpoint']))

# System Entrance
for file in tqdm(files):
    if file != 'TstB02_2022-01-14':
        data = get_data(file,5)
        targetData = pd.DataFrame(np.array([i for i in data['x'].values]))
        targetData['y'] = data['diff']
        targetData['date'] = data['date']
        targetData.to_csv('data.csv',mode='a',index=None,header=None)
