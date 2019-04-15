//当对象的状态改变时，同时改变其行为
//状态模式就两点：1、可以通过改变状态来获得不同的行为。2、你的好友能同时看到你的变化
public class State{
	private String value;
	public void SetValue(String value){
		this.value = value;
	}
	public String getValue(){
		return value;
	}
	public void method1(){
		xxx
	}
	public void method2(){
		xxx
	}
}
public class Context(){
	private State state;
	public Context(State state){
		this.state = state;
	}
	public void setState(State state){
		this.state = state;
	}
	public State getState(){
		return state;
	}
	public void method(){
		if(state.getValue().equals("state1"))
			state.method1();
		else if(state.getValue().equals("state2"))
			state.method2();
	}
}

public class StateTest{
	public static void main(String[] args){
		State state = new State();
		Context context = new Context(state);
		state.SetValue("state1");
		context.method();
		state.SetValue("state2");
		context.method();
	}
}