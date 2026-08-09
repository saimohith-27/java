class Dept{
    private int deptId;
    private String deptName;
    @SuppressWarnings("FieldMayBeFinal")
    private java.util.Scanner scanner = new java.util.Scanner(System.in);

    void setDeptId(){
        System.out.println("Enter Department ID: ");
        this.deptId = scanner.nextInt();
    }
    int getDeptId(){
        return deptId;
    }
    void setDeptName(){
        System.out.println("Enter Department Name: ");
        this.deptName = scanner.nextLine();
    }
    String getDeptName(){
        return deptName;
    }
    static String getDeptName(int deptId, Dept departments[], int numDepts){
        for(int i = 0; i < numDepts; i++){
            if(departments[i].getDeptId() == deptId){
                return departments[i].getDeptName();
            }
        }
        return "Invalid Department";
    }
}