import base64
import json
import requests
import xlrd
import uuid

entity_type_dict = {'1': 'GJBKM_STANDARD',
                    '2': 'GJBKM_ORGANIZATION',
                    '3': 'GJBKM_TERM',
                    '4': 'GJBKM_TIME',
                    '5': 'GJBKM_PERSON',
                    '6': 'GJBKM_LAW'
                    }

relation_code_dict = {'文献关联关系': 'GJBKM_quote',
                    '发布时间': 'GJBKM_pubTime',
                    '实施时间': 'GJBKM_implementeTime',
                    '批准时间': 'GJBKM_approvaTime',
                    '起草': 'GJBKM_draft',
                    '制定': 'GJBKM_layDown',
                    '发布': 'GJBKM_publish',
                    '解释': 'GJBKM_explain',
                    '归口': 'GJBKM_putUnder',
                    '提出': 'GJBKM_putForward',
                    '文献作者': 'GJBKM_drafter',
                    '拥有': 'GJBKM_possess',
                    '执行依据': 'GJBKM_enforcementBasis',
                    '代替': 'GJBKM_replace',
                    '被替代': 'GJBKM_replaced',
                    '历史标准': 'GJBKM_history_standard'
                    }


def get_entity_type(entity_id):
    s = str(entity_id)
    return entity_type_dict[s[0]]


def get_relation_code(relation_name):
    return relation_code_dict[relation_name]


data_template = {
    "source_count": 1,
    "pub_time_max": 1618228700515,
    "priority_level": 0,
    "props": {
        "status": 0
    },
    "pub_time_min": 1618228700515,
    "deleted": "false",
    "entities": [
        {
            "is_start": True,
            "entity_type": "",
            "entity_name": "",
            "is_end": False,
            "entity_id": ""
        },
        {
            "is_start": False,
            "entity_type": "",
            "entity_name": "",
            "is_end": True,
            "entity_id": ""
        }
    ],
    "user_id": 116,
    "last_update": 1618228700515,
    "relation_name": "",
    "relation_code": "",
    "relation_id": "",
}


def construct_data(relation_id, s_entity_id, s_entity_name, relation_name, e_entity_id, e_entity_name):
    data_template['relation_id'] = relation_id
    data_template['relation_name'] = relation_name
    data_template['relation_code'] = get_relation_code(relation_name)
    data_template['entities'][0]['entity_type'] = get_entity_type(s_entity_id)
    data_template['entities'][0]['entity_name'] = s_entity_name
    data_template['entities'][0]['entity_id'] = s_entity_id

    data_template['entities'][1]['entity_type'] = get_entity_type(e_entity_id)
    data_template['entities'][1]['entity_name'] = e_entity_name
    data_template['entities'][1]['entity_id'] = e_entity_id
    return data_template


base_url = 'http://192.168.100.7:9201'
username = ""
password = ""

workbook = xlrd.open_workbook(r'./GJB_V6.xlsx')
sheets_ = workbook.sheets()[9]
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
        array = {'relation_id': int(sheets_.cell_value(rown, 0)), 'relation_name': sheets_.cell_value(rown, 3),
                 's_entity_id': int(sheets_.cell_value(rown, 1)), 's_entity_name': sheets_.cell_value(rown, 2),
                 'e_entity_id': int(sheets_.cell_value(rown, 4)), 'e_entity_name': sheets_.cell_value(rown, 5)
                 }
        tables.append(array)


if __name__ == '__main__':
    # 读取excel数据
    print(sheets_.name)
    import_excel(sheets_)
    for i in tables:
        # 数据写入es
        try:
            # print(i['standard_no'])
            data = construct_data(i['relation_id'], i['s_entity_id'], i['s_entity_name'],
                                  i['relation_name'], i['e_entity_id'], i['e_entity_name'])
            uuid_ = uuid.uuid1()
            uuid__hex = uuid_.hex
            print(f'data :{data}')
            putIndex('jk_v1_graph_relation', uuid__hex, data)
        except Exception as ex:
            print(ex)
            pass
