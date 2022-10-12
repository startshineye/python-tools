'''
实现将输入的中英文句子：进行中英互译
'''
import json
import requests


def parse_data(data):
    # 将json数据转换成python字典
    dict = json.loads(data)
    # 从json中获取结果
    print(dict['content']['out'])


class Translator(object):
    def __init__(self, word):
        self.url = "http://ifanyi.iciba.com/index.php?c=trans&m=fy&client=6&auth_user=key_web_fanyi&sign=2ad53c323affb5ad"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }
        self.data = {
            "from": "zh",
            "to": "en",
            "q": word
        }

    def get_data(self):
        response = requests.post(self.url, self.data, headers=self.headers)
        # 默认返回bytes类型，除非确定外部调用使用str才进行解码操作
        print(response.content)
        return response.content

    def run(self):
        # url
        # headers
        # post——data
        # requests请求
        # 解析
        content = self.get_data()
        parse_data(content)


if __name__ == "__main__":
    # 一次性使用
    # translator = Translator("中国")
    # translator.run()

    # input 输入
    s = input("请输入需要翻译的文字:")
    translator = Translator(s)
    translator.run()
