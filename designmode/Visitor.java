//访问者模式把数据结构和作用于结构上的操作解耦合，使得操作集合可相对自由地演化。访问者模式适用于数据结构相对稳定算法又易变化的系统
//访问者模式使得算法操作增加变得容易
//访问者模式的优点是增加操作很容易，因为增加操作意味着增加新的访问者
//增加新的数据结构很困难
//访问者模式就是一种分离对象数据结构与行为的方法，通过这种分离，可达到为一个被访问者动态添加新的操作而无需做其它的修改的效果
//增加新功能
public interface Visitor{
	public void visit(Subject aub);
}
public class MyVisitor implements Visitor{
	@Override
	public void visit(Subject sub){
		xxx
	}
}

public interface Subject{
	public void accept(Visitor visitor);
	public String getSubject();
}

public class MySubject implements Subject{
	@Override
	public void accept(Visitor visitor){
		visitor.visit(this);
	}
	@Override
	public String getSubject(){
		return "LOVE";
	}
}

public class VisitorTest{
	public static void main(String[] args){
		Visitor visitor = new Visitor();
		Subject sub = new MySubject();
		sub.accept(visitor);
	}
}