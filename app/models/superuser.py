import json
import datetime
import os

class SuperUser:
    FILE_PATH_USERS = "users.json"
    default_role = "SuperUser"

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

    def __str__(self):
        """Representacion en cadena de la clase User."""
        users = SuperUser.load_users()
        for self.username, user in users.items():
            hidden_password = '*' * len(user['password'])
            return f"User ID: {self.user_id}\n First Name: {self.first_name}\n Last Name: {self.last_name}\n Country: {self.country}\n City: {self.city}\n Postal Code: {self.postal_code}\n Address: {self.address}\n Email: {self.email}\n Phone Number: {self.phone_number} \n Username: {self.username}\n Password: {hidden_password}\n Role: {self.role}\n Created At: {self.created_at}\n Updated At: {self.updated_at}\n Deleted At: {self.deleted_at}"

    @staticmethod
    def create_file(file_path):
        """Crear un archivo JSON si no existe."""
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump({}, file)

    @staticmethod
    def load_users():
        """Cargar los usuarios desde el archivo JSON o crea uno primero si no existe."""
        if not os.path.exists("users.json"):
            SuperUser.create_file("users.json")
        try:
            with open(SuperUser.FILE_PATH_USERS, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def save_users(users):
        """Guardar los usuarios en el archivo JSON."""
        with open(SuperUser.FILE_PATH_USERS, "w") as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def view_users():
        """Mostrar todos los usuarios registrados."""
        users = SuperUser.load_users()
        for username, user in users.items():
            hidden_password = '*' * len(user['password'])
            print(f"User ID: {user['user_id']}\n Username: {user['username']}\n Password: {hidden_password}\n Email: {user['email']}\n Phone number: {user['phone_number']}")

    def register_user(self):
        """Registrar un nuevo usuario."""
        users = SuperUser.load_users()
        if self.username in users:
            raise ValueError("Username already exists.")
        for user in users.values():
            if self.email == user['email']:
                raise ValueError("Email already exists.")
            if self.phone_number == user['phone_number']:
                raise ValueError("Phone number already exists.")
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        users[self.user_id] = self.__dict__
        SuperUser.save_users(users)
        print("User registered successfully.")

    def update_user(self):
        """Actualizar los datos de un usuario existente."""
        users = SuperUser.load_users()
        if self.user_id in users:
            users[self.user_id] = self.__dict__
            SuperUser.save_users(users)
            print("User updated successfully.")
        else:
            print("User not found.")

    def delete_user(self):
        """Eliminar un usuario existente."""
        users = SuperUser.load_users()
        if self.user_id in users:
            del users[self.user_id]
            SuperUser.save_users(users)
            print("User deleted successfully.")
        else:
            print("User not found.")

    @staticmethod
    def login(user_id, username, password):
        """Iniciar sesión con un usuario existente."""
        users = SuperUser.load_users()
        if user_id in users and users[user_id]['username'] == username and users[user_id]['password'] == password:
            print(f"Logged in as {username}!")
            while True:
                if users[user_id]['role'] == SuperUser.default_role:
                    print("\n--- SuperUser Menu ---")
                    print("1. View users")
                    print("2. Create user")
                    print("3. Update user")
                    print("4. Delete user")
                    print("5. Logout")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        SuperUser.view_users()
                    elif choice == "2":
                        SuperUser.create_user_interactively()
                    elif choice == "3":
                        SuperUser.update_user_interactively()
                    elif choice == "4":
                        SuperUser.delete_user_interactively()
                    elif choice == "5":
                        break
                    else:
                        print("Invalid choice")
        else:
            print("Incorrect credentials")
    
    def get_user_password(password):
        users = SuperUser.load_users()
        for user in users.values():
            if user['password'] == password:
                return user
        return None

    def create_superuser_interactively():
        print("\n--- Register SuperUser ---")
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
                role=SuperUser.default_role
            )
            user.register_user()
        except ValueError as e:
            print(f"Error: {e}")

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
                password=password
            )
            user.register_user()
        except ValueError as e:
            print(f"Error: {e}")

    @staticmethod
    def find_by_id(user_id):
        users = SuperUser.load_users()
        for user in users.values():
            if user['user_id'] == user_id:
                return user
        return None

    @staticmethod
    def delete_user_interactively():
        """Interactúa con el usuario para eliminarlo."""
        print("\n--- Delete User ---")
        try:
            user_id = input("Enter the ID of the user to delete: ")
            user_data = SuperUser.find_by_id(user_id)
            if not user_data:
                print(f"User with ID {user_id} not found.")
                return
            
            user_to_delete = SuperUser(
                user_id=user_id,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                country=user_data['country'],
                city=user_data['city'],
                postal_code=user_data['postal_code'],
                address=user_data['address'],
                email=user_data['email'],
                phone_number=user_data['phone_number'],
                username=user_data['username'],
                password=user_data['password'],
                role=user_data['role'],  
                created_at=user_data['created_at'],  
                updated_at=user_data['updated_at'],  
                deleted_at=str(datetime.datetime.now())  
            )
            user_to_delete.delete_user()  
            print("User deleted successfully.")
        except Exception as e:
            print(f"Error deleting user: {e}")

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
