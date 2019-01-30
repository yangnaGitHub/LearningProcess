// go_02
//保留字
/*
 break    default	     func	 interface select
 case     defer	     go	 map	    struct
 chan	   else	     goto	 package   switch
 const	   fallthrough if 	 range	    type
 continue for	        import return	 var
*/
/*uint[8|16|32|64] + int[8|16|32|64]
float[32|64] complex[64|128]:[32|64]位实数和虚数
byte:uint8 rune:int32 uintptr:用于存放一个指针
go1.9版本对于数字类型,var定义就好,无需定义int及float32,float64,系统会自动识别*/

package main

import(
    "fmt"
    "strings"
)

func main(){
    str := "natasha is branch"
    fmt.Println(str)
    
    str = strings.Replace(str, " ", "_", -1)
    
    fmt.Println(str)
    
    var float_data = 1.5
    var int_data = -1
    var uint_data = 2
    fmt.Println(float_data)
    fmt.Println(int_data)
    fmt.Println(uint_data)
}