import pandas as pd
import numpy as np

df = pd.read_csv('./data/train.csv')

print(df['段落角色'].value_counts())
print(df.loc[df['缩进']==0,'段落角色'].value_counts())
# print(df[['缩进','段落角色']])
del df['字体']
doc_index = df[df['段落角色']=='-'].index.values
shuffle_ix = np.random.permutation(np.arange(doc_index.shape[0]))
test_shuffle_ix = shuffle_ix[:int(len(shuffle_ix)*0.2)]
train_shuffle_ix = shuffle_ix[int(len(shuffle_ix)*0.2):]
df_test = pd.concat(df[doc_index[x]+1:doc_index[x+1]+1] for x in test_shuffle_ix if x < len(doc_index)-1)
df_train = pd.concat(df[doc_index[x]+1:doc_index[x+1]+1] for x in train_shuffle_ix if x < len(doc_index)-1)
df_train = pd.concat((df[:doc_index[0]+1],df_train))
print(df_train.loc[df_train['段落角色']=='-','段落角色'].value_counts())
print(df_test.loc[df_test['段落角色']=='-','段落角色'].value_counts())
df_test.to_csv('./input/test.csv',index=False,encoding='utf-8')
df_train.to_csv('./input/train.csv',index=False,encoding='utf-8')