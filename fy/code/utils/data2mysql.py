#! /usr/bin/env python
# -*- coding=utf-8 -*-
# mysql连接 然后读取文件 写入到数据库
import pymysql
import re

# 创建MySQL连接
# cnx = mysql.connector.connect(**config)
with open("./testWvfrm.txt", 'r') as f:
    data = f.readlines()

# print(data)
# 将每行数据拆分为列表，并获取第一个元素组成新的列表
pattern = re.compile(r' {2,3}')  # 使用正则表达式进行拆分
first_column = [re.split(pattern, line)[5] for line in data]

result = '['
# 将列表中的所有元素拼接成一个字符串
result += ','.join(first_column)
result += ']'

print(result)
pymysql.connect()
# 连接 MySQL 数据库
conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='ruoyi')

# 创建游标对象
cursor = conn.cursor()

# 定义更新语句
update_query = "UPDATE dp_origin_data SET infra_data = %s WHERE uid = %s"

# 执行更新语句
cursor.execute(update_query, (result, '2222222'))

# 提交事务
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()


'''
# 打开文件并读取内容
with open('testWvfrm.txt', 'r') as f:
    content = f.read()

# 拼接字符串
text = 'Some additional text: ' + content

# 创建游标对象
cursor = cnx.cursor()

# 执行INSERT语句将拼接的字符串写入MySQL数据库中的data表的text字段中
insert_stmt = ("INSERT INTO data (text) VALUES (%s)")
data = (text,)
cursor.execute(insert_stmt, data)

# 提交事务并关闭连接
cnx.commit()
cursor.close()
cnx.close()
'''
