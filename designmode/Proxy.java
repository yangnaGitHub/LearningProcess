//代理模式就是多一个代理类出来，替原对象进行一些操作
//打官司，我们需要请律师，因为律师在法律方面有专长，可以替我们进行操作，表达我们的想法
//如果已有的方法在使用的时候需要对原有的方法进行改进
//采用一个代理类调用原有的方法，且对产生的结果进行控制。这种方法就是代理模式
public interface Sourceable{
	public void Method();
}

public class Source implements Sourceable{
	@Override
	public void Method(){
		xxx
	}
}

public class Proxy implements Sourceable{
	private Source source;
	public Proxy(){
		super();
		this.source = new Source();
	}

	@Override
	public void Method(){
		before();
		source.Method();
		after();
	}

	private void before(){
		xxx
	}
	private void after(){

	}
}

public class ProxyTest{
	public static void main(String[] args){
		Sourceable source = new Proxy();
		source.Method();
	}
}
//diff Decorator