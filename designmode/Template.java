//һ���������У���һ�����������ٶ���1...n�������������ǳ���ģ�Ҳ������ʵ�ʵķ���������һ���࣬�̳иó����࣬��д���󷽷���ͨ�����ó����࣬ʵ�ֶ�����ĵ���
public abstract class AbstractCalculator{
    /*��������ʵ�ֶԱ������������ĵ���*/
    public final int calculate(String exp, String opt){
        int array[] = split(exp, opt);
        return calculate(array[0], array[1]);
    }
    /*��������д�ķ���*/ 
    abstract public int calculate(int num1, int num2);
    public int[] split(String exp, String opt){
        String array[] = exp.split(opt);
        int arrayInt[] = new int[2];
        arrayInt[0] = Integer.parseInt(array[0]);
        arrayInt[1] = Integer.parseInt(array[1]);
        return arrayInt;
    }
}
public class Plus extends AbstractCalculator{
    @Override
    public int calculate(int num1, int num2){
        return num1 + num2;
    }
}
public class Minus extends AbstractCalculator{
    @Override
    public int calculate(int num1, int num2){
        return num1 - num2;
    }
}
public class TemplateTest{
    public static void main(String[] args){
        String exp = "8+8";
        AbstractCalculator cal = new Plus();
        int result = cal.calculate(exp, "\\+");
        xxx
    }
}
