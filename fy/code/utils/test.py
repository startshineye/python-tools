import re

# 定义一个大小为10x10的二维数组
my_array = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
    [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
    [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
    [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
    [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
    [91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
]

# 获取第一列并拼接成一个以逗号隔开的字符串
first_column = [row[0] for row in my_array]
print(first_column)
result = ','.join(map(str, first_column))

print(result)

ar = [1, 2, 3, 4, 5]

print(f'type(ar):{type(ar)}')

with open("./testWvfrm.txt", 'r') as f:
    data = f.readlines()

# print(data)
# 将每行数据拆分为列表，并获取第一个元素组成新的列表
pattern = re.compile(r' {2,3}')  # 使用正则表达式进行拆分
first_column = [re.split(pattern, line)[1] for line in data]

print(type(first_column))
print(len(first_column))
