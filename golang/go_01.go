// go_01
package main//1.包声明,main表示一个可独立执行的程序

//2.引入包,需要使用fmt包
import (
	"fmt"//包实现了格式化IO
)

//3.代码块
func main() {//程序开始执行的函数,{不能单独放一行
	fmt.Println("Hello World!")//自动增加换行字符=fmt.Print("hello, world\n")
}
//标识符大写字母开头就可以被外部包的代码所使用(导出),小写字母开头则对包外是不可见的但是在整个包的内部是可见并且可用的

/*sudo apt-get install golang-go linux版本的安装命令
  https://golang.google.cn/dl/下载go语言
  http://liteide.org/cn/download/下载liteide
  http://www.runoob.com/go/go-tutorial.html
  https://www.w3cschool.cn/go/
*/

/*存储集群或类似用途的巨型中央服务器的系统编程语言
  高性能分布式系统领域而言,有着更高的开发效率,提供了海量并行的支持,游戏服务端的开发而言是再好不过了
  运行命令:go run go_01.go
  最主要的特征:
   自动垃圾回收
   丰富的内置类型
   多返回值
   错误处理
   匿名函数和闭包
   类型和接口
   并发编程
   反射
   语言交互性
*/

//运行命令:go run xx.go