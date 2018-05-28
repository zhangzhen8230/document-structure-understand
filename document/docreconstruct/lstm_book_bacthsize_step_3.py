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
# data,label,test_data,test_label,train_document_num,test_document_num = get_data("data/tezhen_number.csv","data/testnumber.csv")  #读取数据
data,label,test_data,test_label,train_document_num,test_document_num = get_data("data/test.csv","data/test.csv")
#shuffle测试集和训练集合,然后按照80-20划分
data = data.astype(np.float)
shuffle_ix = np.random.permutation(np.arange(data.shape[0]))
x_shuffle = data[shuffle_ix]
y_shuffle = label[shuffle_ix]
ix_cutoff = int(x_shuffle.shape[0]*0.8)
data ,test_data = x_shuffle[:ix_cutoff],x_shuffle[ix_cutoff:]
label,test_label = y_shuffle[:ix_cutoff],y_shuffle[ix_cutoff:]
orginlabel = test_label.copy()#用作最后的对比
maxlength = 500  #每篇文章的最大段落 数目是150
seqlength = len(data[0][0]) #特征数量
labeldic = {1:"xslw:论文名称",2:"xslw:姓名",3:"xslw:单位",4:"slw:中文摘要",5:"xslw:中文关键词",6:"xslw:英文摘要"
            ,7:"xslw:一级标题",8:"xslw:文本段",9:"xslw:公式",10:"xslw:二级标题",11:"xslw:三级标题",12:"xslw:四级标题"
            ,13:"xslw:图片",14:"xslw:图题",15:"xslw:英文关键词",16:" xslw:表题",17:"xslw:表格",18:"xslw:列表"}
label = np_utils.to_categorical(label,19) #将label转化为onehot编码
label  = label.reshape(ix_cutoff,maxlength,19)  #重排为numpy数组
test_label = np_utils.to_categorical(test_label,19) #将label转化为onehot编码
# print (test_label)
test_label  = test_label.reshape(int(x_shuffle.shape[0] - ix_cutoff),maxlength,19)  #重排为numpy数组

# label =  sequence.pad_sequences(label, maxlen=130, padding='post')

model = Sequential() # 声明神经网络
model.add(Masking(mask_value=0,input_shape=(maxlength,seqlength)))  #添加masking层过滤添加的-1
# model.add(Dense(128))
# model.add(Bidirectional(GRU(128, return_sequences=True,dropout=0.1)))  #添加双向LSTM
model.add(Bidirectional(GRU(128, return_sequences=True,dropout=0.1)))
model.add(Dense(128))
model.add(Bidirectional(GRU(128, return_sequences=True,dropout=0.1)))
model.add(TimeDistributed(Dense(19,activation='softmax',kernel_regularizer=regularizers.l1(0.01)))) #添加DENSE层。输出为[文章数量，每篇文章段落数，特征个数]

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])#loss损失函数 optimizer优化方法 metrics 评价方法

history = model.fit(data, label,epochs=100,validation_split=0.2,shuffle=True)  #训练500轮并添加交叉验证
# model.summary()##输出网络结构
model.save('model.h5') #保存模型
model = load_model('model.h5') #载入模型
y_pred = model.predict_classes(test_data) #预测模型
print(y_pred)
i = 0 #文章总段落数量
error =0#不相等的个数
y_pred =  y_pred.astype(int)
orginlabel = orginlabel.astype(int)
# print(orginlabel)
for x,y in zip(y_pred,orginlabel):

    for l,s in zip(x,y):
        if s!=0:
            i =i+1
        if(l!=s&int(s)!=0):
            error = error+1
            # print ("文本段落标签:%s  "%labeldic[s],"lstm预测标签: %s  "%labeldic[l])
            pred_list.append(labeldic[s])
            original_list.append((labeldic[l]))
output_to_csv = {"实际":pred_list,"预测":original_list}
dataframe = pd.DataFrame(output_to_csv)

print ("测试总段落数%f:"%i,"错误识别段落数%f："%error,"正确率:%f"%((i-error)/i))
print(model.evaluate(test_data, test_label))
dataframe.to_csv("data/error.csv",index=False,encoding='utf-8')
def printplt():
    # print(history.history.keys())
# summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
printplt()