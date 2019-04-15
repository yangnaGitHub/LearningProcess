//������ģʽ����˳����ʾۼ��еĶ���
//һ����Ҫ�����Ķ��󣬼��ۼ����󣬶��ǵ������������ڶԾۼ�������б�������
public interface Iterator{
    public Object previous();
    public Object next();
    public boolean hasNext();
    public Object first();
}
public interface Collection{
    public Iterator iterator;
    public Object get(int index);
    public int size();
}

public class MyIterator implements Iterator{
    private Collection collection;
    private int pos = -1;
    public MyIterator(Collection collection){
        this.collection = collection;
    }
    @Override
    public Object previous(){
        if(pos > 0)
            pos--;
        return collection.get(pos);
    }
    @Override
    public Object next(){
        if(pos < collection.size() - 1)
            pos++;
        return collection.get(pos);
    }
    @Override
    public boolean hasNext(){
        if(pos < collection.size() - 1)
            return true;
        else
            return false;
    }
    @Override
    public Object first(){
        pos = 0;
        return collection.get(pos);
    }
}

public class MyCollection implements Collection{
    public String string[] = {"A", "B", "C", "D", "E"};
    @Override
    public Iterator iterator(){
        return new MyIterator(this);
    }
    @Override
    public Object get(int index){
        return string[index];
    }
    @Override
    public int size(){
        return string.length;
    }
}

public class InteratorTest{
    Collection collection = new MyCollection();
    Iterator iterator = collection.iterator();
    while(it.hasNext())
        xxx
}
