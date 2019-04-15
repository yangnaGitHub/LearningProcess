//外观模式是为了解决类与类之家的依赖关系的
//可以将类和类之间的关系配置到配置文件中，而外观模式就是将他们的关系放在一个Facade类中，降低了类类之间的耦合度，
public class Cpu{
    public void StartUp(){
        xxx
    }
    public void ShutDown(){
        xxx
    }
}
public class Memory(){
    public void StartUp(){
        xxx
    }
    public void ShutDown(){
        xxx
    }
}
public class Disk{
    public void StartUp(){
        xxx
    }
    public void ShutDown(){
        xxx
    }
}

public class Computer(){
    private Cpu cpu;
    private Memory memory;
    private Disk disk;

    public Computer(){
        cpu = new Cpu();
        memory = new Memory();
        disk = new Disk();
    }
    public void StartUp(){
        xxx
        cpu.StartUp();
        memory.StartUp();
        disk.StartUp();
        xxx
    }
    public void ShutDown(){
        xxx
        cpu.ShutDown();
        memory.ShutDown();
        disk.ShutDown();
        xxx
    }
}

public class FacadeTest{
    Computer computer = new Computer();
    computer.StartUp();
    computer.ShutDown();
}

