#coding=utf-8
import pandas as pd
import  numpy as np
import csv
# from
from  sklearn.preprocessing import MinMaxScaler
# def alter(file,old_str,new_str):
#     """

#     替换文件中的字符串
#     :param file:文件名
#     :param old_str:就字符串
#     :param new_str:新字符串
#     :return:
#     """
#     file_data = ""
#     with open(file, "r", encoding="utf-8") as f:
#         for line in f:
#             if old_str in line:
#                 # line = line.replace("摘	要\n","摘要")
#                 line = line.replace("摘要\n","摘要")
#                 # line = line.replace("表\n","表")
#                 # line = line.replace("摘\t要","摘要")
#             file_data += line
#     with open(file,"w",encoding="utf-8") as f:
#         f.write(file_data)
# alter("./data/test.txt","摘要\n","摘要")
df  = pd.read_table('./data/traindata.txt',sep='\t',quoting=csv.QUOTE_NONE,encoding='utf-8')
print(df[:10])
del df['文本内容']
print(len(df['字号']))
# print()
# print(df["f6"])
# dftest = pd.read_table('data/test.txt',sep='\t',names=["label","f0","字体","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15"]
# )
# print(df.columns)
# names=["label","关键字","字号","字形","字数","编号","编号位置","word对象","行距","缩进","段前距","断后距","对齐方式","大纲级别","标点","f15"]

# labeldic = df['label'].unique()
# for x in range(labeldic.shape[0]):
#     labeldic[x] =labeldic[x].split('_')[0].replace("xslw:","")
# print(labeldic)

df.drop(["段前距","段后距"], axis=1, inplace=True)
df = df.replace({'9999999':0})

# df
# df[df['f14'].isnull()]

# df.f2
data1 = np.array(df['字号'])

# data1
# # print (data1)
# # print(pd.Series(normalizefont()))
everyfont = [] #每一篇文章的字号集合
onehotfont = []
fontdata = []
index_null =0
for font in data1:  #每篇文档的字号减去正文字号，然后求标准化
    index_null +=1
    if (font!='-'):
        everyfont.append(float(font))
    elif len(everyfont)!=0:
        # count = np.bincount(everyfont)   #将出现次数最多的字体认为是正文
        # common_value = np.argmax(count)
        # print(common_value)
        common_value = max(everyfont,key=everyfont.count)
        # print(common_value)
        dataminusfont = [everyfontx-common_value for everyfontx in everyfont] #减去正文字体
        dataminusfont = np.array(dataminusfont)
        # print(dataminusfont)
        datafontlast = MinMaxScaler().fit_transform(dataminusfont.reshape(-1,1)) #调用sklearn库进行标准化
        for value in range(len(dataminusfont)):
            if(dataminusfont[value]>0):
                dataminusfont[value]=1
            elif dataminusfont[value]<0:
                dataminusfont[value]=-1
        fontdata = np.append(fontdata,datafontlast)
        fontdata = np.append(fontdata,np.array(['100'])) #添加每篇的分隔符
        onehotfont = np.append(onehotfont,dataminusfont)
        onehotfont = np.append(onehotfont,np.array(['100'])) #添加每篇的分隔符
        everyfont=[]

    else:
        print("请定位%d 并查看结果"%index_null)
del df['字号']
# print (onehotfont)
df['字号'] = pd.Series(fontdata)
# df['字号2'] = pd.Series(onehotfont)
# print (fontdata)
'''
对于字体，求频率
'''
# fontname = df['字体']
# begin = 0
# # print(fontname[0])
# everydocfontname = [] #每篇文档的字体集合
# for everfontname in range(len(fontname)):
#     if fontname[everfontname]=='-':
#         everydocfontname = np.array(everydocfontname)
#         # print (begin,(begin+len(everydocfontname)+1))
#         for i in range(begin, (begin+len(everydocfontname))):
#             fontname[i] = np.sum(everydocfontname==everydocfontname[i-begin])/len(everydocfontname)
#
#         begin = begin+len(everydocfontname)+1
#         everydocfontname =[]
#     else:
#         everydocfontname.append(fontname[everfontname])
del df['字体']
# df['字体'] = fontname
###获取其对比
def fenge(arr,prefix):
    # print(arr)
    for x in range(arr.shape[0],):
        if(arr[x]!=prefix+'_-'):  ##以‘-’为区分符号
            arr[x] = 0
        else:
            arr[x] = 1
    return arr
