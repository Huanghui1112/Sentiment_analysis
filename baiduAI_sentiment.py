#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :2020/1/20 15:25
#@Author  :CherryLiu
#@FileName: BaiduAI_sentiment.py
#@Software: PyCharm

import pandas as pd
import time
from aip import AipNlp
import os


APP_ID = '你的APP_ID'
API_KEY = '你的API_KEY'
SECRET_KEY = '你的SECRET_KEY'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def get_sentiments(index_data):
    try:
        time.sleep(0.05)
        text=index_data['content']
        sentiment_dict={0:'negative',1:'neutral',2:'positive'}
        sitems = client.sentimentClassify(text)['items'][0]  # 情感分析
        positive = sitems['positive_prob']  # 积极概率
        negative=sitems['negative_prob']   #消极概率
        confidence = sitems['confidence']  # 置信度
        sentiment= sentiment_dict[sitems['sentiment']] # 0表示消极，1表示中性，2表示积极
        output = '{}\t{}\t{}\t{}\t{}\n'.format(text, positive, negative,confidence, sentiment)
        print(output)
        index_data['positive_prob']=positive
        index_data['negative_prob']=negative
        index_data['confidence']=confidence
        index_data['sentiment']=sentiment
        print(index_data)
        index_data=pd.DataFrame(index_data,index=[0])
        print(index_data)
        savepath='result/sentiment.csv'
        if os.path.exists(savepath):
            index_data.to_csv(savepath,header=None,mode='a+',index=None,encoding='utf-8-sig')
        else:
            index_data.to_csv(savepath,index=None,mode='a+', encoding='utf-8-sig')

    except Exception as e:
        print(e)


def main():
    filename='result/clean_data.xlsx'
    data=pd.read_excel(filename)
    print(data)
    for index in data.index:
        index_data=data.loc[index]
        index_data=dict(index_data)
        get_sentiments(index_data)

if __name__=='__main__':
    main()
