'''
es模板创建：读物文件夹下面的模板文件，然后进行模板文件创建：
注意：1、需要更改加载的文件夹目录
     2、需要更改es数据源信息：base_url、username、password

@author: yexinming
@date 2022/03/01
'''

import base64
import json
import os
import sys

import requests
# es的连接配置
base_url = 'http://xxxx:9200'
username = "elastic"
password = "Gtcom2021!"


def getAuthorization():
    user_info_str = username + ":" + password
    user_info = base64.b64encode(user_info_str.encode())  # 这个得到是个字节类型的数据
    headers = {
        "Authorization": "Basic {0}".format(user_info.decode())  # 这个就是需要验证的信息
    }
    return headers


def putTemplate(templateName, templateDslJson):
    url = base_url + '/_template/{0}'.format(templateName)
    print(f'{templateName} 索引模板正在迁移中 url:{url}')
    res = requests.put(url, json=templateDslJson, headers=getAuthorization())
    print(res.status_code)
    print(res.content)


def loadDir(fil_dir):
    L = []
    for root, dirs, files in os.walk(fil_dir):
        print(root) # 当前目录路径
        print(dirs) # 当前目录下所有子目录
        print(files) # 当前所有非目录子文件
        for file in files:
            print(file)
        return files


def loadTemplateDslJson(dir_name, file_name):
    with open(dir_name+'/'+file_name, 'r') as f:
        t = json.load(f)
        print(t)
        return t


if __name__ == '__main__':
    dir_name = './新版本测试mapping/news'
    files = loadDir(dir_name)
    for file in files:
        jsonTemplate = loadTemplateDslJson(dir_name, file)
        print(jsonTemplate)
        if isinstance(jsonTemplate, dict):
            for templateName in jsonTemplate:
                print(f'templateName: {templateName}')
                templateDslJson = jsonTemplate[templateName]
                print(f'templateJson: {templateDslJson}')
                putTemplate(templateName, templateDslJson)


