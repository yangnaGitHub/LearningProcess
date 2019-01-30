// go_03
package main

import (
	"fmt"
	"unsafe"
)

func main() {
    //声明变量
    //var identifier type,声明后若不赋值则使用默认值
    var bool_data bool
    fmt.Println(bool_data)
    //根据值自行判定变量类型
    var int_data = 2
    fmt.Println(int_data)
    /*省略var,:=左侧的变量不应该是已经声明过的,只能在函数体中使用
      使用=是将一个变量赋值给另外一个变量,是将内存中的值进行了copy
      &variable,使用&来获取variable的地址*/
    oth_init := 10
    fmt.Println(oth_init)
    
    //多变量声明
    //var vname1, vname2, vname3 type
    //var vname1, vname2, vname3 = v1, v2, v3自动推断
    //vname1, vname2, vname3 := v1, v2, v3 => 只能在函数体中使用
    
    //const常量
    //显式
    const str_var_0 string = "natasha"
    //隐式
    const str_var_1 = "yangna"
    
    const LENGTH int = 10
    const WIDTH int = 5
    var area int
    const a_var, b_var, c_var = 1, false, "yangna"
    area = LENGTH * WIDTH
    fmt.Println("面积为:%d", area)//面积为:50
    println(a_var, b_var, c_var)//1 false yangna
    
    //常量也可以用作枚举
    const(
        Unknown = 0
        Female = 1
        Male = 2
    )
    const(
        em_a = "yangna"
        em_b = len(em_a)//可以使用内置函数
        em_c = unsafe.Sizeof(em_a) 
    )
    //字符串类型在go里是个结构,包含指向底层数组的指针和长度,每个部分都是8个字节,所以大小是16个字节
    println(em_a, em_b, em_c)//yangna 6 16
    
    /*iota特殊常量,可认为是一个可以被编译器修改的常量
      在const出现时将被重置为0(内部第一行之前),每每新增一行将使iota计数一次*/
    const(
        iota_a = iota   //0
        iota_b          //1
        iota_c          //2
        iota_d = "yang" //独立值,iota += 1
        iota_e          //"ha"iota += 1
        iota_f = 100    //iota += 1
        iota_g          //100 iota += 1
        iota_h = iota   //7,恢复计数
        iota_i          //8
    )
    fmt.Println(iota_a, iota_b, iota_c, iota_d, iota_e, iota_f, iota_g, iota_h, iota_i)//0 1 2 yang yang 100 100 7 8
    const(
        iota_i = 1<<iota
        iota_j = 3<<iota
        iota_k
        iota_l
    )
    fmt.Println(iota_i, iota_j, iota_k, iota_l)//1 6 12 24
} 