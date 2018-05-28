import pandas as pd
import numpy as np
import csv
number = 33
# df = pd.read_csv('./input/train{}.csv'.format(number),encoding= 'utf-8')
# train = df.loc[df['段落角色']!='19' ]
# train = train.loc[train['段落角色']!='18']
# train = train.loc[train['段落角色']!='7']
# train = train.loc[train['段落角色']!='8']
# train['段落角色'] = train['段落角色'].replace({'9':'7','10':'8','11':'9','12':'10','13':'11','14':'12','15':'13','16':'14','17':'15'})
# train.to_csv('./liu_qian/train{}.csv'.format(number),index=False,header=False)
# print(df.columns)
df = pd.read_csv('./input/Test.csv',encoding= 'utf-8')
print(df.loc[df['段落角色']=='-','段落角色'].value_counts())
doc_index = df[df['段落角色']=='-'].index.values
shuffle_ix = np.random.permutation(np.arange(doc_index.shape[0]))
shuffle_ix = shuffle_ix[:number]
df_test = pd.concat(df[doc_index[x]+1:doc_index[x+1]+1] for x in shuffle_ix if x < len(doc_index)-1)


# '''
# {1: '论文名称', 2: '姓名', 3: '单位', 4: '邮箱', 5: '中文摘要', 6: '中文关键词',
# 7: '英文摘要', 8: '英文关键词', 9: '一级标题', 10: '文本段', 11: '二级标题', 12: '公式',
# 13: '图片', 14: '图题', 15: '表题', 16: '表格', 17: '三级标题', 18: '程序代码', 19: '四级标题'}
#
# '''
df_test = df_test.loc[df['段落角色']!='19' ]
df_test = df_test.loc[df_test['段落角色']!='18']
df_test = df_test.loc[df_test['段落角色']!='7']
df_test = df_test.loc[df_test['段落角色']!='8']
df_test['段落角色'] = df_test['段落角色'].replace({'9':'7','10':'8','11':'9','12':'10','13':'11','14':'12','15':'13','16':'14','17':'15'})
df_test.to_csv('./liu_qian/test{}.csv'.format(number),index=False,header=False,encoding='utf-8')
#
#
# df_train.to_csv('./input/train.csv',index=False,encoding='utf-8')
#
# df_org = train = pd.read_table('data/traindata.txt',sep='\t',quoting=csv.QUOTE_NONE,encoding='utf-8')
#
# df_test_org = pd.concat(df_org[doc_index[x]+1:doc_index[x+1]+1] for x in test_shuffle_ix if x < len(doc_index)-1)
# df_test_org.to_csv('./input/test_orginal.csv',index=False)