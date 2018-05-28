'''train dbow/dm for education/age/gender'''

import pandas as pd
import jieba
from datetime import datetime
from collections import namedtuple
from gensim.models import Doc2Vec
import csv
import codecs
import numpy as np
train = pd.read_table('input/traindata.txt',sep='\t',quoting=csv.QUOTE_NONE,encoding='utf-8')
train = train.fillna('空白')
#-------------------add row number to query----------------------
doc_f = codecs.open('./data/alldata-id.txt','w',encoding='utf8')
for i,queries in enumerate(train['文本内容']):
    words = []
    words.extend(list(jieba.cut(queries)))
    tags = [i]
    if i % 10000 == 0:
        print(datetime.now(),i)
    doc_f.write('_*{} {}'.format(i,' '.join(words)+'\n'))
doc_f.close()
print("alldata has saved in alldataid.txt")

SentimentDocument = namedtuple('SentimentDocument', 'words tags')
class Doc_list(object):
    def __init__(self,f):
        self.f = f
    def __iter__(self):
        for i,line in enumerate(open('./data/alldata-id.txt',encoding='utf8')):

            words = line.split()

            tags = [int(words[0][2:])]
            words = words[1:]
            yield SentimentDocument(words,tags)
d2v = Doc2Vec(dm=0, size=300, negative=5, hs=0, min_count=3, window=30,sample=1e-5,workers=8,alpha=0.025,min_alpha=0.025)
doc_list = Doc_list('./data/alldata-id.txt')
d2v.build_vocab(doc_list)

for i in range(8):
    print(datetime.now(),'pass:',i + 1)
    doc_list = Doc_list('alldata-id.txt')
    print(type(doc_list))
    d2v.train(doc_list,total_examples=100000,epochs=10)
d2v.save('./vec_model/dbow_d2v.model')
print(datetime.now(),'save done')


