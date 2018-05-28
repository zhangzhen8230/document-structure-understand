#coding=utf-8
'''
存在以下缺陷
1、对于99999的处理直接变为0
2、文档数据有很多没有题目
3、是对每一篇进行归一化 而不是对整体
'''
import pandas as pd
import  numpy as np
from  sklearn.preprocessing import MinMaxScaler
df = pd.read_table('data/Exp_0.8/trainData/train.txt',sep=' ',names=["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","label"]
)

# print(np.array(df.columns).shape[0])
# np.array(['0']*np.array(df.columns).shape[0])
# print(zerodata)
print ("请检查在最后加入分隔符号")

df = df.replace({'9999999':0})
data1 = np.array(df['f4'])
# print (data1)
# print(pd.Series(normalizefont()))
everyfont = [] #每一篇文章的字号集合
fontdata = []
for font in data1:  #每篇文档的字号减去正文字号，然后求标准化
    if (font!='-'):
        everyfont.append(float(font))
    elif len(everyfont)!=0:
        count = np.bincount(everyfont)   #将出现次数最多的字体认为是正文
        common_value = np.argmax(count)
        dataminusfont = everyfont-common_value  #减去正文字体
        # print(dataminusfont)
        datafontlast = MinMaxScaler().fit_transform(dataminusfont.reshape(-1)) #调用sklearn库进行标准化
        fontdata = np.append(fontdata,datafontlast)
        fontdata = np.append(fontdata,np.array(['100'])) #添加每篇的分隔符
        everyfont=[]
del df['f4']
df['f4'] = pd.Series(fontdata)

'''
对于字体，求频率
'''
fontname = df['f2']
begin = 0
# print(fontname[0])
everydocfontname = [] #每篇文档的字体集合
for everfontname in range(len(fontname)):
    if fontname[everfontname]=='-':
        everydocfontname = np.array(everydocfontname)
        # print (begin,(begin+len(everydocfontname)+1))
        for i in range(begin, (begin+len(everydocfontname))):
            fontname[i] = np.sum(everydocfontname==everydocfontname[i-begin])/len(everydocfontname)
        begin = begin+len(everydocfontname)+1
        everydocfontname =[]
    else:
        everydocfontname.append(fontname[everfontname])
del df['f2']
df['f2'] = fontname
'''
针对于关键字，将其转换为onehot编码,问题是因为有‘-’，所以要删除第一列，然后每一个00000都要替换为100,100

'''
keyword = pd.get_dummies(df['f1'])  #将其转换为onehot编码
keyword_array = np.array(keyword)
# keyword_array = keyword_array.astype()
zerodata = np.array([1,0 ,0 ,0 ,0, 0,0,.0 ,0]) #看看是否等于以1开头的数组
for x in range(keyword_array.shape[0]):
    if (keyword_array[x]==zerodata).all():
        keyword_array[x] = np.array(['100']*9)
keyworddf = pd.DataFrame(keyword_array,columns=['-','abstract','keywords','null1','关键字','关键词','图','摘要','表'])
del df['f1']  #删除第一列
del keyworddf['-']
df = pd.concat([keyworddf,df], axis=1)
# del df['f2']
'''
针对于大纲级别，使用以上相同的方法来进行one-hot编码
'''
outline = pd.get_dummies(df['f12'])  #将其转换为onehot编码

outline_array = np.array(outline)
keyword_array = outline_array.astype(np.float)
zerodata = np.array([1,0 ,0 ,0 ,0, 0,0,0 ,0,0]) #看看是否等于以1开头的数组
for x in range(outline_array.shape[0]):
    # print(outline_array[0])
    if (outline_array[x]==zerodata).all():
        outline_array[x] = np.array(['100']*10)
outlinedf = pd.DataFrame(outline_array,columns=['-','wdOutlineLevel1','wdOutlineLevel2','wdOutlineLevel3','wdOutlineLevel4','wdOutlineLevel5','wdOutlineLevel6','wdOutlineLevel7','wdOutlineLevel9','wdOutlineLevelBodyText'])
del df['f12']  #删除第一列
del outlinedf['-']
df = pd.concat([outlinedf,df], axis=1)
# print(df[:10])
'''
对齐方式
'''
aligment = pd.get_dummies(df['f11'])  #将其转换为onehot编码

aligment_array = np.array(aligment)
aligment_array = aligment_array.astype(np.float)
zerodata = np.array([1,0 ,0 ,0 ,0, 0]) #看看是否等于以1开头的数组
for x in range(aligment_array.shape[0]):
    # print(outline_array[0])
    if (aligment_array[x]==zerodata).all():
        aligment_array[x] = np.array(['100']*6)
aligmentdf = pd.DataFrame(aligment_array,columns=['-','wdAlignParagraphCenter','wdAlignParagraphDistribute','wdAlignParagraphJustify','wdAlignParagraphLeft','wdAlignParagraphRight'])
del df['f11']  #删除第一列
del aligmentdf['-']

df = pd.concat([aligmentdf,df], axis=1)


