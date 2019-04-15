//桥接模式就是把事物和其具体实现分开，使他们可以各自独立的变化
//将抽象化与实现化解耦，使得二者可以独立变化
public interface Sourceable{
    public void method();
}

public class SourceSub1 implements Sourceable{
    @Override
    public void method(){
        xxx
    }
}
public class SourceSub2 implements Sourceable{
    @Override
    public void method(){
        xxx
    }
}

public abstract class Bridge{
    private Sourceable source;
    public void method(){
        source.method();
    }
    public Sourceable getSource(){
        return source;
    }
    public void setSource(Sourceable source){
        this.source = source;
    }
}
//client
public class MyBridge extends Bridge{
    public void method(){
        getSource().method();
    }
}

public class BridgeTest{
    public static void main(String[] args){
        Bridge bridge = new MyBridge();
        Sourceable source1 = new SourceSub1();
        bridge.setSource(source1);
        bridge.method();

        Sourceable source2 = new SourceSub2();
        bridge.setSource(source2);
        bridge.method();
    }
}
