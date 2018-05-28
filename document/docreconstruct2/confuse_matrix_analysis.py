import pandas as pd
from sklearn.metrics import classification_report
all_df = pd.read_csv('data/result.csv',encoding='gbk')
conf_mat = classification_report(all_df['实际'].values, all_df['预测'].values,digits=4)
print(conf_mat)