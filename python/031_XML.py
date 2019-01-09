#XML指可扩展标记语言,标准通用标记语言的子集,用于标记电子文件使其具有结构性的标记语言
#XML被设计用来传输和存储数据,一套定义语义标记的规则,这些标记将文档分成许多部件并对这些部件加以标识
#XML编程接口有DOM和SAX
#三种方法解析XML,SAX,DOM,以及ElementTree
#SAX解析器,SAX用事件驱动模型,在解析XML的过程中触发一个个的事件并调用用户定义的回调函数来处理XML文件
#DOM:XML数据在内存中解析成一个树,通过对树的操作来操作XML

#SAX是一种基于事件驱动的API(解析器和事件处理器)
#解析器负责读取XML文档,并向事件处理器发送事件
#事件处理器则负责对事件作出相应处理
#使用sax方式处理xml要先引入xml.sax中的parse函数,还有xml.sax.handler中的ContentHandler
#startDocument()方法
#文档启动的时候调用
#endDocument()方法
#解析器到达文档结尾时调用
#startElement(name,attrs)方法
#遇到XML开始标签时调用,name是标签的名字,attrs是标签的属性值字典
#endElement(name)方法
#遇到XML结束标签时调用
#创建一个新的解析器对象并返回xml.sax.make_parser([parser_list])
#创建一个SAX解析器并解析xml文档xml.sax.parse(xmlfile,contenthandler[,errorhandler])
#parseString方法创建一个XML解析器并解析xml字符串xml.sax.parseString(xmlstring,contenthandler[,errorhandler])

import xml.sax

class MovieHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.type = ""
      self.format = ""
      self.year = ""
      self.rating = ""
      self.stars = ""
      self.description = ""

   #元素开始调用
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "movie":
         print ("*****Movie*****")
         title = attributes["title"]
         print ("Title:", title)

   #元素结束调用
   def endElement(self, tag):
      if self.CurrentData == "type":
         print ("Type:", self.type)
      elif self.CurrentData == "format":
         print ("Format:", self.format)
      elif self.CurrentData == "year":
         print ("Year:", self.year)
      elif self.CurrentData == "rating":
         print ("Rating:", self.rating)
      elif self.CurrentData == "stars":
         print ("Stars:", self.stars)
      elif self.CurrentData == "description":
         print ("Description:", self.description)
      self.CurrentData = ""

   #读取字符时调用
   def characters(self, content):
      if self.CurrentData == "type":
         self.type = content
      elif self.CurrentData == "format":
         self.format = content
      elif self.CurrentData == "year":
         self.year = content
      elif self.CurrentData == "rating":
         self.rating = content
      elif self.CurrentData == "stars":
         self.stars = content
      elif self.CurrentData == "description":
         self.description = content
  
if (__name__ == "__main__"):
   
   #创建一个XMLReader
   parser = xml.sax.make_parser()
   #turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   #重写ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler(Handler)
   
   parser.parse("031_Movies.xml")

#文件对象模型DOM,W3C组织推荐的处理可扩展置标语言的标准编程接口
#DOM在解析一个XML文档时,一次性读取整个文档,把文档中所有元素保存在内存中的一个树结构里
   
from xml.dom.minidom import parse
import xml.dom.minidom

#使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("031_Movies.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print ("Root element : %s" % collection.getAttribute("shelf"))

#在集合中获取所有电影
movies = collection.getElementsByTagName("movie")

#打印每部电影的详细信息
for movie in movies:
   print ("*****Movie*****")
   if movie.hasAttribute("title"):
      print ("Title: %s" % movie.getAttribute("title"))

   type = movie.getElementsByTagName('type')[0]
   print ("Type: %s" % type.childNodes[0].data)
   format = movie.getElementsByTagName('format')[0]
   print ("Format: %s" % format.childNodes[0].data)
   rating = movie.getElementsByTagName('rating')[0]
   print ("Rating: %s" % rating.childNodes[0].data)
   description = movie.getElementsByTagName('description')[0]
   print ("Description: %s" % description.childNodes[0].data)










