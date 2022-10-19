'''
获取requests请求返回的数据，然后解析获取里面的以A开头的城市名跟所有城市名
'''

import requests
import json
from jsonpath import jsonpath

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

response = requests.get('https://www.lagou.com/lbs/getAllCitySearchLabels.json', headers=headers)
# 返回的response是字符串形式，json在python3时候会直接将response.content解析成字符串

dict = json.loads(response.content)
# 1.然后解析获取里面的以A开头的城市名
print(jsonpath(dict, '$..A..name'))
# 2.然后解析获取里面的所有城市名
print(jsonpath(dict, '$..name'))
