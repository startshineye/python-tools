from lxml import etree

text = ''' 
<div> 
  <ul> 
    <li class="item-1">
      <a href="link1.html">first item</a>
    </li> 
    <li class="item-1">
      <a href="link2.html">second item</a>
    </li> 
    <li class="item-inactive">
      <a href="link3.html">third item</a>
    </li> 
    <li class="item-1">
      <a href="link4.html">fourth item</a>
    </li> 
    <li class="item-0">
      a href="link5.html">fifth item</a>
  </ul> 
</div>
'''

# 创建element对象
html = etree.HTML(text)

# 1. 获取link1.html的a的内容:我们用修饰语句，修饰a标签，其属性href为link1.html,然后获取标签的文本内容；返回的是一个数组
link1_text = html.xpath('//a[@href="link1.html"]/text()')
print(link1_text)  # 输出:['first item']
print(link1_text[0])  # 输出:first item

# 2. 获取所有a标签的内容:text
link_text = html.xpath('//a/text()')
print(link_text)  # 输出:['first item', 'second item', 'third item', 'fourth item']

# 3. 获取所有a标签的属性href的内容
link_href = html.xpath('//a/@href')
print(link_href)  # 输出:['link1.html', 'link2.html', 'link3.html', 'link4.html']

# 4.如何将上面两个数据的对应数组匹配呢? 比如:link1.html对应的是first item
# 思路：将link_text数组遍历 获取其数组下标，然后根据下标从link_href获取数据即可

for text in link_text:
    inx = link_text.index(text)
    print(link_href[inx], text)

print("-----------------------------")
# 4.上面这种做法比较low；用zip方法：代表以相同的索引遍历多个列表；但是这种方法的话，如果有一个a的text缺失时候会混乱
for text, href in zip(link_text, link_href):
    print(href, text)

# 4.还有一种方法是：先获取所有的a，然后我们遍历所有的a；
print("-----------------------------")
a_list = html.xpath('//a')
# print(a_list)
for a in a_list:
    print(a.xpath('./@href')[0], a.xpath('./text()')[0]) # 输出:link1.html first item
    print(a.xpath('.//@href')[0], a.xpath('.//text()')[0])  # 输出:link1.html first item
    print(a.xpath('.//@href')[0], a.xpath('text()')[0])  # 输出:link1.html first item
