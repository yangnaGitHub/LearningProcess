//解决兼容性的问题
//当希望将一个类转换成满足另一个新接口的类时，可以使用类的适配器模式
//创建一个新类，继承原有的类，实现新的接口即可
public class Source1{
	public void Method1(){
		xxx
	}
}

public class Source2{
	public void Method1(){
		xxx
	}
}

public interface Targetable{
	public void Method1();
	public void Method2();
}

public class Adapter1 extends Source1 implements Targetable{
	@Override
	public void Method2(){
		xxx
	}
}

public class Adapter2 extends Source2 implements Targetable{
	@Override
	public void Method2(){
		xxx
	}
}

public class Adapter_ClassTest{
	public static void main(String[] args){
		Targetable target1 = new Adapter1();
		target1.Method1();
		target1.Method2();
		Targetable target2 = new Adapter2();
		target2.Method1();
		target2.Method2();
	}
}