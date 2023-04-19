# -*- coding=utf-8 -*-
# 同步mysql的数据 然后插入到另一个表中
import pymysql

# 连接源数据库
origin_conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='ruoyi')

# 创建源数据库游标对象
origin_cursor = origin_conn.cursor()

# 查询 dp_origin_data 表的数据
origin_cursor.execute("SELECT * FROM dp_origin_data")

# 获取查询结果
results = origin_cursor.fetchall()

# 关闭源数据库游标和连接
origin_cursor.close()
origin_conn.close()

# 连接目标数据库
data_conn = pymysql.connect(host='103.36.193.81', port=3306, user='root', password='rbjf_DEV123', db='ruoyi')

# 创建目标数据库游标对象
data_cursor = data_conn.cursor()

# 插入查询结果到 data 表
for result in results:
    data_cursor.execute("INSERT INTO dp_origin_data (uid,data_type,producer_id,site_id,device_id,collect_time,sample_rate,"
                        "sensetivity,trans_factor,data_status,lat,lat_name,lon,lon_name,alt,infra_data) VALUES (%s, %s, %s, %s, %s"
                        ", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", result)

# 提交事务
data_conn.commit()

# 关闭目标数据库游标和连接
data_cursor.close()
data_conn.close()

  # uid,data_type,producer_id,site_id,device_id,collect_time,sample_rate,sensetivity,trans_factor,data_status,lat,lat_name,lon,lon_name,alt,infra_data
