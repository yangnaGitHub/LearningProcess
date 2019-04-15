//将上面的多个工厂方法模式里的方法置为静态的，不需要创建实例，直接调用即可
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
	public static Sender produceMail(){
		return new MailSender();
	}
	public static Sender produceSms(){
		return new SmsSender();
	}
}

public class FactoryTest{
	public static void main(String[] args){
		Sender sender = SendFactory.produceMail();
		sender.Send();
	}
}