import base64
import json
import requests
import xlrd

data_template = {
    "deleted": "false",
    "entity_id": "",
    "entity_name": "",
    "time": 0,
    "entity_type": "GJBKM_STANDARD",
    "last_update": 1672738230000,
    "props": {
        "GJBKM_STANDARD": {
            "standard_abbreviate": "",
            "standard_en_name": "",
            "standard_name": "",
            "standard_no": "",
            "standard_principle": "",
            "standard_revise": "",
            "standard_status": "",
            "standard_sumary": "",
            "standard_type": "",
            "standrad_category_no1": "",
            "standrad_category_no2": "",
            "standrad_category_no3": "",
            "standrad_secret_level": "",
            "standrad_version": ""
        }
    },
    "source_count": 0
}


def construct_data(id, standard_no, standard_name):
    data_template['entity_id'] = id
    data_template['entity_name'] = standard_name
    data_template['props']['GJBKM_STANDARD']['standard_no'] = standard_no
    return data_template


base_url = 'http://192.168.100.7:9201'
username = ""
password = ""

workbook = xlrd.open_workbook(r'./GJB_V4.xlsx')
sheets_ = workbook.sheets()[7]
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
        array = {'id': int(sheets_.cell_value(rown, 1)), 'standard_no': sheets_.cell_value(rown, 2), 'standard_name': '标准'+sheets_.cell_value(rown, 3)}
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
           data = construct_data(i['id'], i['standard_no'], i['standard_name'])
           putIndex('jk_v1_graph_entity', i['id'], data)
        except Exception as ex:
            print(ex)
            pass
