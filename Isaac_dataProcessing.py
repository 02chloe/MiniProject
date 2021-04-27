import pandas as pd
import json
from tqdm import tqdm
import numpy as np
import gc 

# Initialization


def price_values(dataList):
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
    if x>0:
        return 1
    elif x<=0:
        return 0
    else:
        return 0

def get_data(fileName,interval):
    tapesPath = './DataSet_B02/%stapes.csv'%(fileName)
    LOBPath = './DataSet_B02/%sLOBs.txt'%(fileName)
    tapes = pd.read_csv(tapesPath,header=None)
    tapes.rename(columns={0:'date',1:'stock',2:'time',3:'price'},inplace=True)
    with open(LOBPath) as f:
        lob  = f.readlines()
    times = []
    bid = []
    ask = []
    for i in lob:
        lobdata = json.loads(i)
        times.append(lobdata[1])
        bid.append(lobdata[2][1])
        ask.append(lobdata[3][1])
    totalData = pd.DataFrame({'times':times,'bid':bid,'ask':ask})
    del times,bid,ask,lob
    gc.collect()
    def get_most_close_value(x):
        index = (np.abs(totalData['times']-x)).argmin()
        return totalData['times'][index]
    v = pd.DataFrame({'tmpTimes':np.arange(1,totalData['times'].max(),interval)})
    v['times'] = v['tmpTimes'].apply(get_most_close_value)
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

for file in tqdm(files):
    if file != 'TstB02_2022-01-14':
        data = get_data(file,5)
        targetData = pd.DataFrame(np.array([i for i in data['x'].values]))
        targetData['y'] = data['diff']
        targetData['date'] = data['date']
        targetData.to_csv('data.csv',mode='a',index=None,header=None)
