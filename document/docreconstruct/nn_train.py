# -*- coding: utf-8 -*-

import yaml
import multiprocessing
import pickle
import pandas as pd
from sklearn.cross_validation import StratifiedKFold
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM,GRU
from keras.layers.core import *
from keras.optimizers import Adam
from keras.models import model_from_yaml,Model
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.layers import \
    Bidirectional,Conv2D,Conv1D,Input,Reshape,GlobalMaxPool2D,concatenate,\
    BatchNormalization,Convolution1D,MaxPooling1D,merge,GlobalMaxPool1D,MaxPooling2D,GlobalAvgPool2D,TimeDistributed
vocab_dim = 300
number_filters = 100
maxlen = 50
batch_size = 128
n_epoch = 15
input_length = 100
adam_lr = 0.0002
adam_beta_1 =0.5
# yaml_file = 'lstm_attention'
SINGLE_ATTENTION_VECTOR = False
yaml_file = 'attention_lstm'
cpu_count = multiprocessing.cpu_count()
df_train = pd.read_csv('./input/train.csv')
df_val = pd.read_csv('./input/validate.csv')
df_test = pd.read_csv('./input/predict_first.csv')
print ('Creat a Word2vec model...')
#载入模型
def word2vec_train():
    model = Word2Vec.load('./vec_model/Word2vec_model.pkl')
    w2indx,w2vec = create_dictionaries(model)
    return   w2indx,w2vec
#创建词语字典，并返回每个词语的索引，词向量，以及每个句子所对应的词语索引
def create_dictionaries(model=None):
    if  (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(),
                            allow_update=True)
        w2indx = {v: k+1 for k, v in gensim_dict.items()}
        w2vec = {word: model[word] for word in w2indx.keys()}
        return w2indx, w2vec
    else:
        print ('No data provided...')
w2indx,w2vec=word2vec_train()
#提取分完词后的文件
def loadfile(path):
    output = open('./input/{}_cut'.format(path)+ u".pkl", 'rb')
    words = pickle.load(output)
    output.close()
    return words


'''
将词语转换为index
'''
def parse_dataset(cut_text,w2indx):
    data=[]
    for sentence in cut_text:
        new_txt = []
        for word in sentence:
            try:
                new_txt.append(w2indx[word])
            except:
                new_txt.append(0)
        data.append(new_txt)
    data = sequence.pad_sequences(data,padding='post', maxlen=maxlen)
    return data
'''
计算权重矩阵和词汇数
'''
def get_data(index_dict,word_vectors):
    n_symbols = len(index_dict) + 1  # 所有单词的索引数，频数小于n_explosore的词语索引为0，所以加1
    embedding_weights = np.zeros((n_symbols, vocab_dim))
    for word, index in index_dict.items():#从索引为1的词语开始，对每个词语对应其词向量
        embedding_weights[index, :] = word_vectors[word]
    return n_symbols,embedding_weights



'''
定义相关网络结构
'''


def get_model(embedding_weights,n_symbols):
    inp = Input(shape=(maxlen, ))
    emb = Embedding(input_dim=n_symbols,output_dim=vocab_dim,trainable=False,weights=[embedding_weights])(inp)
    x = Bidirectional(GRU(50, return_sequences=True))(emb)
    x = GlobalMaxPool1D()(x)
    x = Dropout(0.1)(x)
    x = Dense(50, activation="relu")(x)
    x = Dropout(0.1)(x)
    # x = Dense(5, activation="softmax")(x)
    # x = concatenate([pool1, pool2, pool3, pool4], axis=1)
    x = Dense(1, activation='relu')(x)
    # x = Dense(5, activation="softmax")(x)
    model = Model(inputs=inp, outputs=x)
    model.compile(loss='mse',
                  optimizer='adam',
                  metrics=[rmse_round_s,rmse_s])
    return model
