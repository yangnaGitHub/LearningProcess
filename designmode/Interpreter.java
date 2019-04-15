//解释器模式用来做各种各样的解释器，如正则表达式等的解释器等等
public class Context{
	private int num1;
	private int num2;
	public Context(int num1, int num2){
		this.num1 = num1;
		this.num2 = num2;
	}
	public int getNum1(){
		return num1;
	}
	public int getNum2(){
		return num2;
	}
	public void setNum1(int num){
		this.num1 = num;
	}
	public void setNum2(int num){
		this.num2 = num;
	}
}

public interface Expression{
	public int interpret(Context context);
}
public class Plus implements Expression{
	@Override
	publiv int interpret(Context context){
		return context.getNum1() + context.getNum2();
	}
}

public class Minus implements Expression{
	@Override
	publiv int interpret(Context context){
		return context.getNum1() - context.getNum2();
	}
}

public class InterpretTest{
	public static void main(String[] args){
		int result = new Minus().interpret(new Context(new Plus().interpret(new Context(9, 2)), 8));    
	}
}