'''
对象
'''
object = pd.get_dummies(df['f10'])  #将其转换为onehot编码

object_array = np.array(object)
object_array = object_array.astype(np.float)
zerodata = np.array([1,0 ,0 ,0 ,0]) #看看是否等于以1开头的数组
for x in range(object_array.shape[0]):
    # print(outline_array[0])
    if (object_array[x]==zerodata).all():
        object_array[x] = np.array(['100']*5)
objectdf = pd.DataFrame(object_array,columns=['-','null2','公式对象','图对象','表对象'])
del df['f10']  #删除第一列
del objectdf['-']
df = pd.concat([objectdf,df], axis=1)


'''
关键字位置
'''
objectsite = pd.get_dummies(df['f9'])  #将其转换为onehot编码
# print(objectsite)
objectsite_array = np.array(objectsite)
objectsite_array = objectsite_array.astype(np.float)
zerodata = np.array([1,0 ,0 ,0]) #看看是否等于以1开头的数组
for x in range(objectsite_array.shape[0]):
    # print(outline_array[0])
    if (objectsite_array[x]==zerodata).all():
        objectsite_array[x] = np.array(['100']*4)
objectsitedf = pd.DataFrame(objectsite_array,columns=['-','null3','段尾','段首'])
del df['f9']  #删除第一列
del objectsitedf['-']
df = pd.concat([objectsitedf,df], axis=1)

'''
数字特征
'''
numfeature = pd.get_dummies(df['f8'])  #将其转换为onehot编码

numfeature_array = np.array(numfeature)
numfeature_array = numfeature_array.astype(np.float)
zerodata = np.array([0,1 ,0 ,0,0 ,0 ,0,0 ,0 ,0,0 ]) #看看是否等于以1开头的数组
for x in range(numfeature_array.shape[0]):
    # print(outline_array[0])
    if (numfeature_array[x]==zerodata).all():
        numfeature_array[x] = np.array(['100']*11)
numfeaturedf = pd.DataFrame(numfeature_array,columns=['-','num1','num2','num3','num4','num5','num6','num7','num8','num9','num10'])
del df['f8']  #删除第一列
del numfeaturedf['-']
df = pd.concat([numfeaturedf,df], axis=1)
# print (df['f8'].unique())
# numfeature = df['f8']
# num_arr = np.array(numfeature)
# for x in range(num_arr.shape[0]):
#    if num_arr[x]=='null':
#          num_arr[x] = '0'
#    elif num_arr[x] == '-':
#          num_arr[x] = '100'
#    elif (num_arr[x]=='1'or num_arr[x]=='2'or num_arr[x]=='3'):
#          num_arr[x] = '1'
#    else:
#        num_arr[x] = '0.5'
# numdf = pd.DataFrame(num_arr,columns=['num'])
# df = pd.concat([numdf,df], axis=1)
# del df['f8']

'''
缩进 todo
'''
suojin = np.array(df['f5'].replace({'-':-1})).astype(np.float)
max = suojin.max()
# max = df['f5'].describe()[max]
for i in range(len(suojin)):
    if suojin[i]!=-1 :
        suojin[i] = (suojin[i])/max
suojindf = pd.DataFrame(suojin,columns={'suojin'})
suojindf = suojindf.replace({-1:'-'})
df = pd.concat([suojindf,df], axis=1)
# print(max)
del df['f5']
# suojin = pd.get_dummies(df['f5'])  #将其转换为onehot编码


labeldic = {"xslw:论文名称":1,"xslw:姓名":2,"xslw:单位":3,"xslw:中文摘要":4,"xslw:中文关键词":5,"xslw:英文摘要":6
            ,"xslw:一级标题":7,"xslw:文本段":8,"xslw:公式":9,"xslw:二级标题":10,"xslw:三级标题":11,"xslw:四级标题":12
            ,"xslw:图片":13,"xslw:图题":14,"xslw:英文关键词":15,"xslw:表题":16,"xslw:表格":17,"xslw:列表":18,"	xslw:参考文献条目":19,"	中文摘要内容_xslw1031":20}
df = df.replace(labeldic)
df = df.replace({'100':'-'})
# df = df.replace({100:'-','-1':1,-1:1})

newindex = ['suojin','f2','null3','段尾','段首','null2','公式对象','图对象','表对象','wdAlignParagraphCenter',
            'wdAlignParagraphDistribute','wdAlignParagraphJustify','wdAlignParagraphLeft','wdAlignParagraphRight','wdOutlineLevel1',
            'wdOutlineLevel2','wdOutlineLevel3','wdOutlineLevel4','wdOutlineLevel5','wdOutlineLevel6','wdOutlineLevel7',
            'wdOutlineLevel9','wdOutlineLevelBodyText','abstract','keywords','null1','关键字','关键词','图','摘要','表','f3','f6','f7','f4',
            'num1','num2','num3','num4','num5',
            'num6','num7','num8','num9','num10','label']
df = df[newindex]
df.to_csv('data/test.csv',index=False,encoding='utf-8')