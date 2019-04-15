//希望将一个对象转换成满足另一个新接口的对象时
//创建一个Wrapper类，持有原类的一个实例，在Wrapper类的方法中，调用实例的方法就行。
public class Source{
	public void Method1(){
		xxx
	}
}

public interface Targetable{
	public void Method1();
	public void Method2();
}

public class Adapter implements Targetable{
	private Source source;
	public Adapter(Source source){
		super();
		this.source = source;
	}
	@Override
	public void Method2(){
		xxx
	}
	@Override
	public void Method1(){
		source.Method1();
	}
}

public class Adapter_ObjectTest{
	public static void main(String[] args){
		Source source = new Source();
		Targetable target = new Adapter(Source);
		target.Method1();
		target.Method2();
	}
}