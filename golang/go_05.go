// go_05
package main

import (
	"fmt"
	"math"
)

/*go支持匿名函数,可以作为闭包,是一个内联语句或表达式
  可以直接使用函数内的变量,不必声明*/
func getSequence() func() int {
    index := 0
    return func() int {
        index += 1
        return index
    }
}

type Circle struct {//定义结构体
    radius float64
}

func main() {
    var a_var int = 100
    var b_var int = 101
    fmt.Printf("max_value = %d\n", find_max(a_var, b_var))
    
    fmt.Println(string_swap("yangna", "natasha"))
    
    swap_value(a_var, b_var)
    fmt.Printf("swap_value = %d, %d\n", a_var, b_var)//swap_value = 100, 101
    
    swap_reference(&a_var, &b_var)
    fmt.Printf("swap_reference = %d, %d\n", a_var, b_var)//swap_reference = 101, 100
    
    swap_reference_or(&a_var, &b_var)
    fmt.Printf("swap_reference_or = %d, %d\n", a_var, b_var)//swap_reference_or = 100, 101
    
    getSquareRoot := func(x_data float64) float64 {//声明函数变量
        return math.Sqrt(x_data)
    }
    fmt.Println(getSquareRoot(9))//3
    
    nextNumber := getSequence()//作为一个函数,函数的index=0
    fmt.Println(nextNumber())//1
    fmt.Println(nextNumber())//2
    
    var var_c_object Circle
    var_c_object.radius = 5.00
    fmt.Println("圆的面积是:", var_c_object.getArea())//78.5
}

/*func func_name([parameters]) [return types] {
  }*/
func find_max(num1, num2 int) int {
    var result int
    if num1 > num2 {
        result = num1
    } else {
      result = num2  
    }
    return result
}

func string_swap(x_str, y_str string) (string, string) {
    return y_str, x_str
}

/*值传递
  引用传递*/
func swap_value(x_data, y_data int) {
    x_data = x_data + y_data
    y_data = x_data - y_data
    x_data = x_data - y_data
}

func swap_reference(x_data *int, y_data *int) {
    *x_data = *x_data * *y_data
    *y_data = *x_data / *y_data
    *x_data = *x_data / *y_data
}

func swap_reference_or(x_data *int, y_data *int) {
    *x_data = *x_data ^ *y_data
    *y_data = *x_data ^ *y_data
    *x_data = *x_data ^ *y_data
}

func (var_c Circle) getArea() float64 {//可以是指针var_c *Circle
    return 3.14*var_c.radius*var_c.radius
}