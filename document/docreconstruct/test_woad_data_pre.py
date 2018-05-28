#coding=utf-8
'''
预处理未标注的word数据
'''
#coding=utf-8
import pandas as pd
import  numpy as np
from sklearn import preprocessing
from  sklearn.preprocessing import MinMaxScaler

##将特征转换为数字
def test_ch_csv():
    df = pd.read_table('data/test.txt',sep='\t',names=["等号","关键字","字体","字号","字形","字数","颜色","编号","编号位置","word对象","行距","缩进",
                                                       "段前距","段后距","对齐方式","大纲级别","标点","中文比例"])
    df = df.replace({'9999999':0})
    dftest = df
    print(df[0:3])
    # dftest = df[~df.f0.isin(["-"])]
    keyword_list = dftest['关键字'].tolist()
    equals_list =  dftest["等号"].tolist()
    wdline_list = dftest["大纲级别"].tolist()
    identifier_list = dftest["编号"].tolist()
    pun_list = dftest["标点"].tolist()
    aliment_list = dftest["对齐方式"].tolist()
    wordobject_list = dftest["word对象"].tolist()
    identifiersite_list = dftest["编号位置"].tolist()
    ##处理后的特征
    dic =['关键字_abstract', '关键字_keywords', '关键字_null', '关键字_关键字', '关键字_关键词',
           '关键字_图', '关键字_摘　要', '关键字_摘要', '关键字_表', '等号_False', '等号_True',
           '对齐方式_wdAlignParagraphCenter', '对齐方式_wdAlignParagraphDistribute',
           '对齐方式_wdAlignParagraphJustify', '对齐方式_wdAlignParagraphLeft',
           '对齐方式_wdAlignParagraphRight', '大纲级别_wdOutlineLevel1',
           '大纲级别_wdOutlineLevel2', '大纲级别_wdOutlineLevel3', '大纲级别_wdOutlineLevel4',
           '大纲级别_wdOutlineLevel5', '大纲级别_wdOutlineLevel6', '大纲级别_wdOutlineLevel7',
           '大纲级别_wdOutlineLevel8', '大纲级别_wdOutlineLevel9',
           '大纲级别_wdOutlineLevelBodyText', '编号_(1)', '编号_(1-1)', '编号_(1.1)', '编号_1',
           '编号_1)', '编号_1）', '编号_2', '编号_3', '编号_4', '编号_5', '编号_null', '编号_（1-1）',
           '编号_（1.1）', '编号_（1—1）', '编号_（1）', 'word对象_null', 'word对象_公式对象',
           'word对象_图对象', 'word对象_表对象', '编号位置_null', '编号位置_段尾', '编号位置_段首',
           '标点_False', '标点_True', '字形', '字数', '中文比例', '字号', '字体']

    ##将特征名称进行划分
    keyword_dic = []
    equals_dic = []
    aligment_dic = []
    wdline_dic =[]
    identifier_dic = []
    identifiersite_dic = []
    wordobject_dic =[]
    pun_dic = []

    for x in dic:
        x_pre = x.split('_')[0]
        if(x_pre=="关键字"):
            keyword_dic.append(x)
        elif x_pre=="等号":
            equals_dic.append(x)
        elif x_pre=="对齐方式":
            aligment_dic.append(x)
        elif x_pre=="大纲级别":
            wdline_dic.append(x)
        elif x_pre=="编号":
            identifier_dic.append(x)
        elif x_pre=="编号位置":
            identifiersite_dic.append(x)
        elif x_pre=="标点":
            pun_dic.append(x)
        elif x_pre=="word对象":
            wordobject_dic.append(x)
    def testTooneHot(list,dic,pre):
           onehot = np.zeros((len(list),len(dic)))
           for index1,value in enumerate(list):
                  value = pre+"_"+value
                  if value in dic:
                         index2 = dic.index(value)
                         onehot[index1][index2] = 1

                  else:
                      onehot[index1][:] = 100
           return onehot
    keyword_number =  testTooneHot(keyword_list,keyword_dic,"关键字")
    keyword_df = pd.DataFrame(keyword_number,columns=keyword_dic)
    f4_number =  testTooneHot(equals_list,equals_dic,"等号")
    equals_df = pd.DataFrame(f4_number,columns=equals_dic)
    f5_number =  testTooneHot(wdline_list,wdline_dic,"大纲级别")
    wdline_df = pd.DataFrame(f5_number,columns=wdline_dic)
    f6_number =  testTooneHot(pun_list,pun_dic,"标点")
    pun_df = pd.DataFrame(f6_number,columns=pun_dic)
    f11_number =  testTooneHot(aliment_list,aligment_dic,"对齐方式")
    aligment_df = pd.DataFrame(f11_number,columns=aligment_dic)
    f12_number =  testTooneHot(wordobject_list,wordobject_dic,"word对象")
    wordobject_df = pd.DataFrame(f12_number,columns=wordobject_dic)
    f13_number =  testTooneHot(identifiersite_list,identifiersite_dic,"编号位置")
    identifiersite_df = pd.DataFrame(f13_number,columns=identifiersite_dic)
    f14_number =  testTooneHot(identifier_list,identifier_dic,"编号")
    identifier_df = pd.DataFrame(f14_number,columns=identifier_dic)
    print(identifier_df)
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
            # count = np.bincount(everyfont)   #将出现次数最多的字体认为是正文
            # common_value = np.argmax(count)
            # print(common_value)
            common_value = max(everyfont,key=everyfont.count)
            # print(common_value)
            dataminusfont = [everyfontx-common_value for everyfontx in everyfont] #减去正文字体
            dataminusfont = np.array(dataminusfont)
            # print(dataminusfont)
            datafontlast = MinMaxScaler().fit_transform(dataminusfont.reshape(-1,1)) #调用sklearn库进行标准化
            # print(dataminusfont)
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
    '''
    对于字体，求频率
    '''
    fontname = df['字体']
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
    del df['字体']

    df.drop(labels=['字号','关键字','对齐方式','大纲级别','编号','编号位置','标点',"word对象","缩进",'段前距','段后距',"等号","行距","颜色"], axis=1,inplace = True)
    df['字号'] = pd.Series(fontdata)
    df['字体'] = fontname
    df = pd.concat([pun_df,df], axis=1)
    df = pd.concat([identifiersite_df,df], axis=1)
    df = pd.concat([wordobject_df,df], axis=1)
    df = pd.concat([identifier_df,df], axis=1)
    df = pd.concat([wdline_df,df], axis=1)
    df = pd.concat([aligment_df,df], axis=1)
    df = pd.concat([equals_df,df], axis=1)
    df = pd.concat([keyword_df,df], axis=1)
    df = df.replace({'100':'-',100:'-',"文本段落":"文本段"})
    df.to_csv('data/testdata.csv',index=False,header=False,encoding='utf-8')