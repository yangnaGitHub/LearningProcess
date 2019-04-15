//装饰模式就是给一个对象增加一些新的功能，而且是动态的
//要求装饰对象和被装饰对象实现同一个接口，装饰对象持有被装饰对象的实例
//需要扩展一个类的功能
//动态的为一个对象增加功能，而且还能动态撤销
public interface Sourceable(){
	public void Method();
}

public class Source implements Sourceable{
	@Override
	public void Method(){
		xxx
	}
}
public class Decorator implements Sourceable{
	private Sourceable source;
	public Decorator(Sourceable source){
		super();
		this.source = source;
	}
	@Override
	public void Method(){
		xxx
		source.Method();
		xxx
	}
}

public class DecoratorTest{
	public static void main(String[] args){
		Sourceable source = new Source();
		Sourceable decorator = new Decorator(source);
		decorator.Method();
	}
}
