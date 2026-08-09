class Main {
    public static void main(String[] args) {
        System.out.println("Welcome to Employee Management System");
        System.out.println("=====================================");
        System.out.println("Enter total number of departments: ");
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        int numDepts = scanner.nextInt();
        Dept departments[] = new Dept[numDepts];
        for (int i = 0; i < numDepts; i++) {
            Dept dept = new Dept();
            dept.setDeptId();
            dept.setDeptName();
            departments[i] = dept;
        }
        Emp employees[] = new Emp[100]; // Declare employees array outside the loop
        int numEmployees = 0; // Declare numEmployees outside the loop
        while (true) {
            int choice ;
            System.out.println("Menu:");
            System.out.println("1. Create Employee");
            System.out.println("2. View Employee");
            System.out.println("3. Employee name starts with a given letter");
            System.out.println("4. Compare Employee Salaries");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();
            switch(choice){
                case 1 -> {
                    Emp emp = new Emp();
                    emp.createEmployee(employees, numEmployees, departments, numDepts); // Pass the employees array and numEmployees to createEmployee
                    employees[numEmployees] = emp; // Add the new employee to the array
                    numEmployees++; // Increment the number of employees                    
                }
                case 2 -> {
                    System.out.println("Enter Employee ID to view details: ");
                    int empId = scanner.nextInt();
                    boolean found = false;
                    for (int i = 0; i < numEmployees; i++) {
                        if (employees[i].getId() == empId) {
                            employees[i].displayEmployeeDetails(employees[i], departments, numDepts);
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        System.out.println("Employee with ID " + empId + " not found.");
                    }
                }
                case 3 -> {
                    System.out.println("Enter the letter to search for: ");
                    scanner.nextLine(); // Consume newline
                    String letter = scanner.nextLine();
                    System.out.println("Employees with names starting with '" + letter + "':");
                    for (int i = 0; i < numEmployees; i++) {
                        if (employees[i].isNameStartingWith(letter)) {
                            employees[i].displayEmployeeDetails(employees[i], departments, numDepts);
                        }
                    }
                }
                case 4 -> {
                    System.out.println("Enter the first Employee ID to compare: ");
                    int empId1 = scanner.nextInt();
                    System.out.println("Enter the second Employee ID to compare: ");
                    int empId2 = scanner.nextInt();
                    Emp emp1 = null, emp2 = null;
                    for (int i = 0; i < numEmployees; i++) {
                        if (employees[i].getId() == empId1) {
                            emp1 = employees[i];
                        }
                        if (employees[i].getId() == empId2) {
                            emp2 = employees[i];
                        }
                    }
                    if (emp1 != null && emp2 != null) {
                        if (emp1.compareSalary(emp2)) {
                            System.out.println("Employee " + emp1.getName() + " has a higher salary than Employee " + emp2.getName());
                        } else{
                            System.out.println("Employee " + emp2.getName() + " has a higher salary than Employee " + emp1.getName());
                        }
                    }
                }
                case 5 -> {
                    System.out.println("Exiting the program.");
                    scanner.close();
                    return;
                }
                default -> System.out.println("Invalid choice. Please try again.");
                 
            }
        }
    }
}