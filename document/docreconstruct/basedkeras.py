# coding=utf-8
import h5py
from docreconstruct.data_helper import get_data
import numpy as np
import  pandas as pd
# import keras
from keras.layers.core import *
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.models import Sequential,Model
from keras.layers import  merge,concatenate,RepeatVector,Dense,LSTM,GRU,Masking,Bidirectional,TimeDistributed,MaxPooling1D,Permute,Reshape,Embedding,Flatten,Dropout
from keras.utils import np_utils
from keras.models import load_model
from keras import regularizers,Input
import matplotlib.pyplot  as plt
from gensim.models import Doc2Vec
SINGLE_ATTENTION_VECTOR = True
pred_list = [] #输出的list
original_list = [] #最开始的list
all_pred_list = [] #输出的list
all_original_list = [] #最开始的list
test_data_end = [] #记录错误的特征
number = 300
numbertest = 200
num_class = 16
maxlength = 500  #每篇文章的最大段落数目是150
n_epochs = 30
doc2vec_model =  Doc2Vec.load('./vec_model/dbow_d2v.model')
data,label,train_doc2id,test_data,test_label,test_doc2id,train_document_num,test_document_num = get_data("liu_qian/train{}.csv".format(number),"liu_qian/test{}.csv".format(numbertest))
#shuffle测试集和训练集合,然后按照80-20划分
orginlabel = test_label.copy()#用作最后的对比

seqlength = len(data[0][0]) #特征数量
print(seqlength)
print(train_document_num)
X_train = np.zeros((train_document_num,maxlength,300))
X_test = np.zeros((len(test_label),maxlength,300))
print(len(test_doc2id))
def get_doc2vec_data(doc2id,X):
    for num,num_doc in enumerate(doc2id):
        for i,id in enumerate(num_doc):
            if(id=='-1'):
                X[num,i,] = np.array([0]*300)
            else:
                X[num,i,] = doc2vec_model.docvecs[int(id)]
    return X
X_train = get_doc2vec_data(train_doc2id,X_train)
X_test = get_doc2vec_data(test_doc2id,X_test)
# ix_cutoff = int(x_shuffle.shape[0]*0.8)

labeldic = {1: '论文名称', 2: '姓名', 3: '单位', 4: '邮箱', 5: '中文摘要', 6: '中文关键词', 7: '一级标题', 8: '文本段', 9: '二级标题', 10: '公式', 11: '图片', 12: '图题', 13: '表题', 14: '表格', 15: '三级标题'}
label = np_utils.to_categorical(label,num_class) #将label转化为onehot编码
label  = label.reshape(len(label),maxlength,num_class)  #重排为numpy数组
print(label)
test_label = np_utils.to_categorical(test_label,num_class) #将label转化为onehot编码
test_label  = test_label.reshape(len(test_label),maxlength,num_class)  #重排为numpy数组
print('shape:',test_label.shape)
print('data shape',data.shape)
# label =  sequence.pad_sequences(label, maxlen=130, padding='post')
def attention_3d_block(emb):
     input_dim = int(emb.shape[2])
     a = Permute((2, 1))(emb)
     a = Reshape((input_dim, maxlength))(a) # this line is not useful. It's just to know which dimension is what.
     a = Dense(maxlength, activation='softmax')(a)
     if SINGLE_ATTENTION_VECTOR:
         a = Lambda(lambda x: K.mean(x, axis=1), name='dim_reduction')(a)
         a = RepeatVector(input_dim)(a)
     a_probs = Permute((2, 1), name='attention_vec')(a)
     output_attention_mul = merge([emb, a_probs], name='attention_mul', mode='mul')
     return output_attention_mul
def model_attention_applied_before_lstm():
    inputs = Input(shape=(maxlength,seqlength))
    attention_mul = attention_3d_block(inputs)
    x = Bidirectional(GRU(50, return_sequences=True))(attention_mul)
    x = Dropout(0.1)(x)
    x = Dense(50, activation="relu")(x)
    x = Dropout(0.1)(x)
    x = TimeDistributed(Dense(num_class, activation='softmax'))(x)
    model = Model(inputs=inputs, outputs=x)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
def model_attention_applied_after_lstm():
     inputs = Input(shape=(maxlength,seqlength))
     print(inputs.shape)
     lstm_out = Bidirectional(GRU(50,kernel_regularizer=regularizers.l2(0.01), return_sequences=True))(inputs)
     lstm_out = Bidirectional(GRU(50, kernel_regularizer=regularizers.l2(0.01),return_sequences=True))(lstm_out)
     attention_mul = attention_3d_block(lstm_out)
     x =TimeDistributed(Dense(num_class,activation='softmax'))(attention_mul)
     print(x.shape)
     model = Model(input=inputs, output=x)
     model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
     return model
