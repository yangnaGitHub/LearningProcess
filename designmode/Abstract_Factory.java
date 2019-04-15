//工厂方法模式有一个问题就是，类的创建依赖工厂类
//抽象工厂模式，创建多个工厂类，这样一旦需要增加新的功能，直接增加新的工厂类就可以了
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

public interface Provider{
	public Sender produce();
}

public class SendMailFactory implements Provider{
	@Override
	public Sender produce(){
		return new MailSender();
	}
}

public class SendSmsFactory implements Provider{
	@Override
	public Sender produce(){
		return new SmsSender();
	}
}

public class Abstract_FactoryTest{
	public static void main(String[] args){
		Provider provider = new SendSmsFactory();
		Sender sender = provider.produce();
		sender.Send();
	}
}