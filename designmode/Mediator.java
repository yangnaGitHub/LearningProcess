//中介者模式也是用来降低类类之间的耦合的，因为如果类类之间有依赖关系的话，不利于功能的拓展和维护，因为只要修改一个对象，其它关联的对象都得进行修改
//有点像spring容器的作用
public interface Mediator{
	public void createMediator();
	public void workAll();
}

public class MyMediator implements Mediator{
	private User user1;
	private User user2;
	public User getUser1(){
		return User1;
	}
	public User getUser2(){
		return User2;
	}
	@Override
	public void createMediator(){
		user1 = new User1(this);
		user2 = new User2(this);
	}
	@Override
	public void workAll(){
		user1.work();
		user2.work();
	}
}

public abstract class User{
	private Mediator mediator;
	public Mediator getMediator{
		return mediator;
	}
	public User(Mediator mediator){
		this.mediator = mediator;
	}
	public abstract void work();
}

public class User1 extends User{
	public User1(Mediator mediator){
		super(mediator);
	}
	@Override
	public void work(){
		xxx
	}
}

public class User2 extends User{
	public User2(Mediator mediator){
		super(mediator);
	}
	@Override
	public void work(){
		xxx
	}
}

public class MediatorTest{
	public static void main(String[] args){
		Mediator mediator = new Mediator();
		mediator.createMediator();
		mediator.workAll();
	}
}