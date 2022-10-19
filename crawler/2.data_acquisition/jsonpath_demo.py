'''
多层嵌套的字典，我们如何获取最里面的值
'''
from jsonpath import jsonpath

data = {'key1': {'key2': {'key3': {'key4': {'key5': {'key6': 'python'}}}}}}

# 一: 使用最原始的字典获取方案
print(f'使用最原始的字典获取方案: {data["key1"]["key2"]["key3"]["key4"]["key5"]["key6"]}')

# 二: 使用jsonpath的子节点获取
print(f'使用jsonpath的子节点获取:{jsonpath(data,("$.key1.key2.key3.key4.key5.key6"))[0]}')

# 三：使用jsonpath的任意节点获取
print(f'使用jsonpath的任意节点获取:{jsonpath(data,("$..key6"))[0]}')

