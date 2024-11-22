import os
import json
import datetime
from dateutil import parser

"""Este archivo debe ejecutarse desde su carpeta ya que no tiene el mismo
funcionamiento que el archivo 'main.py', ni tampoco los mismos atributos de la
clase 'User', solo funciones y logica de todo el negocio como una guia para el 
desarrollo de la aplicacion. (Leer README.md)"""

logged_in_user = None
facility_name = None
FILE_PATH_USERS = "users.json"

 
def create_file(file_path):
    """Funcion para crear un archivo JSON si no existe"""
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({}, file)

def load_users():
    """Funcion para cargar datos desde el archivo JSON o crearlo antes si no existe"""
    if not os.path.exists("users.json"):
        create_file("users.json")
    with open("users.json", "r") as file:
        return json.load(file)

def save_users(users):
    """Funcion para guardar usuarios en el archivo JSON"""
    with open("users.json", "w") as file:
        json.dump(users, file)

def view_users():
    """Funcion para mostrar todos los usuarios"""
    users = load_users()
    for username, user in users.items():
        hidden_password = '*' * len(user['Password'])
        print(f"Username: {username}, Password: {hidden_password}, Email: {user['Email']}, Phone number: {user['PhoneNumber']}")

def user_exists(username):
    """Funcion para verificar si el nombre de usuario ya existe"""
    users = load_users()
    return username in users

def email_exists(email):
    """Funcion para verificar si el email ya esta registrado"""
    users = load_users()
    for user in users.values():
        if user.get("Email") == email:
            return True
    return False

def phone_number_exists(phone_number):
    """Funcion para verificar si el numero de telefono ya esta registrado"""
    users = load_users()
    for user in users.values():
        if user.get("PhoneNumber") == phone_number:
            return True
    return False

def validate_password():
    """Funcion para validar que la contraseña tenga al menos 8 caracteres"""
    while True:
        password = input("Password (at least 8 characters): ")
        if len(password) >= 8:
            return password
        else:
            print("Password must be at least 8 characters long. Please try again.")

def register_user(username, password, email, phone_number):
    """Funcion para registrar el usuario en el archivo JSON"""
    users = load_users()
    users[username] = {
        "Password": password,
        "Email": email,
        "PhoneNumber": phone_number
    }
    save_users(users)
    print("Registration successful! Please verify your account.")

def validate_and_register_user():
    """Funcion para validaciones antes de registrar un nuevo usuario y registrarlo
y no tener que repetir codigo con peticiones de datos"""
    username = input("Username: ")
    while user_exists(username):
        print("Username already exists. Here is a list of usernames in use:")
        print(", ".join(load_users().keys()))
        username = input("Please enter a different username: ")
    password = validate_password()
    email = input("Email: ")
    while email_exists(email):
        print("Email already in use. Please use a different email.")
        email = input("Email: ")
    phone_number = input("Phone Number: ")
    while phone_number_exists(phone_number):
        print("Phone number already in use. Please use a different phone number.")
        phone_number = input("Phone Number: ")
    register_user(username, password, email, phone_number)

def login(username, password):
    """Funcion para iniciar la sesion verificando credenciales"""
    users = load_users()
    if username in users and users[username]["Password"] == password:
        return "Login successful"
    return "Incorrect credentials"

def admin_menu():    
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Users")
        print("2. View Facilities")
        print("3. View Bookings")
        print("4. Back")        
        choice = input("Choose an option (1, 2, 3, 4): ")
        if choice == '1':
            view_users()
        elif choice == '2':
            view_facilities()
        elif choice == '3':
            view_bookings()
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")

def handle_login():
    """Funcion para controlar el login y no tener que repetir codigo, no hace
    falta llamar a la funcion login"""
    users = load_users()
    username = input("Username: ")
    password = input("Password: ")
    if username in users and users[username]["Password"] == password:
        print(f"Logged in as {username}!")
        while True:
            print("\n--- Profile Menu ---")
            print("3. Exit")
            print("4. Admin Menu")
            print("5. Bookings Menu")
            print("6. Facilities Menu")

            choice = input("Choose an option (3, 4): ")
            if choice == '3':
                print("Exiting the program.")
                break
            elif choice == '4':
                admin_menu()
            elif choice == '5':
                handle_bookings()
            elif choice == '6':
                handle_facilities()
            else:
                print("Invalid option, please try again.")

    else:
        print("Incorrect credentials.")

def load_facilities():
    """Funcion para cargar facilities desde el archivo JSON"""
    with open("facilities.json", "r") as file:
            return json.load(file)
        
def save_facilities(facilities):
    """Funcion para guardar facilities en el archivo JSON"""
    with open("facilities.json", "w") as file:
        json.dump(facilities, file)
        
def view_facilities():
    """Funcion para mostrar todas las facilities"""
    facilities = load_facilities()
    for facility_name, facility in facilities.items():
        print(f"Facility name: {facility_name}, Adress: {facility['Adress']}, PhoneNumber: {facility['PhoneNumber']}, Description: {facility['Description']}")

