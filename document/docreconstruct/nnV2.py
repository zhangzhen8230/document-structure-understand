#-*-coding:utf8-*-
import pandas as pd
import  numpy as np
import yaml
from keras.layers import Input,Masking,Bidirectional,GRU,Embedding,Dense,TimeDistributed,concatenate,LSTM,BatchNormalization
from keras_contrib.layers.crf import CRF
from keras.models import Model,model_from_yaml,load_model
from keras.utils import np_utils
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.regularizers import l2
from keras.optimizers import adam
yaml_file = 'gru_xuewei'
max_par_num = 1000
max_duiqifangshi = 6
max_dagangjibie = 11
max_wordduixiang = 5
max_keyword = 9
max_bianhao = 11
max_bianhaoweizhi = 4
num_class = 23
df_train = pd.read_csv('./input/train.csv',encoding='utf-8')
normal_feature_num = 8


weight_keyword = np.identity(max_keyword)
weight_bianhaoweizhi = np.identity(max_bianhaoweizhi)
weight_wordduixiang = np.identity(max_wordduixiang)
weight_duiqifangshi = np.identity(max_duiqifangshi)
weight_dagangjibie = np.identity(max_dagangjibie)
weight_bianhao = np.identity(max_bianhao)
def get_keras_data(path,step):
    df_train = pd.read_csv(path,encoding='utf-8')
    df_train = df_train.fillna('0')
    df_train.loc[df_train['字形']=='0','字形']=1
    df_train.loc[df_train['标点']=='0','标点']=-1
    df_train.loc[df_train['字数']=='0','字数']=-1
    keyword_df = df_train[['关键字']]
    bianhao_df = df_train[['编号']]
    bianhaoweizhi_df = df_train[['编号位置']]
    wordduixiang_df = df_train[['word对象']]
    duiqifangshi_df = df_train[['对齐方式']]
    dagangjibie_df = df_train[['大纲级别']]
    df_normal_feature = df_train[['等号','字形','字数','标点','中文比例','邮箱符号','字号','缩进']]
    feature_normal = toArray(df_normal_feature,'等号')
    wordduixiang = toArray(wordduixiang_df,"word对象")
    bianhaoweizhi = toArray(bianhaoweizhi_df,'编号位置')
    keyword = toArray(keyword_df,'关键字')
    duiqifangshi = toArray(duiqifangshi_df,'对齐方式')
    dagangjibie = toArray(dagangjibie_df,'大纲级别')
    bianhao = toArray(bianhao_df,'编号')

    X ={
        'feature_normal':feature_normal,
        'wordduixiang':wordduixiang,
        'bianhaoweizhi':bianhaoweizhi,
        'keyword':keyword,
        'duiqifangshi':duiqifangshi,
        'dagangjibie':dagangjibie,
        'bianhao':bianhao
    }
    print(X)
    if step!='predict':
        label_df = df_train[['段落角色']]
        orginal_label = toArray(label_df,'段落角色')
        label = np_utils.to_categorical(orginal_label,num_class)
        print(label.shape)
        return X,label,orginal_label
    else:
        return X
def toArray(df,name):
    doc_index = df[df[name]=='-'].index.values
    print(name,len(doc_index))
    traindata =  df.iloc[0:doc_index[0]]
    traindata = traindata.astype(float)
    b = np.zeros(shape=(1000-doc_index[0],len(df.iloc[1])))
    traindata = np.row_stack((traindata,b))
    for x in range(len(doc_index)):
        if(x+1<len(doc_index)):
           data =  df.iloc[doc_index[x]+1:doc_index[x+1]].values
           data = data.astype(float)
           if doc_index[x+1]-(doc_index[x]+1)<1000:
                b = np.zeros(shape=(1000-(doc_index[x+1]-(doc_index[x]+1)),len(df.iloc[1])))
                data = np.row_stack((data,b))
           else:
               data = data[:1000]
           traindata = np.concatenate((traindata,data),axis=0)
           # print(traindata.shape)
    if name=='等号':
        traindata = np.reshape(traindata,newshape=(len(doc_index),max_par_num,len(df.iloc[1])))
    else :
        traindata = np.reshape(traindata,newshape=(len(doc_index),max_par_num))
    print(name,traindata.shape)
    return traindata