def train_lstm(n_symbols,embedding_weights,x_train,y_train,x_val,y_val):

    print ('Defining a Keras Model...')
    model = textcnn(embedding_weights,n_symbols)
    print('write model to yaml file..')
    yaml_string = model.to_yaml()
    with open('./lstm_data/{}.yml'.format(yaml_file), 'w') as outfile:
        outfile.write( yaml.dump(yaml_string, default_flow_style=True) )
    print ("Train...")
    checkpoint = ModelCheckpoint("./lstm_data/{}.hdf5".format(yaml_file), monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    early = EarlyStopping(monitor="val_loss", mode="min", patience=20)
    callbacks_list = [checkpoint, early]
    # x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
    # x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
    # model.load_weights("./lstm_data/word2vec_rnn_cnn_classify.hdf5")
    # model.load_weights("./lstm_data/{}.hdf5".format(yaml_file))
    model.fit(x_train, y_train, batch_size=batch_size, nb_epoch=n_epoch,verbose=1, validation_data=(x_val, y_val),callbacks=callbacks_list,)
    model.load_weights("./lstm_data/{}.hdf5".format(yaml_file))
    print ("Evaluate...")
    score = model.evaluate(x_val, y_val,
                                batch_size=batch_size)
    print ('Test score:', score)

##5折交叉验证求平均
def train_lstm_Kfold(n_symbols,embedding_weights,x_train,y_train,x_val,y_val,x_test):
    print ('Defining a Simple Keras Model...')
    stack_te = np.zeros((x_test.shape[0]))
    stack_tr = np.zeros((x_train.shape[0]))
    for k,(tr,va) in enumerate(StratifiedKFold(y_train,random_state=27,n_folds=5)):
        print(' stack:{}/{}'.format(k+1,5))
        X_train = x_train[tr]
        Y_train = y_train[tr]
        # model = model_attention_applied_after_lstm(embedding_weights,n_symbols)
        model = textcnn(embedding_weights,n_symbols)
        print ("Train...")
        checkpoint = ModelCheckpoint("./lstm_data/{}.hdf5".format(yaml_file), monitor='val_loss', verbose=1, save_best_only=True, mode='min')
        early = EarlyStopping(monitor="val_loss", mode="min", patience=20)
        #
        callbacks_list = [checkpoint, early]
        # X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
        # x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
        # x_val = x_val.reshape((x_val.shape[0], 1, x_val.shape[1]))
        model.fit(X_train, Y_train, batch_size=batch_size, epochs=n_epoch,verbose=1, validation_data=(x_val, y_val),callbacks=callbacks_list,)
        model.load_weights("./lstm_data/{}.hdf5".format(yaml_file))
        # y_pred_va = model.predict_proba(X_train[va])
        y_pred = model.predict(x_test).flatten()
        stack_te += y_pred
        stack_tr[va] +=model.predict(x_train[va]).flatten()
    stack_te /= 5
    print(len(stack_te),len(df_test))
    df_test['Score'] = stack_te
    df_train['Score1'] = stack_tr
    df_test.to_csv('./result/predit_5_fold_{}.csv'.format(yaml_file),encoding='utf-8',index=0)
    df_train.to_csv('./result/train_5_fold_{}.csv'.format(yaml_file),encoding='utf-8',index=0)
def train():
    print('loading cut file...')
    train_cut = loadfile('train')
    validate_cut = loadfile('validate')
    print ('Setting up Arrays for Keras Embedding Layer...')
    x_train = parse_dataset(train_cut,w2indx)
    x_val = parse_dataset(validate_cut,w2indx)

    y_train = df_train.Score.values
    y_val = df_val.Score.values
    n_symbols,embedding_weights=get_data(w2indx,w2vec)
    print('starting nn step')
    train_lstm(n_symbols,embedding_weights,x_train,y_train,x_val,y_val)

    # test_cut = loadfile('test')
    # print ('Setting up Arrays for Keras Embedding Layer...')
    # x_test = parse_dataset(test_cut,w2indx)
    # train_lstm_Kfold(n_symbols,embedding_weights,x_train,y_train,x_val,y_val,x_test)

def lstm_predict():
    print ('loading model......')
    with open('./lstm_data/{}.yml'.format(yaml_file), 'r') as f:
        yaml_string = yaml.load(f)
    model = model_from_yaml(yaml_string)
    cut_test = loadfile('validate')
    print ('loading weights......')
    model.load_weights('./lstm_data/{}.hdf5'.format(yaml_file))
    model.compile(loss='mse',
                  optimizer='adam',metrics=[rmse_round_s,rmse_s])
    x_test = parse_dataset(cut_test,w2indx)
    result=model.predict(x_test)
    return result

def predict_tocsv(tagetpath):
    df_pre = pd.read_csv('./input/validate.csv',encoding='utf-8') #对结果进行预测
    result = lstm_predict()
    result = result.flatten()
    print(result.shape)
    df_pre['predict_score'] = result
    df_pre.to_csv(tagetpath,index=False,header=False)
if __name__=='__main__':
    train()  #训练模型
    predict_tocsv('./result/validattention_after_lstm.csv')