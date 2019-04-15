//部分-整体模式在处理类似树形结构的问题时比较方便
public class TreeNode{
    private String name;
    private TreeNode parent;
    private Vector<TreeNode> children = new Vector<TreeNode>();
    public TreeNode(String name){
        this.name = name;
    }
    public String getName(){
        return name;
    }
    public void setName(String name){
        this.name = name;
    }
    public TreeNode getParent(){
        return parent;
    }
    public void setParent(TreeNode parent){
        this.parent = parent;
    }
    public void add(TreeNode node){
        children.add(node);
    }
    public void remove(TreeNode node){
        children.remove(node);
    }
    public Enumeration<TreeNode> getChildren(){
        return children.elements();
    }
}

public class CompositeTest{
    TreeNode root = null;
    public CompositeTest(String name){
        root = new TreeNode(name);
    }
    public static void main(String[] args){
        CompositeTest tree = new CompositeTest("A");
        TreeNode nodeb = new TreeNode("B");
        TreeNode nodec = new TreeNode("C");
        nodeb.add(nodec);
        tree.root.add(nodeb);
        xxx
    }
}
