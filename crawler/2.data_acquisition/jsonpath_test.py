from jsonpath import jsonpath
import json
'''
解析获取：
1、解析book_dict并获取里面的各个书籍的价格：price。
2、获取自行车的颜色。
'''

book_str = '''{
  "store": {
    "book": [
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}'''

book_dict = json.loads(book_str)
# 1、解析book_dict并获取里面的各个书籍的价格：price。

print(f'解析book_dict并获取里面的各个书籍的价格:{jsonpath(book_dict,"$..price")}')
# 2、获取自行车的颜色,由于颜色color是单一的属性
print(f'获取自行车的颜色:{jsonpath(book_dict,"$..color")}')

