#PyMySQL用于连接MySQL服务器的一个库
#安装PyMySQL(pip install PyMySQL)
#Mysql数据库用户授权请使用Grant命令
import pymysql
db = pymysql.connect("localhost", "username", "password", "database")#打开数据库连接
cursor = db.cursor()#创建一个游标对象
cursor.execute("SELECT VERSION()")#执行SQL查询
data = cursor.fetchone()#fetchone()方法获取单条数据
print("Database version : %s " % data)
db.close()
#可以使用execute()方法来为数据库创建表
 #cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
 #使用预处理语句创建表
 #sql = """CREATE TABLE EMPLOYEE (
 #        FIRST_NAME  CHAR(20) NOT NULL,
 #        LAST_NAME  CHAR(20),
 #        AGE INT,  
 #        SEX CHAR(1),
 #        INCOME FLOAT )"""
 #cursor.execute(sql)
#插入语句
 #sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
 #        LAST_NAME, AGE, SEX, INCOME)
 #        VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
 #try:
 #  cursor.execute(sql)
 #  db.commit()提交到数据库执行
 #except:
 #  db.rollback()发生错误则回滚

#fetchone()方法获取单条数据,结果集是一个对象
#fetchall()获取多条数据,全部的返回结果行
#rowcount只读属性返回执行execute()方法后影响的行数
 #try:
 #  cursor.execute(sql)
 #  results = cursor.fetchall()
 #  for row in results:
 #      name = row[0] 
 #      age = row[1]
 #except:
 #

#事务机制可以确保数据一致性ACID
#原子性,一致性,隔离性,持久性
#当游标建立之时,自动开始了一个隐形的数据库事务
#commit()方法游标的所有更新操作,rollback()方法回滚当前游标的所有操作
#
#
#
#
#
#
#
#
