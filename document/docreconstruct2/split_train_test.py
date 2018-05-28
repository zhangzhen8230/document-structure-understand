import pandas as pd
import numpy as np
import csv
df = pd.read_csv('./data/train.csv')
doc_index = df[df['段落角色']=='-'].index.values
shuffle_ix = np.random.permutation(np.arange(doc_index.shape[0]))
# shuffle_ix = shuffle_ix[:int(len(shuffle_ix)*0.8)]
test_shuffle_ix = shuffle_ix[:int(len(shuffle_ix)*0.2)]
train_shuffle_ix = shuffle_ix[int(len(shuffle_ix)*0.2):]
df_test = pd.concat(df[doc_index[x]+1:doc_index[x+1]+1] for x in test_shuffle_ix if x < len(doc_index)-1)
df_train = pd.concat(df[doc_index[x]+1:doc_index[x+1]+1] for x in train_shuffle_ix if x < len(doc_index)-1)
df_train = pd.concat((df[:doc_index[0]+1],df_train))
print(df_train.loc[df_train['段落角色']=='-','段落角色'].value_counts())
print(df_test.loc[df_test['段落角色']=='-','段落角色'].value_counts())
# del df_test['文章名称'],df_train['文章名称']
'''
{1: '论文名称', 2: '姓名', 3: '单位', 4: '邮箱', 5: '中文摘要', 6: '中文关键词',
7: '英文摘要', 8: '英文关键词', 9: '一级标题', 10: '文本段', 11: '二级标题', 12: '公式',
13: '图片', 14: '图题', 15: '表题', 16: '表格', 17: '三级标题', 18: '程序代码', 19: '四级标题'}

'''
df_test.to_csv('./input/test.csv',index=False,encoding='utf-8')


df_train.to_csv('./input/train.csv',index=False,encoding='utf-8')
#
# df_org = train = pd.read_table('data/traindata.txt',sep='\t',quoting=csv.QUOTE_NONE,encoding='utf-8')
#
# df_test_org = pd.concat(df_org[doc_index[x]+1:doc_index[x+1]+1] for x in test_shuffle_ix if x < len(doc_index)-1)
# df_test_org.to_csv('./input/test_orginal.csv',index=False)