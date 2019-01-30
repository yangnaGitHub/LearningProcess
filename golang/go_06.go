// go_06
package main

import (
	"fmt"
)

func main() {
    /*数组
      相同唯一类型的一组 已经编号 长度固定的数据项序列
      类型可以是任意原始类型 索引从0号开始
      var variable_name [size] variable_type*/
    var first = [5]float32{1000.0, 1.1, 2.3, 6.5, 10.0}//{}中的个数不能大于[]中的数字,如果不填[]中的数,会根据{}中的个数自动设置SIZE
    fmt.Println(first)
    
    var second [10]int
    for index := 0; index < 10; index++ {
        second[index] = index + 1
        fmt.Printf("second[%d] = %d\n", index, second[index])
    }
    
    /*var variable_name [SIZE1][SIZE2]...[SIZEN] variable_type*/
    third := [3][4]int {
        {0, 1, 2, 3},
        {4, 5, 6, 7},
        {8, 9, 10, 11}}
    fmt.Println(third)
    
    var four = [5]int{1, 2, 3, 4, 5}
    setArray_len(four)
    
    var five = []int{6, 7, 8, 9}
    setArray(five)
}








































































func setArray(params []int) {
    fmt.Println("len(Array) = ", len(params))
}

func setArray_len(params [5]int) {
    fmt.Println("len(Array) = ", len(params))
}