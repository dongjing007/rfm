import time
import numpy as np
import pandas as pd

# 导入数据
df_raw = pd.DataFrame(pd.read_excel('rfm.csv',index_col='USERID'))

# 缺失值处理
sales_data = df_raw.dropna() # 丢失带有缺失值NA的行记录
sales_data = sales_data[sales_data['AMOUNTINFO'] > 1] # 丢弃订单金额<=1的记录 


# # 方差、标准差
# print('Data DESC')
# print(df_raw.describe())
# print('-' * 30)

# 数据转换 (按用户id去重归总)
recency_value = sales_data['ORDERDATE'].groupby(sales_data.index).max() #计算最近一次订单时间
frequency_value = sales_data['ORDERDATE'].groupby(sales_data.index).count() #计算订单频率
monetary_value = sales_data['AMOUNTINFO'].groupby(sales_data.index).sum() #计算订单总金额

# 方差、标准差
# print('Data DESC')
# print(monetary_value)
# print('-' * 30)

# 分别计算R,F,M得分
deadline_date = pd.datetime(2019, 5,1) #指定一个时间节点，用来计算其他时间和改时间的距离
r_interval = (deadline_date - recency_value).dt.days #计算r间隔
r_score = pd.cut(r_interval, 5, labels=['5','4','3','2','1']) # 计算r得分 五分位倒序
f_score = pd.cut(frequency_value, 5, labels=[1,2,3,4,5]) # 计算f得分
m_score = pd.cut(monetary_value, 5, labels=[1,2,3,4,5]) # 计算m得分

# R,F,M数据合并
rfm_list = [r_score, f_score, m_score] # 将R,F,M三个维度组成列表
rfm_cols = ['r_score', 'f_score', 'm_score'] # 设置R,F,M三个维度的列名
rfm_pd = pd.DataFrame(np.array(rfm_list).transpose(),
                      columns=rfm_cols, index=frequency_value.index) #建立R,F,M数据框

# 策略1：加权得分 定义用户价值
# rfm_pd['rfm_wscore'] = rfm_pd['r_score']*0.25 + rfm_pd['f_score']*0.25 + rfm_pd['m_score']*0.5

# 策略2：RFM组合 直接输出三维度值
rfm_pd_tmp = rfm_pd.copy()
rfm_pd_tmp['r_score'] = rfm_pd_tmp['r_score'].astype('str')
rfm_pd_tmp['f_score'] = rfm_pd_tmp['f_score'].astype('str')
rfm_pd_tmp['m_score'] = rfm_pd_tmp['m_score'].astype('str')
rfm_pd['rfm_comb'] = rfm_pd_tmp['r_score'].str.cat(rfm_pd_tmp['f_score']).str.cat(rfm_pd_tmp['m_score'])

# 导出数据
rfm_pd.to_csv('sales_rfm_score.csv')