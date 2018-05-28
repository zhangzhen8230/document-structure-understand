import pandas as pd
import numpy as np
import csv
df_train = pd.read_csv('./input/train100.csv')
labeldic = {1: '论文名称', 2: '姓名', 3: '单位', 4: '邮箱', 5: '中文摘要', 6: '中文关键词', 7: '英文摘要', 8: '英文关键词', 9: '一级标题', 10: '文本段', 11: '二级标题', 12: '公式', 13: '图片', 14: '图题', 15: '表题', 16: '表格', 17: '三级标题', 18: '程序代码', 19: '四级标题'}
ser = df_train['段落角色'].value_counts()
print(ser)
# doc_index = df[df['段落角色']=='-'].value_counts()
# shuffle_ix = np.random.permutation(np.arange(doc_index.shape[0]))
# shuffle_ix = shuffle_ix[:160]
#
# train_shuffle_ix = shuffle_ix[int(len(shuffle_ix)*0.2):]
#
# df_train = pd.concat(df[doc_index[x]+1:doc_index[x+1]+1] for x in train_shuffle_ix if x < len(doc_index)-1)
# df_train = pd.concat((df[:doc_index[0]+1],df_train))
# print(df_train.loc[df_train['段落角色']=='-','段落角色'].value_counts())
# df_train.to_csv('./input/train.csv',index=False,header=False,encoding='utf-8')
