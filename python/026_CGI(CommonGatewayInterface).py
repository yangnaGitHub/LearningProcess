#CGI通用网关接口,是一段运行在服务器上程序(HTTP服务器)

#1>访问URL并连接到HTTP web 服务器
#2>服务器接收到请求信息后会解析URL,并查找访问的文件在服务器上是否存在,存在返回文件的内容
#3>浏览器从服务器上接收信息,显示接收的文件或者错误信息

#进行CGI编程前,确保Web服务器支持CGI及已经配置了CGI的处理程序,CGI文件的扩展名为.cgi
#Apache支持CGI配置
#1>设置好CGI目录(HTTP服务器执行CGI程序都保存在一个预先配置的目录)ScriptAlias /cgi-bin/ /var/www/cgi-bin/
 #想指定其他运行CGI脚本的目录,修改httpd.conf配置文件
 #AddHandler中添加.py后缀AddHandler cgi-script .cgi .pl .py
print("Content-type:text/html")#告诉浏览器文件的内容类型
print()#空行,告诉服务器结束头部
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print('<title>Hello Word - 我的第一个 CGI 程序！</title>')
print('</head>')
print('<body>')
print('<h2>Hello Word! 我是来自菜鸟教程的第一CGI程序</h2>')
print('</body>')
print('</html>')

#CGI的环境变量
#import os
#print("Content-type: text/html")
#print()
#print("<meta charset=\"utf-8\">")
#print("<b>环境变量</b><br>")
#print("<ul>")
#for key in os.environ.keys():
#    print("<li><span style='color:green'>%30s </span> : %s </li>" % (key,os.environ[key]))
#print("</ul>")

#客户端通过两种方法向服务器传递信息,GET&POST
#GET方法发送编码后的用户信息到服务端,数据信息包含在请求页面的URL上,以"?"号分割
 #请求可被缓存
 #请求保留在浏览器历史记录中
 #请求可被收藏为书签
 #请求不应在处理敏感数据时使用
 #请求有长度限制
 #请求只应当用于取回数据
 #
 #/cgi-bin/test.py?name=菜鸟教程&url=http://www.runoob.com
 #import cgi, cgitb
 #form = cgi.FieldStorage()#FieldStorage实例化
 #site_name = form.getvalue('name')
 #site_url  = form.getvalue('url')
 #
 #<form action="/cgi-bin/hello_get.py" method="get">

#POST方法向服务器传递数据是更安全可靠的,一些敏感信息如用户密码等需要使用POST传输数据
 #<form action="/cgi-bin/hello_get.py" method="post">

#cookie会在http头部单独发送
#使用了Set-Cookie头信息来设置Cookie信息,过期时间Expires,域名Domain,路径Path
#print('Content-Type: text/html')
#print('Set-Cookie: name="菜鸟教程";expires=Wed, 28 Aug 2016 18:30:00 GMT')
#print()

#检索Cookie信息
#Cookie信息存储在CGI的环境变量HTTP_COOKIE中
#if 'HTTP_COOKIE' in os.environ:
#    cookie_string=os.environ.get('HTTP_COOKIE')
#    c=Cookie.SimpleCookie()
#    c.load(cookie_string)
#    try:
#        data=c['name'].value
#        print ("cookie data: "+data+"<br>")
#    except KeyError:
#        print ("cookie 没有设置或者已过去<br>")

#上传文件的表单需要设置enctype属性为multipart/form-data
 #<meta charset="utf-8">
 #<form enctype="multipart/form-data" action="/cgi-bin/save_file.py" method="post">
 #<input type="file" name="filename" />
 #
 #import cgi, os
 #import cgitb; cgitb.enable()
 #form = cgi.FieldStorage()
 #fileitem = form['filename']
 #if fileitem.filename:
 #fn = os.path.basename(fileitem.filename)
 #open('/tmp/' + fn, 'wb').write(fileitem.file.read())

#文件下载通过设置HTTP头信息来实现
#print ("Content-Disposition: attachment; filename=\"foo.txt\"")
