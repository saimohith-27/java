class Emp{
    private int id;
    private String name;
    private int deptId;
    private double salary;
    private double commission;
    private Emp manager;
    private String hireDate;
    private String jobTitle;

    @SuppressWarnings("FieldMayBeFinal")
    private java.util.Scanner scanner = new java.util.Scanner(System.in);

    void setId(){
        System.out.println("Enter Employee ID: ");
        this.id = scanner.nextInt();
    }
    int getId(){
        return id;
    }
    void setName(){
        System.out.println("Enter Employee Name: ");
        this.name = scanner.nextLine(); 
    }
    String getName(){
        return name;
    }
    void setDeptId(Dept departments[], int numDepts){
        System.out.println("Enter Department ID: ");
        int setDeptId = scanner.nextInt();
        for(int i = 0; i < numDepts; i++){
            if(departments[i].getDeptId() == setDeptId){
                this.deptId = setDeptId;
                return;
            }
        }
        System.out.println("Invalid Department ID. Please try again.");
    }   
    int getDeptId(){
        return deptId;
    }
    void setSalary(){
        System.out.println("Enter Employee Salary: ");
        this.salary = scanner.nextDouble(); 
    }
    double getSalary(){
        return salary;
    }
    void setCommission(){
        System.out.println("Enter Employee Commission: ");
        this.commission = scanner.nextDouble(); 
    }
    double getCommission(){
        return commission;
    }
    void setManager(Emp employees[], int numEmployees){
        System.out.println("Enter Manager ID (or 0 if no manager): ");
        int managerId = scanner.nextInt();
        if(managerId != 0){
            for(int i = 0; i < numEmployees; i++){
                if(employees[i].getId() == managerId){
                    this.manager = employees[i];
                    break;
                }
            }
        }
    }
    Emp getManager(){
        return manager;
    }
    void setHireDate(){
        System.out.println("Enter Employee Hire Date (YYYY-MM-DD): ");
        this.hireDate = scanner.nextLine();
    }
    String getHireDate(){
        return hireDate;
    }
    void setJobTitle(){
        System.out.println("Enter Employee Job Title: ");
        this.jobTitle = scanner.nextLine(); 
    }
    String getJobTitle(){
        return jobTitle;
    }
    void displayEmployeeDetails(Emp emp , Dept departments[], int numDepts){
        System.out.println("Employee ID: " + emp.getId());
        System.out.println("Employee Name: " + emp.getName());
        System.out.println("Department ID: " + emp.getDeptId());
        System.out.println("Department Name: " + Dept.getDeptName(emp.getDeptId(), departments, numDepts));
        System.out.println("Salary: " + emp.getSalary());
        System.out.println("Commission: " + emp.getCommission());
        if(emp.getManager() != null){
            System.out.println("Manager ID: " + emp.getManager().getId());
            System.out.println("Manager Name: " + emp.getManager().getName());
        } else {
            System.out.println("Manager: None");
        }
        System.out.println("Hire Date: " + emp.getHireDate());
        System.out.println("Job Title: " + emp.getJobTitle());
    }
    void createEmployee(Emp employees[], int numEmployees, Dept departments[], int numDepts){
        setId();
        scanner.nextLine(); // Consume newline left-over
        setName();
        setDeptId(departments, numDepts);
        setSalary();
        setManager(employees, numEmployees); // Initially, no manager is assigned
        setCommission();
        scanner.nextLine(); // Consume newline left-over
        setHireDate();
        setJobTitle();
    }
    boolean isNameStartingWith(String letter){
        letter = letter.toLowerCase();
        return name != null && !name.isEmpty() && name.startsWith(letter) || name.startsWith(letter.toUpperCase());
    }
    boolean compareSalary(Emp other){
        return this.salary > other.salary;
    }
}