//写的一个接口中有多个抽象方法，当我们写该接口的实现类时，必须实现该接口的所有方法
//比较浪费，因为并不是所有的方法都是我们需要的，有时只需要某一些
//当不希望实现一个接口中所有的方法时，可以创建一个抽象类Wrapper
public interface Sourceable(){
	public void Method1();
	public void Method2();
}

public abstract class Wrapper implements Sourceable{
	public void Method1(){}
	public void Method2(){}
}

public class SourceSub1 extends Wrapper{
	public void Method1(){
		xxx
	}
}

public class SourceSub2 extends Wrapper{
	public void Method2(){
		xxx
	}
}

public class Adapter_InterfaceTest{
	public static void main(String[] args){
		Sourceable source1 = new SourceSub1();
		Sourceable source2 = new SourceSub2();
		source1.Method1();
		source1.Method2();
		source2.Method1();
		source2.Method2();
	}
}