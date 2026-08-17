public class UserTable {
    static UserTable[] users = new UserTable[100];
    static int size = 0;

    private int id;
    private String name;
    private String email;

    static final UserTable DELETED = new UserTable();
    private java.util.Scanner sc = new java.util.Scanner(System.in);
    boolean insert(int id, String name, String email) {
        if (id <= 0) {
            System.out.println("User cannot have such ID");
            return false;
        }

        int index = hash(id);
        int deletedPos = -1;

        for (int i = 0; i < users.length; i++) {
            int pos = (index + i) % users.length;

            if (users[pos] == DELETED) {
                if (deletedPos == -1)
                    deletedPos = pos;
            }
            else if (users[pos] == null) {

                if (deletedPos != -1)
                    pos = deletedPos;

                this.id = id;
                this.name = name;
                this.email = email;

                users[pos] = this;
                size++;

                return true;
            }
            else if (users[pos].id == id) {
                System.out.println("User with given ID already exists.....");
                return false;
            }
        }

        // Table has no null slots, but a deleted slot is available
        if (deletedPos != -1) {
            this.id = id;
            this.name = name;
            this.email = email;

            users[deletedPos] = this;
            size++;

            return true;
        }

        System.out.println("Hash table is full");
        return false;
    }

    static UserTable findById(int id) {
        int index = hash(id);

        for (int i = 0; i < users.length; i++) {
            int pos = (index + i) % users.length;

            if (users[pos] == null) {
                return null;
            }

            if (users[pos] != DELETED && users[pos].id == id) {
                System.out.println("=============================");
                System.out.println("User with given id found !!");
                System.out.println("ID\t :" + users[pos].id);
                System.out.println("Name\t :" + users[pos].name);
                System.out.println("Email\t :" + users[pos].email);
                System.out.println("=============================");

                return users[pos];
            }
        }

        return null;
    }

    boolean delete(int id) {
        int index = hash(id);

        for (int i = 0; i < users.length; i++) {
            int pos = (index + i) % users.length;

            if (users[pos] == null) {
                return false;
            }

            if (users[pos] != DELETED && users[pos].id == id) {
		System.out.println("Press 0 to cancel, or any other key to continue deleting :");
		int choice = sc.nextInt();
		sc.nextLine(); //consumes next line
		if(choice == 0){
		    System.out.println("Deletion cancelled");
		    return false;
		}
                users[pos] = DELETED;
                size--;

                System.out.println("User deleted successfully");
                return true;
            }
        }

        return false;
    }

    boolean update(String newName, String newEmail) {
        if (newName.length() == 0 || newEmail.length() == 0) {
            System.out.println("Enter valid name or email...");
            return false;
        }

        this.name = newName;
        this.email = newEmail;

        return true;
    }

    static int hash(int id) {
        return id % users.length;
    }
}
