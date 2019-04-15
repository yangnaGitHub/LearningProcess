//����ģʽ������һϵ���㷨������ÿ���㷨��װ������ʹ���ǿ����໥�滻�����㷨�ı仯����Ӱ�쵽ʹ���㷨�Ŀͻ�
public interface ICalculator{
    public int calculate(String exp);
}

public abstract class AbstractCalculator{
    public int[] split(String exp, String opt){
        String array[] = exp.split(opt);
        int arrayInt[] = new int[2];
        arrayInt[0] = Integer.parseInt(array[0]);
        arrayInt[1] = Integer.parseInt(array[1]);
        return arrayInt;
    }
}

public class Plus extends AbstractCalculator implements ICalculator{
    @Override
    public int calculate(String exp){
        int arrayInt[] = split(exp, "\\+");
        return arrayInt[0] + arrayInt[1];
    }
}
public class Minus extends AbstractCalculator implements ICalculator{
    @Override
    public int calculate(String exp){
        int arrayInt[] = split(exp, "-");
        return arrayInt[0] - arrayInt[1];
    }
}
public class Multiply extends AbstractCalculator implements ICalculator{
    @Override
    public int calculate(String exp){
        int arrayInt[] = split(exp, "\\*");
        return arrayInt[0] * arrayInt[1];
    }
}
public class StrategyTest{
    public static void main(String[] args){
        String exp = "2+8";
        ICalculator cal = new Plus();
        int result = cal.calculate(exp);
    }
}
