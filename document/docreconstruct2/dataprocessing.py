#coding=utf-8
import pandas as pd
import  numpy as np
import csv
from  sklearn.preprocessing import MinMaxScaler
import regex as re
def clean_value_change(x):
    if (x!='null') & ('.' in str(x)):
#         x = '长度'+str(len(str(x).split('.')))
        x = '长度'+str(len(str(x).split('.')))
    elif (x!='null') &((')' in str(x))|('）' in str(x))|('（' in str(x))|(']' in str(x))):
        x =  '括号'
    r1 = re.compile(u'[0-9][、|.|,|．|，]')
    r2 = re.compile(u'[④|①|②|③|⑤|⑦|△|⑥]')
    r3 = re.compile(u'[一|二|三|四|五|六|第]')
#     r4 = re.compile(u'[|二|三|四|五|六|第]')
    try:
        if(len(r1.findall(x))!=0):
            return '数字+符号'
        elif(len(r2.findall(x))!=0):
            return '罗马符号'
        elif(len(r3.findall(x))!=0):
            return '一级'
        else:
            return x
    except:
            return x
def clean_x_null(x):
    if(x=='-'):
        return x
    r1 = re.compile(u'[数字|括号|长度|一级|罗马符号|六|第]')
    try:
        if(len(r1.findall(x))!=0):
                return x
        else:
                return 'null'
    except:
        pass
def clean_big_data(x):
    try:
          if (float(x)>10):
              return 'null'
          else :
               return '数字1'
    except:
          return x
def diclist(filepath):
    dics = { line.strip().split(':')[0]: line.strip().split(':')[1] for line in open(filepath, 'r', encoding='utf8').readlines()}
    return dics
def suojin_noramal(x):
    if(x=='-'):
        return x
    try:
        if(float(x)<0):
                return -1
        elif(float(x)>0):
                return 1
        else:
            return 0
    except:
        pass
def font_size_normal(df):
    data1 = np.array(df['字号'])
    everyfont = [] #每一篇文章的字号集合
    onehotfont = []
    fontdata = []
    index_null =0
    for font in data1:  #每篇文档的字号减去正文字号，然后求标准化
        index_null +=1
        if (font!='-'):
            everyfont.append(float(font))
        elif len(everyfont)!=0:
            common_value = max(everyfont,key=everyfont.count)
            dataminusfont = [everyfontx-common_value for everyfontx in everyfont] #减去正文字体
            dataminusfont = np.array(dataminusfont)
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
    df['字号'] = pd.Series(fontdata)
def font_normal(df):
    fontname = df['字体']
    begin = 0
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
    del df['字体']
    df['字体'] = fontname
def No_normal(df):
    df['编号'] = df['编号'].map(lambda x: clean_big_data(x))
    df['编号'] = df['编号'].map(lambda x: clean_value_change(x))
    df['编号'] = df['编号'].map(lambda x: clean_x_null(x))
    return  df

def datanormal(datapath,resultpath,step):
    df = pd.read_table(datapath,sep='\t',quoting=csv.QUOTE_NONE,encoding='utf-8')
    print(df.loc[df['字号'].isnull()])
    df['缩进'] = df['缩进'].map(lambda x:suojin_noramal(x))
    df = No_normal(df)
    df = df.replace({'9999999':0})
    font_size_normal(df)
    print(df.columns)
    dics = diclist('./data/dic/valuedic.txt')
    df = df.replace(dics)
    if step =='test':
        del df['段前距'],df['段后距'],df['行距']
    else:
        del df['段前距'],df['段后距'],df['行距'],df['文章名称'],df['文本内容']
    df = df.replace({'100':'-',100:'-',"文本段落":"文本段"})
    dic ={'中文摘要': 1, '中文关键词': 2, '英文摘要': 3, '英文关键词': 4, '一级标题': 5, '二级标题': 6, '文本段': 7, '三级标题': 8, '图片': 9, '图题': 10, '表题': 11, '表格': 12, '四级标题': 13, '程序代码': 14, '五级标题': 15, '公式': 16, '论文名称': 17, '姓名': 18, '单位': 19, '邮箱': 20}
    # dic ={'中文摘要': 1, '中文关键词': 2, '英文摘要': 3, '英文关键词': 4, '一级标题': 5, '二级标题': 5, '文本段': 6, '三级标题': 5, '图片': 7, '图题': 8, '表题': 9, '表格': 10, '四级标题': 5, '程序代码': 11, '五级标题': 5, '公式': 12, '论文名称': 13, '姓名': 14, '单位': 15, '邮箱': 16}
    df = df.replace(dic)
    df.to_csv(resultpath,index=False,encoding='utf-8')

if __name__ == '__main__':
    '''
    训练数据处理
    '''
    datapath = './data/traindata.txt'
    resultpath = 'data/train.csv'
    datanormal(datapath,resultpath,'train')
    '''
    测试数据处理
    '''
    # datapath = './data/test.txt'
    # resultpath = 'data/test.csv'
    # datanormal(datapath,resultpath,'test')