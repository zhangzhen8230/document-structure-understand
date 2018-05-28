from gensim.models import Doc2Vec
import csv
import pandas as pd
model = Doc2Vec.load( './vec_model/dbow_d2v.model')
train = pd.read_table('input/traindata.txt',sep='\t',quoting=csv.QUOTE_NONE,encoding='utf-8')
train['d2v_id'] = train.index.values
del train['文本内容']
train.to_csv('./input/data_id.csv',index=False,encoding='utf-8')
