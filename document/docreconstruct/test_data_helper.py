#-*-coding:utf8-*-
import pandas as pd
import  numpy as np
label = []
data = []
maxlength = 500#文章最大段落数量
# def getdata():

#     df = pd.read_csv("data/trainForCRF1.csv",names=["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","label"])
#     label = df["label"]
#     print(label.values)
#     del df["label"]
#     data = df.values
#     return data,label
def _Readfile(filepath):
    '''

    :param filepath: 要打开的文件的路径
    :return: 返回的是读取文件每行的迭代器
    '''
    data = []  #训练数据
    eachdata = [] #每一行的训练数据
    label = []   #标签数据
    eachlabel = [] #每一行的标签数据
    with open(filepath,'r',encoding='utf-8') as network_file:  #打开文件
        documentnum=0   #文档的篇数
        each_paragraph =0 #每一篇的段落数量，取前200段
        for line in network_file.readlines():     #按行读取
            each_paragraph = each_paragraph+1
            # print (line)
            line=' '.join(line).replace(' ','').replace('\t',' ')   ##每个段落的长度
            line_columns = line.strip().split(',') #按制表符分割
            # print(len(line_columns))
            # line_columns = line.strip().split(' ')
            if line_columns!="":
                if line_columns[0]=='-':   #按-分割每篇文章
                     # print (documentnum)
                     documentnum = documentnum+1
                     data.append(eachdata)   #合并每篇文章的特征向量
                     label.append(eachlabel)  #合并每篇文章的标签
                     eachdata = []
                     eachlabel = []
                     each_paragraph = 0
                else:
                    if each_paragraph<maxlength:
                        try:
                            line_columns =[float(i) for i in line_columns]  #将文档的string类型转化为float
                            eachdata.append(line_columns[:])  #前n个数据为特征
                        except:
                            print("该列转成float时候有错误，请注意修改")
                            print(line_columns)
                    else:
                        pass


    # te = [y for x in data for y in x]
    # a1 = [y for x in te for y in x]
    # print (a1)
    return data,documentnum
def bullet(data_1):
    bullet_data =[]
    for line1 in data_1:
        # train_data.remove(line1)
        x = list(line1)
        if len(x)>0:
            for i in range(maxlength-len(line1)):
                # line1 = np.row_stack((line1,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
                #对每一个都补全为最大-1
                x.append([0.0]*len(x[0]))
            bullet_data.append(x)
    return bullet_data

def bullet_label(data_1):
    bullet_data = []
    for x in data_1:
        # train_data.remove(line1)
        x1 = list(x)
        for i in range(0, maxlength - len(x)):
           x1.append(0)
        bullet_data.append(x1)
    return bullet_data
def get_data(trainpath):
    train_data,train_document_num = _Readfile(trainpath)
    trian_data = np.array(bullet(train_data))
    return trian_data,train_document_num
def get_2ddata():   #将所有的数据拼接成二维向量，用来做embedding的实验
     df = pd.read_table("data\\noseqtrain.txt",names=['f1','f2','f3','f4','f5','f6','f7','f8','label'])
     df.dropna(axis=0,how='all')
     y_data = df['label'].values
     del df['label']
     x_data = df.values
     return  x_data,y_data