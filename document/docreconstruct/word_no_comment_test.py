# coding=utf-8
'''
对文档未标注数据进行预测，调用模型，得出结果，保存文件
'''
import h5py
from docreconstruct.test_data_helper import get_data
from docreconstruct.test_woad_data_pre import  test_ch_csv
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
test_ch_csv()
pred_list = [] #输出的list
original_list = [] #最开始的list
test_data_end = [] #记录错误的特征
num_class = 21
# data,label,test_data,test_label,train_document_num,test_document_num = get_data("data/tezhen_number.csv","data/testnumber.csv")  #读取数据
real_test_data,real_test_document_num = get_data("data/testdata.csv")
maxlength = 500  #每篇文章的最大段落数目是150
seqlength = len(real_test_data[0][0]) #特征数量
zeronp = np.zeros(seqlength)  ##对比数组 用于判断有多少段
numpara = 0
for x in real_test_data:
    for z in x:
        if (z==zeronp).all():
               break;
        else:
             numpara +=1
print(numpara)
labeldic ={1: '论文名称', 2: '姓名', 3: '单位', 4: '中文摘要', 5: '中文关键词', 6: '英文摘要', 7: '一级标题', 8: '文本段', 9: '公式', 10: '二级标题', 11: '图片', 12: '图题', 13: '英文关键词', 14: '表题', 15: '表格', 16: '三级标题', 17: '程序代码', 18: '四级标题', 19: '邮箱', 20: '五级标题'}
model = load_model('model.h5') #载入模型
real_y_pred = model.predict_classes(real_test_data)
real_y_pred = np.transpose(real_y_pred)
label_df = pd.DataFrame(real_y_pred)
label_df = label_df.replace(labeldic)
label_df = label_df[:numpara]
label_df.to_csv("./data/result.csv",header=False,index=False,encoding='utf-8')