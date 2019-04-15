//单例对象能保证在一个JVM中，该对象只有一个实例存在
//省去了new操作符，降低了系统内存的使用频率，减轻GC压力
pubic class Singleton{
	/* 私有构造方法，防止被实例化 */ 
	private Singleton(){

	}
	/* 此处使用一个内部类来维护单例 */ 
	private static class SingletonFactory{
		private static Singleton instance = new Singleton();
	}
	/* 获取实例 */ 
	public static Singleton getInstance(){
		return SingletonFactory.instance;
	}
	/* 如果该对象被用于序列化，可以保证对象在序列化前后保持一致 */
	public Object readResolve(){
		return getInstance();
	}
}
//synchronized关键字,synchronized关键字锁定的是对象
//静态类不能实现接口,因为接口中不允许有static修饰的方法
//单例可以被延迟初始化，静态类一般在第一次加载是初始化
//单例类可以被继承，他的方法可以被覆写。但是静态类内部方法都是static，无法被覆写

