from models.user import User
from models.superuser import SuperUser
import os

def main():
    """Función principal para el menú de la aplicación."""
    while True:
        print("\n--- Homepage Menu ---")
        print("1. Register User")
        print("2. User Login")
        print("3. Register SuperUser")
        print("4. SuperUser Login") 
        choice = input("Choose an option (1, 2, 3, 4): ")

        if choice == '1':
            User.create_user_interactively()

        elif choice == '2':
            print("\n--- User Login ---")
            user_id = input("Enter user ID: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            User.login(user_id, username, password)

        elif choice == '3':
            SuperUser.create_superuser_interactively()

        elif choice == '4':
            print("\n--- SuperUser Login ---")
            user_id = input("Enter user ID: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            SuperUser.login(user_id, username, password)
    
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()