def GRU_only_Feature_model():
    input_featrue_noraml = Input((max_par_num,normal_feature_num),name='feature_normal')
    input_bianhao = Input((max_par_num,),name='bianhao')
    emb_bianhao = Embedding(max_bianhao,max_bianhao,mask_zero=True,weights=[weight_bianhao])(input_bianhao)
    input_wordduixiang = Input((max_par_num,),name='wordduixiang')
    emb_wordduixiang = Embedding(max_wordduixiang,max_wordduixiang,mask_zero=True,weights=[weight_wordduixiang])(input_wordduixiang)
    input_bianhaoweizhi = Input((max_par_num,),name='bianhaoweizhi')
    emb_bianhaoweizhi = Embedding(max_bianhaoweizhi,max_bianhaoweizhi,mask_zero=True,weights=[weight_bianhaoweizhi])(input_bianhaoweizhi)
    input_keyword = Input((max_par_num,),name='keyword')
    emb_keyword = Embedding(max_keyword,max_keyword,mask_zero=True,weights=[weight_keyword])(input_keyword)
    input_duiqifangshi = Input((max_par_num,),name='duiqifangshi')
    emb_duiqifangshi = Embedding(max_duiqifangshi,max_duiqifangshi,mask_zero=True,weights=[weight_duiqifangshi])(input_duiqifangshi)
    input_dagangjibie = Input((max_par_num,),name='dagangjibie')
    emb_dagangjibie = Embedding(max_dagangjibie,max_dagangjibie,mask_zero=True,weights=[weight_dagangjibie])(input_dagangjibie)
    fe = concatenate([input_featrue_noraml,emb_bianhaoweizhi,emb_dagangjibie,emb_duiqifangshi,emb_keyword,emb_wordduixiang,emb_bianhao])
    # input_featrue_noraml = Input((max_par_num,normal_feature_num),name='feature_normal')
    # input_bianhao = Input((max_par_num,),name='bianhao')
    # emb_bianhao = Embedding(max_bianhao,max_bianhao,mask_zero=True)(input_bianhao)
    # input_wordduixiang = Input((max_par_num,),name='wordduixiang')
    # emb_wordduixiang = Embedding(max_wordduixiang,max_wordduixiang,mask_zero=True)(input_wordduixiang)
    # input_bianhaoweizhi = Input((max_par_num,),name='bianhaoweizhi')
    # emb_bianhaoweizhi = Embedding(max_bianhaoweizhi,max_bianhaoweizhi,mask_zero=True)(input_bianhaoweizhi)
    # input_keyword = Input((max_par_num,),name='keyword')
    # emb_keyword = Embedding(max_keyword,max_keyword,mask_zero=True)(input_keyword)
    # input_duiqifangshi = Input((max_par_num,),name='duiqifangshi')
    # emb_duiqifangshi = Embedding(max_duiqifangshi,max_duiqifangshi,mask_zero=True)(input_duiqifangshi)
    # input_dagangjibie = Input((max_par_num,),name='dagangjibie')
    # emb_dagangjibie = Embedding(max_dagangjibie,max_dagangjibie,mask_zero=True)(input_dagangjibie)
    # fe = concatenate([emb_bianhaoweizhi,emb_dagangjibie,emb_duiqifangshi,emb_keyword,emb_wordduixiang,emb_bianhao])
    print(fe.shape)
    fe = Masking(mask_value=0)(fe)
    x = Bidirectional(GRU(32, return_sequences=True,dropout=0.2))(fe)
    # x = Bidirectional(GRU(128, return_sequences=True,dropout=0.2))(x)
    x = TimeDistributed(Dense(num_class))(x)
    crf = CRF(num_class, sparse_target=False,learn_mode='join')
    x = crf(x)
    model = Model(inputs=[input_featrue_noraml,input_wordduixiang,input_bianhaoweizhi,input_keyword,input_duiqifangshi,input_dagangjibie,input_bianhao], output=x)
    # myadam = adam(lr=0.001,decay=1e-6)

    model.compile(loss=crf.loss_function,
            # loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=[crf.accuracy])
    print(model.summary())
    return model
def train():
    train_data,train_label,_ = get_keras_data('./input/train.csv','train')
    model = GRU_only_Feature_model()
    checkpoint = ModelCheckpoint("./model_file/{}.hdf5".format(yaml_file), monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    early = EarlyStopping(monitor="val_loss", mode="min", patience=20)
    callbacks_list = [checkpoint, early]
    # model.load_weights('./model_file/Blstm_feature_doc2vec.hdf5')
    model.fit(train_data, train_label,epochs=20,batch_size=10,callbacks=callbacks_list,validation_split=0.2,shuffle=True)
    yaml_string = model.to_yaml()
    with open('./model_file/{}.yml'.format(yaml_file), 'w') as outfile:
        outfile.write( yaml.dump(yaml_string, default_flow_style=True) )
def test(path):
    test_data,test_label,orginal_label = get_keras_data(path,'test')
    # with open('./model_file/{}.yml'.format(yaml_file), 'r') as f:
    #     yaml_string = yaml.load(f)
    # model = model_from_yaml(yaml_string)
    model = GRU_only_Feature_model()
    model.load_weights('./model_file/{}.hdf5'.format(yaml_file))
    # model.compile(loss='categorical_crossentropy',
    #               optimizer='adam',
    #               metrics=['accuracy'])
    # model.compile(loss=crf.loss_function,
    #     # loss='categorical_crossentropy',
    #           optimizer='adam',
    #           metrics=[crf.accuracy])
    y_pred = []
    y_pred_pro= model.predict(test_data) #预测模型
    for x in y_pred_pro:
        every_pre = []
        for i in x:
            every_pre.append(np.argmax(i))
        y_pred.append(every_pre)
    i = 0 #文章总段落数量
    error =0#不相等的个数
    y_pred = np.array(y_pred)
    y_pred =  y_pred.astype(int)
    orginal_label =  orginal_label.astype(int)
    labeldic =  {0:'错误',1:'中文摘要标题', 2:'中文关键词',3:'英文摘要标题',4:'英文关键词',5: '一级标题',
                 6:'二级标题', 7:'文本段',8: '三级标题', 9:'图片', 10:'图题',
                 11:'表题', 12:'表格',13: '四级标题',14: '程序代码',15: '五级标题',
                 16:'公式',17: '论文名称',18: '姓名',19: '单位',20: '邮箱',21:'中文摘要内容',22:'英文摘要内容'}
    # labeldic =  {0:'错误',1:'中文摘要', 2:'中文关键词',3:'英文摘要',4:'英文关键词',5: '标题',
    #               6:'文本段',7:'图片', 8:'图题',
    #              9:'表题', 10:'表格',11: '程序代码',
    #              12:'公式',13: '论文名称',14: '姓名',15: '单位',16: '邮箱'}
    all_pred_list=[]   #预测标签结果
    all_original_list =[] #实际标签结
    for x,y in zip(y_pred,orginal_label):
        for l,s in zip(x,y):
            if int(s)!=0:
                all_original_list.append(labeldic[s])
                all_pred_list.append((labeldic[l]))
    all_output_to_csv = {"预测":all_pred_list,"实际":all_original_list}
    alldataframe = pd.DataFrame(all_output_to_csv)
    alldataframe.to_csv("data/result.csv",index=False,encoding='gbk')
def predict(path):
    test_data = get_keras_data(path,'predict')
    with open('./model_file/{}.yml'.format(yaml_file), 'r') as f:
        yaml_string = yaml.load(f)
    model = model_from_yaml(yaml_string)
    model.load_weights('./model_file/{}.hdf5'.format(yaml_file))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    y_pred = []
    y_pred_pro= model.predict(test_data) #预测模型
    for x in y_pred_pro:
        every_pre = []
        for i in x:
            every_pre.append(np.argmax(i))
        y_pred.append(every_pre)
    i = 0 #文章总段落数量
    error =0#不相等的个数
    y_pred = np.array(y_pred)
    y_pred =  y_pred.astype(int)
    labeldic =  {0:'错误',1:'中文摘要', 2:'中文关键词',3:'英文摘要',4:'英文关键词',5: '一级标题',
                 6:'二级标题', 7:'文本段',8: '三级标题', 9:'图片', 10:'图题',
                 11:'表题', 12:'表格',13: '四级标题',14: '程序代码',15: '五级标题',
                 16:'公式',17: '论文名称',18: '姓名',19: '单位',20: '邮箱',21:'中文摘要内容',22:'英文摘要内容'}
    all_pred_list=[]   #预测标签结果
    for x in y_pred:
        for l in x:
            if int(l)!=0:
                all_pred_list.append((labeldic[l]))
    all_output_to_csv = {"预测":all_pred_list}
    alldataframe = pd.DataFrame(all_output_to_csv)
    alldataframe.to_csv("data/result.csv",header=False,index=False,encoding='utf8')
if __name__ == '__main__':
    train()
    test('./input/test.csv')
    # predict('./data/test.csv')
