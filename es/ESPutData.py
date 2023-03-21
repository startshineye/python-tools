'''
es插入数据：读物文件夹下面文件，然后按照行读取解析数据，然后将数据插入到es索引：
注意：1、需要更改加载的文件夹目录
     2、需要更改es数据源信息：base_url、username、password

@author yexinming
@date 2022/12/27
'''

import base64
import json
import requests

base_url = 'http://192.168.100.6:9200'
username = ""
password = ""


def getAuthorization():
    user_info_str = username + ":" + password
    user_info = base64.b64encode(user_info_str.encode())  # 这个得到是个字节类型的数据
    headers = {
        "Authorization": "Basic {0}".format(user_info.decode())  # 这个就是需要验证的信息
    }
    return headers


def parseData():
    print('parseData')


def putIndex(index_name, id, data_json):
    url = base_url + '/{0}/_doc/{1}'.format(index_name, id)
    print(f'index: {index_name} id:{id} 正在插入数据')
    res = requests.put(url, json=data_json)
    print(res.status_code)
    print(res.content)


if __name__ == '__main__':
    file_name = '/Users/xiexinming/code/jk-data-mining/es/outernet/locationslib.json'
    with open(file_name, encoding='utf-8') as fp:
        for i, line in enumerate(fp):
            try:
                data = json.loads(line.strip())
                putIndex(data['_index'],  data['_id'], data['_source'])
            except Exception as ex:
                print(ex)
                pass
