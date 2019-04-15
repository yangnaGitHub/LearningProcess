//命令模式的目的就是达到命令的发出者和执行者之间解耦，实现请求和执行分开
//Struts其实就是一种将请求和呈现分离的技术
public interface Command{
	public void exe();
}

public class MyCommand implements Command{
	private Receiver receiver;
	public MyCommand(Receiver receiver){
		this.receiver = receiver;
	}
	@Override
	public void exe(){
		receiver.action();
	}
}
public class Receiver{
	public void action(){
		xxx
	}
}

public class Invoker{
	private Command command;
	public Invoker(Command command){
		this.command = command;
	}
	public void action(){
		command.exe();
	}
}

public class CommandTest{
	public static void main(String[] args){
		Receiver receiver = new Receiver();
		Command command = new MyCommand(receiver);
		Invoker invoker = new Invoker(command);
		invoker.action();
	}
}