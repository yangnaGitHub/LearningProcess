// go_04
package main

import (
	"fmt"
)

func main() {
    /*if condition {
      }else{
      }
      switch 判断变量 {
          case 变量值1:xx1
          case 变量值2,变量值3,变量值4:xx2
          ...
          default:xxn+m
      }
      switch {
          case 变量==变量值1:xx1
          case 变量==变量值2:xx2
          ...
          default:xxn+1
      }
      select类似于switch语句,但是select会随机执行一个可运行的case,如果没有case可运行就将他阻塞直到有case可运行
      每个case都必须有一个chan,所有的chan表达式都会被求值,如果多个case都可以运行就随机公平的选一个执行,其他的不会执行
      提倡使用chan的方法代替共享内存,任何时候只能有一个goroutine访问通道进行发送和获取数据,goroutine之间通过通道就可以通信
      通道就像是一个传送带或是队列,遵循先入先出的规则,保证收发数据的顺序
      var 通道变量 chan 通道类型
      chan的空值是nil,声明后需要配合make后才能使用
      通道是引用类型,需要使用make进行创建 通道实例 := make(chan 数据类型)
       数据类型:通道内传输的元素类型
       通道实例:通过make创建的通道句柄
      通道创建后可以使用通道进行发送和接收操作
       将数据通过通道发送的格式:通道变量 <- 值
       接收数据:
        阻塞接收数据:data := <-ch + 非阻塞接收数据:data(接收到的数据), ok(是否接收到数据) := <-ch
      */
    var c_1, c_2, c_3 chan int
    var var_a, var_b int
    select {
        case var_a = <-c_1://接收数据
            fmt.Println("received ", var_a, " from c1")
        case c_2 <-var_b://发送数据
            fmt.Println("sent ", var_b, " to c2")
        case var_c, ok := (<-c_3)://接收数据,然后看是否接收成功
            if ok {
                fmt.Println("received ", var_c, " from c3")
            }else{
                fmt.Println("c3 is closed")
            }
        default:
            fmt.Println("no communication")
    }
    
    for index := 0; index < 5; index++ {//for(index=0; index<5; index++){}
        fmt.Printf("index = %d\n", index)//fmt.Println("index = %d", index)
    }
    
    var a_var int
    var b_var int = 5
    for a_var < b_var {//while(a_var<b_var)
        a_var++
        fmt.Printf("a_var = %d\n", a_var)
    }
    
    numbers := [6]int{1, 2, 3, 5}//6个的数组,依顺序填写1, 2, 3, 5,剩下的2位为0
    fmt.Println(numbers)
    /*
      range格式可以对slice,map,数组,字符串等进行迭代循环
      for key,value := range mymaps {
          fmt.Println(key, value)
      }
    */
    for index,data := range numbers {
        fmt.Printf("index = %d, data = %d\n", index, data)
    }
}