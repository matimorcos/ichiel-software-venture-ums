# Users CRUD as UMS for a booking App

<div align="center">
    <img src="ums/users/static/components/logo1.png" alt="Logo" style="width: 100px; height: 100px;">
</div>

<div align="left">
    <img src="https://img.shields.io/badge/technology-framework/language-darkorange" alt="Technology Badge">
</div>

## Table of contents

- [Description](#descripción)
- [Architecture and Design](#arquitectura-y-diseño)
- [Components Diagram](#diagrama-de-componentes)
- [Installation and Configuration](#instalación-y-configuración)
- [Uses](#uso)
- [Testing](#testing)
- [Contributions](#contribuciones)
- [License](#licencia)
- [Security](#política-de-seguridad)

---

## Description:
Users Management System (UMS) como sistema central para la administracion de usuarios de una aplicacion dedicada a la reserva de instalaciones deportivas, las cuales, a la vez, pueden ser proveidas por los mismos usuarios de la aplicacion, estableciendose dos posibles roles para estos, el rol Customer y el rol Provider.

Para llevar a cabo esta primera etapa del desarrollo del programa, encontre necesaria la creacion de 2 diferentes clases que se encuentran en el modulo models:

Clase SuperUser (SuperUser.py): Enfocada en la gestion y control de las interacciones del usuario con la aplicacion.

Clase User (User.py): Contiene los permisos y accesos necesarios para que los usuarios interactuen con la aplicacion, concretando sus funciones a traves de metodos definidos en la clase SuperUsuario, desde la cual se controla el flujo, esto porque la aplicacion debe permitirle al usuario gestionar sus datos sin complicaciones. Esta clase contempla dos roles para los usuarios de la aplicacion mencionados anteriormente, como default_role tenemos a Customer, y como alt_role tenemos a Provider, cada uno con su menu definido al iniciar sesion (leer iteraciones pendientes).

La clase SuperUser puede absorver a la clase User en una sola, dependiendo de como decida ser la dinamica de la app en un futuro, y si en lugar de requerir la insercion de los datos del cliente a traves de la clase User lo hacemos por un formulario directamente desde el frontend con HTML y JS.

## Architecture and Design
El proyecto está estructurado en módulos que cumplen roles específicos dentro de la arquitectura:

- **`order_services`**: Gestiona la lógica de negocio de las órdenes, permitiendo crear, actualizar y gestionar órdenes.
- **`email_services`**: Responsable de la configuración y el envío de notificaciones por correo electrónico.
- **`db_services`**: Maneja la conexión y los modelos de la base de datos, proporcionando una capa de abstracción para los datos.

Esta estructura permite mantener cada módulo desacoplado, facilitando el mantenimiento y la escalabilidad del sistema. 

Para más detalles sobre la arquitectura del sistema, consulta los diagramas en la carpeta [`documents`](./documents).

## Components Diagram
Para visualizar los diferentes flujos y relaciones del sistema, los siguientes diagramas están disponibles en la carpeta [`documents`](./documents):

- [Diagrama de flujo de datos](./documents/data_flow_diagram.drawio)
- [Diagrama de clases](./documents/class_diagram.puml)
- [Diagrama entidad-relación](./documents/er_diagram.mmd)

## Installation and Configuration
Sigue estos pasos para instalar y ejecutar el proyecto localmente.

## Use
Para ejecutar la app, abrir el archivo main.py posicionados en su carpeta, y ejecutarlo, o desde la terminal: python main.py. El programa guarda por defecto los cambios en el archivo users.json, de no hallarlo en su modulo creara uno automaticamente, en este caso, este archivo se encuentra en el directorio raiz con lo cual se dara el segundo caso.

Archivo funcions.py: Contiene la logica de negocio, se recomienda utilizarlo como guia.

Iteraciones:
Roles del Usuario:
Los roles de la clase User podrian heredarse en dos clases diferentes, Customer y Provider, manteniendose User como base, y estas dos segun el caso de uso por el usuario, o por otro lado, podrian mantenerse dichos roles y anadirse los casos de uso y manejo en la clase SuperUser para que administre estas interacciones que pueden ser simultaneas en un mismo usuario, es decir, un usuario puede proveer una instalacion y a la vez ser consumidor de una.

Clases:
La posible iteracion descripta ut supra, aun sin definirse, despierta la duda de si sera necesaria la creacion de las clases Facility (Instalacion), Shifts(Turnos ofrecidos por el Provider) y Bookings(Reservas realizadas por el Customer), o la combinacion de las mismas dentro de las hipoteticas clases Customer y Provider, o incluso, la integracion de de Shifts y Bookings como una instancia de la clase independiente Facility.

Seguridad:
Prevenciones pendientes.

Atributos:
Como atributos pendientes de anadirse a la clase User se encuentran: user_dni (o documentacion que acredite identidad), fecha de nacimiento (para impedimento de registro y restriccion de determinados permisos y accesos a menores de edad).

## Testing
Errores:
Como unico error tecnico en esta version del programa, se observo la imposibilidad del usuario Customer de eliminar su propia cuenta.

## Contributions

## License

## Security 
Prevenciones pendientes.

