import json
import datetime
import os
from models.superuser import SuperUser

class User:
    FILE_PATH_USERS = "users.json"
    default_role = "Customer"
    alt_role = "Provider"

    def __init__(self, user_id, first_name, last_name, country, city, postal_code, address, email, phone_number, username, password, role=default_role, created_at=None, updated_at=None, deleted_at=None):
        """Constructor de la clase User."""
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.password = password
        self.role = role
        self.created_at = created_at or str(datetime.datetime.now())
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @staticmethod
    def login(user_id, username, password):
        """Iniciar sesión con un usuario existente."""
        users = SuperUser.load_users()
        if user_id in users and users[user_id]['username'] == username and users[user_id]['password'] == password:
            print(f"Logged in as {username}!")
            while True:
                if users[user_id]['role'] == User.alt_role:
                    print("\n--- Provider Menu ---")
                    print("1. Administer Facilities")
                    print("2. Logout")
                    choice = input("Enter your choice:")
                    if choice == "1":
                        print("\n--- Facilities Menu ---")
                        print("1. View Facilities")
                        print("2. Create Facility")
                        print("3. Update Facility")
                        print("4. Delete Facility")
                        print("5. Logout")
                        choice = input("Enter your choice: ")
                    elif choice == "2":
                        break
                elif users[user_id]['role'] == User.default_role:
                    print("\n--- Customer Menu ---")
                    print("1. Booking")
                    print("2. Settings")
                    print("3. Logout")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        print("\n--- Shifts View ---")
                        print("1. Select Shift")
                        print("2. Logout")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            print("\n--- Shifts Views ---")
                            print("1. Make Booking")
                            print("2. Logout")
                            choice = input("Enter your choice: ")
                        elif choice == "2":
                            break
                    elif choice == "2":
                        print("\n--- Settings Menu ---")
                        print("1. Update User")
                        print("2. Delete My Account")
                        print("3. Logout")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            User.update_user_interactively()
                        elif choice == "2":
                            User.delete_my_account()    
                    elif choice == "3":
                        break
        else:
            print("Incorrect credentials")
    
    @staticmethod
    def create_user_interactively():
        """Captura los datos de usuario desde la entrada estándar y crea un usuario."""
        print("\n--- Register User ---")
        try:
            user_id = input("Enter user ID: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            country = input("Enter country: ")
            city = input("Enter city: ")
            postal_code = input("Enter postal code: ")
            address = input("Enter address: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")
            username = input("Enter username: ")
            password = input("Enter password: ")

            user = SuperUser(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                country=country,
                city=city,
                postal_code=postal_code,
                address=address,
                email=email,
                phone_number=phone_number,
                username=username,
                password=password,
                role=User.default_role
            )
            user.register_user()
        except ValueError as e:
            print(f"Error: {e}")

    def delete_my_account():
        """Elimina la cuenta del usuario actual."""
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        users = SuperUser.get_user_password(password)
        if username in users and users[password]['password'] == password:
            SuperUser.delete_user(username, password)
            print("Account deleted successfully.")
        else:
            print("Incorrect username or password.")


    @staticmethod
    def update_user_interactively():
        """Interactúa con el usuario para actualizar los datos."""
        print("\n--- Update User ---")
        try:
            user_id = input("Enter the ID of the user to update: ")
            user_data = SuperUser.find_by_id(user_id)
            if not user_data:
                print(f"User with ID {user_id} not found.")
                return

            print("Leave a field blank to keep the current value.")
            first_name = input(f"Enter first name [{user_data['first_name']}]: ") or user_data['first_name']
            last_name = input(f"Enter last name [{user_data['last_name']}]: ") or user_data['last_name']
            country = input(f"Enter country [{user_data['country']}]: ") or user_data['country']
            city = input(f"Enter city [{user_data['city']}]: ") or user_data['city']
            postal_code = input(f"Enter postal code [{user_data['postal_code']}]: ") or user_data['postal_code']
            address = input(f"Enter address [{user_data['address']}]: ") or user_data['address']
            email = input(f"Enter email [{user_data['email']}]: ") or user_data['email']
            phone_number = input(f"Enter phone number [{user_data['phone_number']}]: ") or user_data['phone_number']
            username = input(f"Enter username [{user_data['username']}]: ") or user_data['username']
            password = input(f"Enter password [{user_data['password']}]: ") or user_data['password']

            updated_user = SuperUser(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                country=country,
                city=city,
                postal_code=postal_code,
                address=address,
                email=email,
                phone_number=phone_number,
                username=username,
                password=password,
                role=user_data['role'],  
                created_at=user_data['created_at'],  
                updated_at=str(datetime.datetime.now())  
            )
            updated_user.update_user()  
            print("User updated successfully.")
        except Exception as e:
            print(f"Error updating user: {e}")
