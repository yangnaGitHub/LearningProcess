#JSON(JavaScript Object Notation)轻量级的数据交换格式,基于ECMAScript的一个子集
#json.dumps()对数据进行编码
#json.loads()对数据进行解码
import json
#Python字典类型转换为JSON对象
data = {
    'no' : 1,
    'name' : 'natasha',
    'url' : 'http://www.google.com'
}

json_str = json.dumps(data)
print ("Python原始数据:", repr(data))
print ("JSON对象:", json_str)
data1 = json.loads(json_str)
print ("data2['name']:", data1['name'])
print ("data2['url']:", data1['url'])

#使用json.dump()和json.load()来编码和解码JSON文件数据,
#写入JSON数据
with open('032_json.json', 'w') as f:
    json.dump(data, f)

#读取数据
with open('032_json.json', 'r') as f:
    data = json.load(f)
