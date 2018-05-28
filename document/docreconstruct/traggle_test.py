# coding=utf-8
import h5py
from docreconstruct.data_helper import get_data
import numpy as np
import  pandas as pd
# import keras
from keras.models import Sequential
from keras.layers import Dense,LSTM,GRU,Masking,Bidirectional,TimeDistributed
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras.models import load_model
from keras import regularizers
import matplotlib.pyplot  as plt
pred_list = [] #输出的list
original_list = [] #最开始的list
test_data_end = [] #记录错误的特征
num_class = 21
# data,label,test_data,test_label,train_document_num,test_document_num = get_data("data/tezhen_number.csv","data/testnumber.csv")  #读取数据
real_test_data,real_test_label,rtest_data,test_label,train_document_num,real_test_document_num = get_data("data/testdata.csv","data/testdata.csv")
# print(real_test_data[0])
orginlabel = real_test_label.copy()#用作最后的对比
maxlength = 500  #每篇文章的最大段落数目是150
seqlength = len(real_test_data[0][0]) #特征数量
print(seqlength)

labeldic ={1: '论文名称', 2: '姓名', 3: '单位', 4: '中文摘要', 5: '中文关键词', 6: '英文摘要', 7: '一级标题', 8: '文本段', 9: '公式', 10: '二级标题', 11: '图片', 12: '图题', 13: '英文关键词', 14: '表题', 15: '表格', 16: '三级标题', 17: '程序代码', 18: '四级标题', 19: '邮箱', 20: '五级标题'}

real_test_label = np_utils.to_categorical(real_test_label,num_class) #将label转化为onehot编码
real_test_label  = real_test_label.reshape(real_test_document_num,maxlength,num_class)  #重排为numpy数组


model = load_model('model.h5') #载入模型

real_y_pred = model.predict_classes(real_test_data)

# print(model.evaluate(real_test_data,real_test_label))
i = 0 #文章总段落数量
error =0#不相等的个数
y_pred =  real_y_pred.astype(int)
orginlabel = orginlabel.astype(int)
# print(orginlabel)
j=0 #错误的段落位置
for x,y in zip(y_pred,orginlabel):

    for l,s in zip(x,y):

        if s!=0:
            j +=1;
            i =i+1
        if(l!=s&int(s)!=0):
            error = error+1
            # print ("文本段落标签:%s  "%labeldic[s],"lstm预测标签: %s  "%labeldic[l])
            pred_list.append(labeldic[s])
            original_list.append((labeldic[l]))
            test_data_end.append((j))
print ("测试总段落数%f:"%i,"错误识别段落数%f："%error,"正确率:%f"%((i-error)/i))
output_to_csv = {"位置":test_data_end,"实际":pred_list,"预测":original_list}
dataframe = pd.DataFrame(output_to_csv)
dataframe.to_csv("data/error.csv",index=False,encoding='gbk')