def GRU_model():
    inputs1 = Input((maxlength,seqlength),name='feature')
    inputs2 = Input((maxlength,300),name = 'doc2vec')
    x1 = Masking(mask_value=0)(inputs1)
    x2 = Masking(mask_value=0)(inputs2)
    x1 = Dense(100)(x1)
    x2 = Dense(50)(x2)
    x = concatenate([x1,x2])
    x = Bidirectional(GRU(128, return_sequences=True,dropout=0.2))(x)
    x = Dense(128)(x)
    x = Bidirectional(GRU(50, return_sequences=True,dropout=0.2))(x)
    x = Dense(50)(x)
    x = TimeDistributed(Dense(num_class,activation='softmax'))(x)
    model = Model([inputs1,inputs2], output=x)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
def GRU_only_Feature_model():
    inputs1 = Input((maxlength,seqlength))
    x1 = Masking(mask_value=0)(inputs1)
    x = Bidirectional(GRU(128, return_sequences=True,dropout=0.2))(x1)

    x = Bidirectional(GRU(128, return_sequences=True,dropout=0.2))(x)
    x = TimeDistributed(Dense(num_class,activation='softmax'))(x)
    model = Model(inputs1, output=x)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
train_data = {
    'feature':data,
    'doc2vec':X_train
}
te_date = {
    'feature':test_data,
    'doc2vec':X_test
}
checkpoint = ModelCheckpoint("./model_file/Blstm_feature_doc2vec.hdf5", monitor='val_loss', verbose=1, save_best_only=True, mode='min')
early = EarlyStopping(monitor="val_loss", mode="min", patience=20)
callbacks_list = [checkpoint, early]
model = GRU_model()
# model = model_attention_applied_before_lstm()
history = model.fit(train_data, label,epochs=n_epochs,validation_split=0.2,shuffle=False,callbacks=callbacks_list,batch_size=10)  #训练500轮并添加交叉验证
model = load_model('./model_file/Blstm_feature_doc2vec.hdf5') #载入模型
y_pred = []
y_pred_pro= model.predict(te_date) #预测模型
for x in y_pred_pro:
    every_pre = []
    for i in x:
        every_pre.append(np.argmax(i))
    y_pred.append(every_pre)
# real_y_pred = model.predict_classes(real_test_data)
i = 0 #文章总段落数量
error =0#不相等的个数
y_pred = np.array(y_pred)
y_pred =  y_pred.astype(int)
orginlabel = orginlabel.astype(int)
# print(orginlabel)
j=0 #错误的段落位置
print(y_pred)
for x,y in zip(y_pred,orginlabel):
    j +=1
    for l,s in zip(x,y):
        if int(s)!=0:
            j +=1
            i =i+1
            all_pred_list.append(labeldic[s])
            all_original_list.append((labeldic[l]))
        if(l!=s&int(s)!=0):
            error = error+1
            # print ("文本段落标签:%s  "%labeldic[s],"lstm预测标签: %s  "%labeldic[l])
            pred_list.append(labeldic[s])
            original_list.append((labeldic[l]))
            test_data_end.append((j))
output_to_csv = {"位置":test_data_end,"实际":pred_list,"预测":original_list}
all_output_to_csv = {"实际":all_pred_list,"预测":all_original_list}
dataframe = pd.DataFrame(output_to_csv)
alldataframe = pd.DataFrame(all_output_to_csv)
# print(test_data.)
# test_data = np.reshape(test_data,(test_data.shape[0]*test_data.shape[1] ,test_data.shape[2]))
# print(test_data.shape)
# df = pd.DataFrame(test_data,columns = ['f0_abstract', 'f0_keywords', 'f0_null', 'f0_关键字', 'f0_关键词', 'f0_图',
#        'f0_摘要', 'f0_表', 'f11_wdAlignParagraphCenter',
#        'f11_wdAlignParagraphDistribute', 'f11_wdAlignParagraphJustify',
#        'f11_wdAlignParagraphLeft', 'f11_wdAlignParagraphRight',
#        'f12_wdOutlineLevel1', 'f12_wdOutlineLevel2', 'f12_wdOutlineLevel3',
#        'f12_wdOutlineLevel4', 'f12_wdOutlineLevel5', 'f12_wdOutlineLevel6',
#        'f12_wdOutlineLevel7', 'f12_wdOutlineLevel8', 'f12_wdOutlineLevel9',
#        'f12_wdOutlineLevelBodyText', 'f5_null', 'f5_段尾', 'f5_段首', 'f13_False',
#        'f13_True', 'f2', 'f3', 'f9', 'f10', 'f1'])

# print(df)
print ("测试总段落数%f:"%i,"错误识别段落数%f："%error,"正确率:%f"%((i-error)/i))
# print(model.evaluate(test_data, test_label))
dataframe.to_csv("data/error.csv",index=False,encoding='gbk')
alldataframe.to_csv("data/result{}.csv".format(number),index=False,encoding='gbk')
# df.to_csv("data/error1.csv",index=True,header=True,encoding='gbk')
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