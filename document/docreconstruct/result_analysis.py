import pandas as pd
from pandas import DataFrame

number = 300
# df = pd.read_csv('data/error{}.csv'.format(number),encoding='gbk')
# result = df['实际']
# count = result.describe()['count']
# resultCount = df['实际'].value_counts()/count
# result = pd.DataFrame({"个数":df['实际'].value_counts(),"比例":resultCount})


all_df = pd.read_csv('data/result.csv',encoding='gbk')
correct = all_df[all_df["实际"]==all_df["预测"]]

P = correct['预测'].count()/all_df["预测"].count()
R = correct['预测'].count()/all_df["实际"].count()
print("整体",' ',"实际总数=",all_df["实际"].count(),":\n",'  准确率:P=',P,R )
labeldic = all_df['实际'].unique()
labeldic = labeldic.tolist()
labellist = []
Rlist = []
Plist = []
Flist = []
numlist = []
for i in labeldic:
    R = sum(correct['预测']==i)/sum(all_df["实际"]==i)
    P = sum(correct['预测']==i)/sum(all_df["预测"]==i)
    F = R*P*2/(R+P)
    labellist.append(i)
    Plist.append(P)
    Rlist.append(R)
    Flist.append(F)
    numlist.append(sum(all_df["实际"]==i))
    # print(i,"  实际总数=",sum(all_df["实际"]==i),':\n','召回率:R=',R,'  准确率:P=',P,"  F=",F)
dic = {"准确率":Plist,"召回率":Rlist,"F值":Flist,"标签":labellist,"数量":numlist}
data = DataFrame(dic)
print (data)
index = ["标签","数量","准确率","召回率","F值"]
data = data.reindex(columns=index)
data.to_csv("./liu_qian/score_{}.csv".format(number))