//保存一个对象的某个状态，以便在适当的时候恢复对象
public class Original{
	private String value;
	public String getValue(){
		return value;
	}
	public void setValue(String value){
		this.value = value;
	}
	public Original(String value){
		this.value = value;
	}
	public Memento createMemento(){
		return new Memento(value);
	}
	public void restoreMemento(Memento memento){
		this.value = memento.getValue();
	}
}

public class Memento{
	private String value;
	public Memento(String value){
		this.value = value;
	}
	public String getValue(){
		return value;
	}
	public void setValue(){
		this.value = value;
	}
}

public class Storage{
	private Memento memento;
	public Storage(Memento memento){
		this.memento = memento;
	}
	public Memento getMemento(){
		return memento;
	}
	public void setMemento(Memento memento){
		this.memento = memento;
	}
}

public class MementoTest{
	public static void main(String[] args){
		Original original = new Original("yangna");
		Storage storage = new Storage(original.createMemento());
		xxx
		original.setValue("natasha");
		xxx
		original.restoreMemento(storage.getMemento());_
	}
}