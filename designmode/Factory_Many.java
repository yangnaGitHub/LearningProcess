//多个工厂方法模式是提供多个工厂方法，分别创建对象
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

public class SendFactory{
	public Sender produceMail(){
		return new MailSender();
	}
	public Sender produceSms(){
		return new SmsSender();
	}
}

public class FactoryTest{
	public static void main(String[] args){
		SendFactory factory = new SendFactory();
		Sender sender = factory.produceSms();
		sender.Send();
	}
}