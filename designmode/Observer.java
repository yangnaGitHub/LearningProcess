//当一个对象变化时，其它依赖该对象的对象都会收到通知，并且随着变化
public interface Observer{
    public void update();
}

public class Observer1 implements Observer{
    @Override
    public void update(){
        xxx
    }
}

public class Observer2 implements Observer{
    @Override
    public void update(){
        xxx
    }
}

public interface Subject{
    public void add(Observer observer);
    public void del(Observer observer);
    public void notifyObserver();
    public void operation();
}

public abstract class AbstractSubject implements Subject{
    private Vector<Observer> vector = new Vector<Observer>();
    @Override
    public void add(Observer observer){
        vector.add(observer);
    }
    @Override
    public void del(Observer observer){
        vector.remove(observer);
    }
    @Override
    public void notifyObserver(){
        Enumeration<Observer> enumo = vector.elements();
        while(enumo.hasMoreElements()){
            enumo.nextElement().updata();
        }
    }
}

public class MySubject extends AbstractSubject{
    @Override
    public void operation(){
        xxx
        notifyObserver();
    }
}

public class ObserverTest{
    public static void main(String[] args){
        Subject sub = new MySubject();
        sub.add(new Observer1);
        aub.add(new Observer2);
        sub.operation();
    }
}
