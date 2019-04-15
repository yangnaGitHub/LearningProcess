//��Ԫģʽ����ҪĿ����ʵ�ֶ���Ĺ���������أ���ϵͳ�ж�����ʱ����Լ����ڴ�Ŀ�����ͨ���빤��ģʽһ��ʹ��
//FlyWeightFactory���𴴽��͹�����Ԫ��Ԫ
public class ConnectionPool{
    private Vector<Connection> pool;

    private String url = "jdbc:mysql://localhost:3306/test";
    private String username = "root";
    private String password = "root";
    private String driverClassName = "com.mysql.jdbc.Driver";

    private int poolSize = 100;
    private static ConnectionPool instance = null;
    Connection conn = null;

    private ConnectionPool(){
        pool = new Vector<Connection>(poolSize);

        for(int index = 0; index < poolSize; index++){
            try{
                Class.forName(driverClassName);
                conn = DriverManager.getConnection(url, username, password);
                pool.add(conn);
            }catch(ClassNotFoundException e){
                e.printStackTrace();
            }catch(SQLException e){
                e.printStackTrace();
            }
        }
    }
    public synchronized void release(){
        pool.add(conn);
    }
    public synchronized Connection getConnection(){
        if(pool.size() > 0){
            Connection conn = pool.get(0);
            pool.remove(conn);
            return conn;
        }else{
            return null;
        }
    }
}
