//工厂类模式提供的是创建单个类的模式，而建造者模式则是将各种产品集中起来进行管理，用来创建复合对象
//所谓复合对象就是指某个类具有不同的属性
public interface Sender{
	public void Send();
}

public class MailSender implements Sender{
	@Override
	public void Send(){
		xxx
	}
}

public class SmsSender implements Sender{
	@Override
	public void Send(){
		xxx
	}
}

public class Builder{
	//表现对象为List(混合对象)
	private List<Sender> list = new ArrayList<Sender>();
	public void produceMail(int count){
		for(int index = 0; index < count, index++)
			list.add(new MailSender());
	}
	public void produceSms(int count){
		for(int index = 0; index < count, index++)
			list.add(new SmsSender())
	}
}

public class BuilderTest{
	public static void main(String[] args){
		Builder builder = new Builder();
		builder.produceSms(10);
	}
}
//工厂模式关注的是创建单个产品，而建造者模式则关注创建符合对象