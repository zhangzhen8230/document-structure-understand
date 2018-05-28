#-*-coding:utf8-*-
import pandas as pd
import  numpy as np
label = []
data = []
doc_id = []
maxlength = 500#文章最大段落数量
# def getdata():


def _Readfile(filepath):
    '''

    :param filepath: 要打开的文件的路径
    :return: 返回的是读取文件每行的迭代器
    '''
    data = []  #训练数据
    eachdata = [] #每一行的训练数据
    doc_id = []
    label = []   #标签数据
    eachlabel = [] #每一行的标签数据
    each_doc_id = [] #每一行的doc2vecid
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
                     doc_id.append(each_doc_id)
                     eachdata = []
                     eachlabel = []
                     each_doc_id = []
                     each_paragraph = 0
                else:
                    if each_paragraph<maxlength:
                        try:
                            eachlabel.append((line_columns[-1])) #最后一个数据为label
                            each_doc_id.append(line_columns[-2])
                            line_columns =[float(i) for i in line_columns[:-2]]  #将文档的string类型转化为float
                            eachdata.append(line_columns[:])  #前n个数据为特征
                        except:
                            print("该列转成float时候有错误，请注意修改")
                            print(line_columns)
                    else:
                        pass


    # te = [y for x in data for y in x]
    # a1 = [y for x in te for y in x]
    # print (a1)
    return data,label,documentnum,doc_id
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
        x1 = list(x)
        for i in range(0, maxlength - len(x)):
           x1.append(0)
        bullet_data.append(x1)
    return bullet_data
def bullet_doc2id(data_1):
    bullet_data = []
    for x in data_1:
        x1 = list(x)
        for i in range(0, maxlength - len(x)):
           x1.append(-1)
        bullet_data.append(x1)
    return bullet_data
def get_data(trainpath,testpath):
    train_data,train_label,train_document_num,train_doc2id = _Readfile(trainpath)
    trian_data = np.array(bullet(train_data))
    train_label = np.array(bullet_label(train_label))
    train_doc2id  = np.array(bullet_doc2id(train_doc2id))
    test_data,test_label,test_document_num,test_doc2id = _Readfile(testpath)
    test_data = np.array(bullet(test_data))
    test_label = np.array(bullet_label(test_label))
    test_doc2id  = np.array(bullet_doc2id(test_doc2id))
    print(len(test_doc2id))
    return trian_data,train_label,train_doc2id,test_data,test_label,test_doc2id,train_document_num,test_document_num
if __name__ == '__main__':
    data,label,train_doc2id,test_data,test_label,test_doc2id,train_document_num,test_document_num = get_data("input/train.csv","input/test.csv")
