#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#��������˴��󣬿�������Լ������һ���������
def foo():
    r = some_function()
    if r == (-1):
        return (-1)
    return r
def bar():
    r = foo()
    if r == (-1):
        print("Error")
    else:
        pass
#ĳЩ������ܻ����ʱ���Ϳ�����try��������δ��룬���ִ�г�����������벻�����ִ�У�����ֱ����ת����������룬��except���飬ִ����except�������finally���飬��ִ��finally����
#����û�д�����������except���鲻�ᱻִ�У�����finally����У���һ���ᱻִ��
#�����ж��except������ͬ���͵Ĵ���
try:
    print("try")
    r = 10 / 0
    print("result = ", r)
except ZeroDivisionError as e:
    print("except:", e)
finally:
    print("finally")
print("END")
#Python���еĴ����Ǵ�BaseException��������
#try...except���������һ���޴�ĺô������ǿ��Կ�Խ�����ã����纯��main()����foo()��foo()����bar()�����bar()�����ˣ���ʱ��ֻҪmain()�����ˣ��Ϳ��Դ���
def foo(s):
    return 10 / int(s)
def bar(s):
    return foo(s) * 2
def main():
    try:
        bar("0")
    except Exception as e:
        print("Error : ", e)
    finally:
        print("finally")
main()
#�������û�б��������ͻ�һֱ�����ף����Python���������񣬴�ӡһ��������Ϣ��Ȼ������˳�
#Python���õ�loggingģ����Էǳ����׵ؼ�¼������Ϣ
#import logging
#def foo(s):
#    return 10 / int(s)
#def bar(s):
#    return foo(s) * 2
#def main():
#    try:
#        bar("0")
#    except Exception as e:
#        logging.exception(e)
#main()
#raise����׳�һ�������ʵ��
#������print()�������鿴�ĵط����������ö��ԣ�assert�������
#assert n != 0, 'n is zero!' ==> ���ʽn != 0Ӧ����True�����򣬸��ݳ������е��߼�
#��Python������ʱ������-O�������ر�assert python3.4 -O err.py
#import logging
#logging.basicConfig(level=logging.INFO)
#s = "0"
#n = int(s)
#logging.info("n = %d" % n)
print(10 / n)
#������ָ����¼��Ϣ�ļ�����debug��info��warning��error�ȼ������𣬵�����ָ��level=INFOʱ��logging.debug�Ͳ���������
#����Python�ĵ�����pdb���ó����Ե�����ʽ���У�������ʱ�鿴����״̬
#python3 -m pdb err.py
#��������l���鿴����, ��������n���Ե���ִ�д���, ��������p ���������鿴����, ��������q��������
#import pdb��Ȼ���ڿ��ܳ���ĵط���һ��pdb.set_trace()���Ϳ�������һ���ϵ�
#������Զ���pdb.set_trace()��ͣ������pdb���Ի���������������p�鿴����������������c��������
