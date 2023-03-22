import base64
import json
import requests
import xlrd

data_template = {
    "deleted": "false",
    "entity_id": "",
    "entity_name": "",
    "entity_type": "GJBKM_TERM",
    "last_update": 1672738230001,
    "props": {
        "GJBKM_TERM": {
            "term_name": "",
        }
    },
    "source_count": 0
}


def construct_data(id, term_name):
    data_template['entity_id'] = id
    data_template['entity_name'] = term_name
    data_template['props']['GJBKM_TERM']['term_name'] = term_name
    return data_template


base_url = 'http://192.168.100.7:9201'
username = ""
password = ""

workbook = xlrd.open_workbook(r'./GJB_V5.xlsx')
sheets_ = workbook.sheets()[2]
# 定义空列表，存储Excel数据
tables = []


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


def import_excel(excel):
    for rown in range(excel.nrows):
        print(rown)
        if rown == 0:
            continue
        array = {'id': int(sheets_.cell_value(rown, 0)), 'term_name': sheets_.cell_value(rown, 1)}
        tables.append(array)


if __name__ == '__main__':
    # 读取excel数据
    print(sheets_.name)
    import_excel(sheets_)
    for i in tables:
        # 数据写入es
        try:
            print(i)
           # print(i['standard_no'])
            data = construct_data(i['id'], i['time'])
            putIndex('jk_v1_graph_entity', i['id'], data)
        except Exception as ex:
            print(ex)
            pass