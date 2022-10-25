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

html = etree.HTML(text)
etree_tostring = etree.tostring(html)
print(etree_tostring)

# 输出:b'<html><body><div> \n  <ul> \n    <li class="item-1">\n      <a href="link1.html">first item</a>\n    </li> \n    <li class="item-1">\n      <a href="link2.html">second item</a>\n    </li> \n    <li class="item-inactive">\n      <a href="link3.html">third item</a>\n    </li> \n    <li class="item-1">\n      <a href="link4.html">fourth item</a>\n    </li> \n    <li class="item-0">\n      a href="link5.html"&gt;fifth item\n  </li></ul> \n</div>\n</body></html>'
print("-------------------------------")
print(etree.tostring(html).decode())