def toOnehot(ser,df,prefix):
    outline = pd.get_dummies(ser,prefix=prefix)  #将其转换为onehot编码
    # outline
    outline_array = np.array(outline)
    outline_array = outline_array.astype(np.float)
    zerodata = fenge(np.array(outline.columns),prefix)
    #看看是否等于以1开头的数组
    for x in range(outline_array.shape[0]):
        # print(outline_array[0])
        if (outline_array[x]==zerodata).all():
            outline_array[x] = np.array(['100']*(zerodata.shape[0]))
    outlinedf = pd.DataFrame(outline_array,columns=outline.columns)
    # print(outlinedf)
    del outlinedf[prefix+'_-']
    df = pd.concat([outlinedf,df], axis=1)
    # print (outlinedf)
    return df
print('开始处理标点')
df = toOnehot(df['标点'],df,'标点')
del df['标点']  #删除第一列
print('开始处理编号位置 ')
df = toOnehot(df['编号位置'],df,'编号位置')
del df['编号位置']
print('开始处理word对象')
df = toOnehot(df['word对象'],df,'word对象')
del df['word对象']

df = toOnehot(df['编号'],df,'编号')
# del df['编号']
print('开始处理大纲级别')
df = toOnehot(df['大纲级别'],df,'大纲级别')
del df['大纲级别']
print('开始处理对齐方式')
df = toOnehot(df['对齐方式'],df,'对齐方式')
del df['对齐方式']
print('开始处理等号')
df = toOnehot(df['等号'],df,'等号')
del df['等号']
print('开始处理关键字')
df = toOnehot(df['关键字'],df,'关键字')
del df['关键字']
'''
行距
'''
hangju = np.array(df['行距'].replace({'-':-1})).astype(np.float)
max = hangju.max()
# max = df['f5'].describe()[max]
for i in range(len(hangju)):
    if hangju[i]!=-1 :
        hangju[i] = (hangju[i])/max
hangjudf = pd.DataFrame(hangju,columns={'行距'})
hangjudf = hangjudf.replace({-1:'-'})
df = pd.concat([hangjudf,df], axis=1)
del df['行距']
'''
缩进 todo
'''
# suojin = np.array(df['缩进'].replace({'-':-1})).astype(np.float)
# abssuojin = np.abs(suojin)
# max = abssuojin.max()
# # max = df['f5'].describe()[max]
# for i in range(len(suojin)):
#     if suojin[i]!=-1 :
#         suojin[i] = (suojin[i])/max
# suojindf = pd.DataFrame(suojin,columns={'suojin'})
# suojindf = suojindf.replace({-1:'-'})
# df = pd.concat([suojindf,df], axis=1)
# everyfont = [] #每一篇文章的字号集合
# onehotfont = []
# fontdata = []
# data1 = np.array(df['缩进'])
# for font in data1:  #每篇文档的字号减去正文字号，然后求标准化
#     if (font!='-'):
#         everyfont.append(float(font))
#     elif len(everyfont)!=0:
#         # print(common_value)
#         # common_value = max(everyfont,key=everyfont.count)
#         # # print(common_value)
#         # dataminusfont = [everyfontx-common_value for everyfontx in everyfont] #减去正文字体
#         dataminusfont = np.array(everyfont)
#         maxfont = np.max(np.abs(dataminusfont))
#         dataminusfont = dataminusfont/maxfont
#         # print(dataminusfont)
#         # datafontlast = MinMaxScaler().fit_transform(dataminusfont.reshape(-1,1)) #调用sklearn库进行标准化
#         # print(dataminusfont)
#         fontdata = np.append(fontdata,dataminusfont)
#         fontdata = np.append(fontdata,np.array(['100'])) #添加每篇的分隔符
#         # onehotfont = np.append(onehotfont,dataminusfont)
#         # onehotfont = np.append(onehotfont,np.array(['100'])) #添加每篇的分隔符
#         everyfont=[]

# print (onehotfont)
del df['缩进']
# df['缩进']= pd.Series(fontdata)
# print(max)


# df = df.replace(docreconstruct/test.py:127labeldic)

# biaotidic = {"一级标题":"标题","二级标题":"标题","三级标题":"标题","四级标题":"标题",}
# df = df.replace(biaotidic)
df = df.replace({'100':'-',100:'-',"文本段落":"文本段","列表段落":"文本段","非数字":"0"})
labeldic = df['段落角色'].unique()
# print((labeldic))
# print(len(labeldic))
labeldic = labeldic.tolist()
labeldic.remove('-')
dic = {x:(y+1) for x,y in zip(labeldic,range(len(labeldic)))}
def getdic():
    return dic
print(dic)
dict_new = {value:key for key,value in dic.items()}
print (dict_new)
def getnewdic():
    return dict_new
df = df.replace(dic)
label = df['段落角色']
df.drop(labels=['段落角色'], axis=1,inplace = True)
df['d2v_id'] = df.index.values
df['段落角色'] = label
df.to_csv('data/train.csv',index=False,header=True,encoding='utf-8')
print((df.columns))
