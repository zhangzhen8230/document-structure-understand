#coding=utf-8
'''
对word2vec进行训练，
toddo:验证如何选择最好的参数
'''
import csv
import multiprocessing
import numpy as np
import jieba
import pickle
import pandas as pd
from sklearn.cross_validation import KFold
from gensim.models.word2vec import Word2Vec

vocab_dim = 300
maxlen = 50
n_iterations = 50  # ideally more..
n_exposures = 2
window_size = 3
input_length = 100
cpu_count = multiprocessing.cpu_count()
train = pd.read_table('input/traindata.txt',sep='\t',quoting=csv.QUOTE_NONE,encoding='utf-8')
train = train.fillna('空白')
print(train.loc[train['文本内容'].isnull(),'文章名称'])
#对句子经行分词
def tokenizer(text,path):
    ''' 去除停用词，然后分词，存入文档。
    '''
    print('{} file starting'.format(path))
    words = []
    for word_value in text:
        try:
            sentence_seged = list(jieba.lcut(word_value.strip()))
        except:
            print(word_value)
        words.append(sentence_seged)
    output = open('./input/{}_cut'.format(path) + u".pkl", 'wb')
    pickle.dump(words, output)  # 索引字典
    output.close()
    print('{}  file has save done '.format(path))
#提取分完词后的文件句子
def get_tokenizer(path):
    output = open('./input/{}_cut'.format(path)+ u".pkl", 'rb')
    words = pickle.load(output)
    output.close()
    return words
'''
word2vec训练方法
'''
def word2vec_train(combined):
    print('starting trainning word2vec')
    model = Word2Vec(size=vocab_dim,
                     min_count=n_exposures,
                     window=window_size,
                     workers=cpu_count,
                     iter=n_iterations)
    model.build_vocab(combined)
    model.train(combined,total_examples=model.corpus_count,epochs=model.iter)
    model.save('./vec_model/Word2vec_model.pkl')
    print('word2vec has trained done')
if __name__ == '__main__':
    '''
    对句子进行分词
    '''
    tokenizer(train['文本内容'],'train')

    '''
    提取分完词后的向量
    '''
    train_dis_cut = get_tokenizer('train')
    '''
    训练word2vec
    '''
    word2vec_train(train_dis_cut)