def facility_exists(facility_name):
    """Funcion para verificar si el nombre de la facilitie ya existe"""
    facilities = load_facilities()
    return facility_name in facilities

def create_facility(facility_name, adress, phone_number, description):
    """Funcion para registrar la facilitie en el archivo JSON"""
    facilities = load_facilities()
    facilities[facility_name] = {
        "Adress": adress,
        "PhoneNumber": phone_number,
        "Description": description
    }
    save_facilities(facilities)
    print("Facility creation was successful!")

def load_shifts():
    """Carga los turnos disponibles desde un archivo JSON o devuelve un diccionario vacío si el archivo está vacío."""
    try:
        with open("shifts.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("El archivo de turnos está vacío o corrupto. Se iniciará con una estructura vacía.")
        return {}
    except FileNotFoundError:
        print("El archivo de turnos no existe. Creando uno nuevo.")
        return {}

def save_shifts(shifts):
    with open("shifts.json", "w") as file:
        json.dump(shifts.values(), file)  

def view_shifts(shifts):    
    shifts = load_shifts()
    for shift_id, shift in shifts.items():
        if isinstance(shift, dict):
            print(shift_id, shift["Username"], shift["Facility Name"], shift["Start Time (YYYY-MM-DDTHH:MM:SS)"], shift["End Time (YYYY-MM-DDTHH:MM:SS)"])
        else:
            print("Formato de datos incorrecto para el shift:", shift_id)

def shift_exists(shift_id, facility_name, start_time, end_time):
    shifts = load_shifts()
    return (shift_id,facility_name, start_time, end_time) in shifts

def create_shifts(shift_id, logged_in_user, facility_name, start_time, end_time):
    """Solicitar start_time y end_time en un formato específico"""
    shifts = load_shifts()

    if shift_id in shifts == True:  
        """Usar dateutil.parser para parsear las fechas"""
    try:
        start_time = parser.parse(start_time)
        end_time = parser.parse(end_time)
    except ValueError:
        print("Error: el formato de fecha y hora debe ser 'YYYY-MM-DDTHH:MM:SS'")
        return
    """Convertir a cadena ISO 8601 para almacenar en JSON"""
    start_time = start_time.isoformat()
    end_time = end_time.isoformat()
    shifts[shift_id] = {
            "Username": logged_in_user,
            "Facility Name": facility_name,
            "Start Time (YYYY-MM-DDTHH:MM:SS)": start_time,
            "End Time (YYYY-MM-DDTHH:MM:SS)": end_time
        }
    save_shifts(shifts)
    print("Shift creation was successful!")

def handle_shifts():
    while True:
        print("\n--- Shifts Menu ---")
        print("1. Create Shift")
        print("2. View Shifts")
        print("3. Back")
        choice = input("Choose an option (1, 2, 3): ")
        if choice == '1':
            shift_id = input("Shift ID: ")
            facility_name = input("Facility Name: ")
            start_time = input("Start Time (YYYY-MM-DDTHH:MM:SS): ")
            end_time = input("End Time (YYYY-MM-DDTHH:MM:SS): ")
            create_shifts(shift_id, logged_in_user, facility_name, start_time, end_time)
        elif choice == '2':
            view_shifts()
        elif choice == '3':
            break
        else:
            print("Invalid option, please try again.")

def validate_and_register_facilities():
    """Funcion para validaciones antes de registrar una nueva facilitie y registrarla
sin tener que repetir codigo con peticiones de datos"""
    facility_name = input("Facility name: ")
    while facility_exists(facility_name):
        print("Facility name already exists. Here is a list of facilities in use:")
        print(", ".join(load_facilities().keys()))
        facility_name = input("Please enter a different facility name: ")
    adress = input (str("Adress: "))
    phone_number = int(input("PhoneNumber: "))
    description = input (str ("Description: "))
    create_facility(facility_name, adress, phone_number, description)

def handle_facilities():    
    while True: 
        print("\n--- Facilities Menu ---")    
        print("1. Create facilitie")    
        print("2. Show Facilities")    
        print("3. Back")    
        choice = input("Choose an option (1, 2, 3): ")    
        if choice == '1':    
            validate_and_register_facilities()
            print("Lets create a new shift")
            print("1. Create Shifts")
            print("2. View My Shifts")   
            print("3. Back") 
            choice = input("Choose an option (1, 2, 3): ")
            if choice == '1':
                handle_shifts()
            elif choice == '2':
                view_shifts()
            elif choice == '3':
                break
        elif choice == '2':    
            view_facilities() 
            print("1. Create Shifts")
            print("2. Edit My Shifts")   
            print("3. Back") 
            choice = input("Choose an option (1, 2, 3): ")
            if choice == '1':
                view_shifts(shifts=load_shifts())
                shift_id = input("Shift ID: ")
                facility_name = input("Facility Name: ")
                start_time = input("Start Time (YYYY-MM-DDTHH:MM:SS): ")
                end_time = input("End Time (YYYY-MM-DDTHH:MM:SS): ")
                create_shifts(shift_id, logged_in_user, facility_name, start_time, end_time)
            elif choice == '2':
                view_shifts(shifts=load_shifts())
        elif choice == '3':    
            break    
        else:    
            print("Invalid option, please try again.")

def load_bookings():
    """Carga las reservas desde un archivo JSON o devuelve un diccionario vacío si el archivo está vacío."""
    try:
        with open("bookings.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("El archivo de reservas está vacío o corrupto. Se iniciará con una estructura vacía.")
        return {}
    except FileNotFoundError:
        print("El archivo de reservas no existe. Creando uno nuevo.")
        return {}

def save_bookings(bookings):
    """Funcion para guardar bookings en el archivo JSON"""
    with open("bookings.json", "w") as file:
        json.dump(bookings, file)

def view_bookings():    
    """Funcion para mostrar todas las bookings"""
    bookings = load_bookings()
    for booking_id, booking in bookings.items():    
        print(f"Booking ID: {booking_id}")    
        print(f"Customer: {booking['username']}")    
        print(f"Facility: {booking['facility']}")    
        print(f"Start Time: {booking['start_time']}")    
        print(f"End Time: {booking['end_time']}")    
        print()

def view_available_shifts():
    """Función para mostrar las reservas disponibles"""
    shifts = load_shifts() 
    if not shifts:
        print("No hay turnos disponibles.")
        return

    print("Reservas Disponibles:")
    for shift_id, details in shifts.items():
        print(f"ID: {shift_id}")
        print(f"Host: {details['customer']}")
        print(f"Instalación: {details['facility']}")
        print(f"Fecha de inicio: {details['start_time']}")
        print(f"Fecha de fin: {details['end_time']}")
        print("-" * 20)


def make_booking(shift_id, logged_in_user, facility_name, start_time, end_time):
    """Función para registrar una nueva reserva en el archivo JSON"""
    if shift_id in load_shifts() == True:

        """Usar dateutil.parser para parsear las fechas"""
    try:
        start_time = parser.parse(start_time)
        end_time = parser.parse(end_time)
    except ValueError:
        print("Error: el formato de fecha y hora debe ser 'YYYY-MM-DDTHH:MM:SS'")
        return

    """Convertir a cadena ISO 8601 para almacenar en JSON"""
    start_time = start_time.isoformat()
    end_time = end_time.isoformat()

    bookings = load_shifts()
    bookings[shift_id] = {
        "username": logged_in_user,
        "facility": facility_name,
        "start_time": start_time,
        "end_time": end_time
    }

    save_bookings(bookings)
    print("Booking creation was successful!")

def handle_bookings():    
    while True:    
        print("\n--- Bookings Menu ---")    
        print("1. View Shifts")       
        print("2. Back")    
        choice = input("Choose an option (1, 2): ")    
        if choice == '1':        
            shifts = load_shifts()
            view_shifts(shifts)
            shift_id = input("Shift ID: ")
            if shift_id in shifts:
                for shift_id, shift in shifts.items():
                    if isinstance(shift, dict):
                        getattr(shift_id, shift["Start Time (YYYY-MM-DDTHH:MM:SS)"], shift["End Time (YYYY-MM-DDTHH:MM:SS)"])
                        make_booking(shift_id, shift["Username"], shift["Facility Name"], shift["Start Time (YYYY-MM-DDTHH:MM:SS)"], shift["End Time (YYYY-MM-DDTHH:MM:SS)"])
        elif choice == '2':    
            break    
        else:    
            print("Invalid option, please try again.")

def standarize_users(FILE_PATH_USERS):
    """Funcion para standarizar los usuarios del archivo JSON porque hasta esta 
    etapa del codigo ya hemos agregado mas atributos a los usuarios y debemos
    corregir las claves faltantes. Atributos a agregar: Fecha de nacimiento, 
    DNI, etc. Tambien habra que standarizar las demas clases"""
    required_keys = {
        "user_id": None,
        "first_name": "",
        "last_name": "",
        "country": "",
        "city": "",
        "postal_code": "",
        "address": "",
        "email": "",
        "phone_number": "",
        "username": "",
        "password": "",
        "role": None,
        "created_at": None,
        "updated_at": None,
        "deleted_at": None
    }
    """Cargar usuarios desde el archivo JSON."""
    try:
        with open(FILE_PATH_USERS, "r") as file:
                users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
                users = {}
    """Agregar claves faltantes."""
    for username, user_data in users.items():
        for key, default_value in required_keys.items():
            if key not in user_data:
                        user_data[key] = default_value

    """Guardar usuarios normalizados"""
    with open(FILE_PATH_USERS, "w") as file:
            json.dump(users, file, indent=4)

    print("Users standardization was successful.")

def main():
    """Funcion main/principal"""
    while True:
        print("\n--- Homepage Menu ---")
        print("1. Register")
        print("2. Login")
        choice = input("Choose an option (1, 2): ")
        if choice == '1':
            validate_and_register_user()
        elif choice == '2':
            handle_login()
        else:
            print("Invalid option, please try again.")
if __name__ == "__main__":
    main()