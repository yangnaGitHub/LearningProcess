# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 17:24:46 2018

@author: natasha1_Yang
"""

#Python提供多个图形开发界面的库
#Tkinter:Unix+Windows+Mac基本都可以使用,内置安装包,可应付简单的图形界面
#wxPython:开源,比较方便创建方便完整的GUI界面
#Jython:使用Java语言,可被动态的编译成Java字节码

import Tkinter
#1.导入Tkinter模块
#2.创建控件
test = Tkinter.Tk()
# 1.1>Tkinter目前提供15种控件
#  Button:按钮控件
#  Canvas:画布控件(显示图形元素如线条或者文本)
#  Checkbutton:多项选择框
#  Entry:输入控件==>显示简单的文本内容
#  Frame:框架控件==>矩形区域,多用来作为容器
#  Label:标签==>显示文本和位图
#  Listbox:列表控件
#  Menubutton:菜单按钮控件
#  Menu:菜单控件,下拉菜单和弹出菜单
#  Message:消息控件,显示多行文本
#  Radiobutton:单选按钮
#  Scale:范围控件,显示数值刻度
#  Scrollbar:滚动条控件
#  Text:文本控件,显示多行文本
#  Toplevel:容器控件,提供单独的对话框
#  Spinbox:输入控件,可以指定输入范围值
#  PanedWindow:窗口布局管理
#  LabelFrame:简单的容器控件
#  tkMessageBox:应用程序的消息框
# 1.2>控件的共有属性
#  Dimension:控件大小
#  Color:控件颜色
#  Font:控件字体
#  Anchor:锚点
#  Refief:控件样式
#  Bitmap:位图
#  Cursor:光标
# 1.3>几何管理
#  pack():包装
#  grid():网格
#  place():位置
#3.指定控件属于哪一个
#4.告诉GM(geometry manager)有一个控件产生
test.mianloop()#进入消息循环