public class MainUserTable {
    @SuppressWarnings("resource")
    public static void main(String[] args) {
        java.util.Scanner sc = new java.util.Scanner(System.in);
        System.out.println("Welcome to the User Table Management System!");
        while (true) {
            System.out.println("Please choose an option:");
            System.out.println("1. Insert a new user");
            System.out.println("2. Find a user by ID");
            System.out.println("3. Delete a user by ID");
            System.out.println("4. Update a user's information");
            System.out.println("5. Exit");

            int choice = sc.nextInt();
            sc.nextLine(); // Consume the newline character

            switch (choice) {
                case 1:
		    System.out.println("Enter id to create user :");
                    int id = sc.nextInt();
                    sc.nextLine(); // Consume the newline character
		    System.out.println("Enter Name of the user :");
                    String name = sc.nextLine();
		    System.out.println("Enter Email of the user :");
                    String email = sc.nextLine();
                    UserTable user = new UserTable();
                    boolean result = user.insert(id, name, email);
                    if(result)
                        System.out.println("User created successfully....");
                    else
                        System.out.println("User has not created");
                    break;
                case 2:
                    System.out.println("Enter id to search :");
                    int searchId = sc.nextInt();
                    sc.nextLine(); // Consume the newline character
                    UserTable u = UserTable.findById(searchId);
                    if(u == null){
                        System.out.println("User not found with given id. Try again");
                        break;
                    }
                    break;
                case 3:
                    System.out.println("Enter id to delete :");
                    int deleteId = sc.nextInt();
                    sc.nextLine();
                    UserTable userToDelete = UserTable.findById(deleteId);
                    if(userToDelete == null){
                        System.out.println("User cannot be deleted...");
                        break;
                    }
                    userToDelete.delete(deleteId);
                    break;
                case 4:
		    System.out.println("Enter id of usrer to update their details :");
                    int idToUpdate = sc.nextInt();
                    sc.nextLine();
                    UserTable userToUpdate = UserTable.findById(idToUpdate);
                    if(userToUpdate == null){
                        System.out.println("User not found with given id. Try again");
                        break;
                    }
                    System.out.println("Enter new name :");
                    String nameToUpdate = sc.nextLine();
                    System.out.println("Enter new email :");
                    String emailToUpdate = sc.nextLine();
                    userToUpdate.update(nameToUpdate, emailToUpdate);
                    break;
                case 5:
                    System.out.println("Exiting the system. Goodbye!");
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }
}
