# Users Management System (UMS) for Bookings Application

<div align="center">
    <img src="ums/users/static/components/logo1.png" alt="Logo" style="width: 100px; height: 100px;">
</div>

<div align="left">
    <img src="https://img.shields.io/badge/technology-framework/language-darkorange" alt="Technology Badge">
</div>

## Table of contents

- [Description](#descripción)
- [Architecture](#Architecture)
- [Design](#Design)
- [Installation and Configuration](#instalación-y-configuración)
- [Uses](#uso)
- [Testing](#testing)
- [Contributions](#contribuciones)
- [License](#licencia)
- [Security](#política-de-seguridad)

---

## Description:
Sistema de Gestion de Usuarios (Users Management System - UMS) que funciona como sistema de administracion central de una aplicacion de reservas de instalaciones deportivas, dotando a los usuarios de permisos y autorizaciones para realizar acciones especificas y fiscalizadas por el programa.

## Architecture:
Considerando que la aplicacion cuenta con un elevado nivel de escalabilidad en virtud de la existencia de multiples usos futuros, los cuales son complementarios y derivados de su funcion principal de reservas y seran desarrollados e integrados como micro servicios, encontre necesaria la implementacion de una arquitectura que ademas de permitir la administracion de usuarios, contara con suficiente flexibilidad a la hora de adaptarse a los cambios necesarios de la aplicacion y, a pesar de que a priori y a grandes rasgos Django resulto ser el candidato electo ideal para el programa, fue prudente evaluar la compatibilidad y viabilidad del mismo con todo el proyecto, mediante un -superficial- Desk Research que me permitiera confirmar esta eleccion.

En la busqueda de aplicaciones que compartieran la implementacion de Django para una amplia gestion de sus usuarios, considerando principalmente la administracion de sus cuentas, perfiles, personalizacion, medios de pago, canales de comunicacion, permisos y autorizaciones de administracion de productos y servicios del usuario, entre otras funcionalidades, me encontre con las siguientes:

Booking: Se apoya en Django para administrar cuentas de usuarios, gestionar reservas en tiempo real y personalizar la experiencia de cada cliente según sus preferencias. Su uso demuestra como Django permite manejar la disponibilidad en tiempo real, funcionalidad clave para nuestro sistema de reservas.

Rappi y Glovo: Emplean Django para gestionar la autenticación, medios de pago y permisos en la administración de servicios. Esto refuerza la capacidad de Django para manejar roles como clientes o usuarios y proveedores o partners, además de facilitar la configuración de servicios desde el perfil del usuario.

Instagram: Utiliza Django como base para gestionar la autenticación, perfiles de usuario y su feed en tiempo real, además de facilitar el manejo eficiente de contenido multimedia como imágenes y videos. Su capacidad para manejar estas funcionalidades en una plataforma con millones de usuarios lo convierte en un ejemplo ideal para implementar feeds dinámicos y perfiles enriquecidos con fotos y videos personalizados. 

Spotify: Ha utilizado Django en la gestión de usuarios y en el desarrollo de APIs que manejan datos a gran escala. Esto valida el uso de Django para aplicaciones complejas que requieren integraciones con sistemas avanzados de análisis de datos y recomendaciones personalizadas.

Hasta aqui, a la luz de los fundamentos bajo analisis, se puede concluir en que Django permite un alto grado de escalabilidad, siendo ideal para proyectos con planes de expansión futura. Esto incluye funcionalidades como un feed de instalaciones en tiempo real según la ubicación del usuario y características de red social, donde los usuarios puedan conectarse, formar grupos o crear torneos. Además, facilita la integración de nuevas funcionalidades como rankings o análisis de datos, lo cual fundamenta tambien el uso de Django dentro del ecosistema de Python y su diversa variedad de librerias.

La gestión de usuarios de Django es robusta, ofrece un sistema integrado para autenticar, autorizar y asignar roles a los usuarios. Esto se alinea perfectamente con la necesidad de diferenciar entre clientes y proveedores, administrar permisos personalizados para reservas y gestionar perfiles con contenido multimedia como imágenes y videos de las instalaciones. En el caso de Instagram, este sirve como modelo para la creación y gestión de un sistema de usuarios escalable, con perfiles personalizables, feeds basados en intereses y sistemas de relaciones entre usuarios (grupos o "followers").

Django tambien se destaca por su seguridad, ofreciendo protección contra amenazas como CSRF, inyecciones SQL y XSS, además de un manejo seguro de contraseñas. Esto lo convierte en la elección ideal para proteger datos sensibles como métodos de pago y configuraciones personalizables en perfiles y fondos compartidos.

Como mencione anteriormente, la integración con herramientas modernas es otra ventaja significativa, puesto que gracias a Python, Django puede incorporar bibliotecas de Machine Learning e IA para recomendaciones personalizadas y optimización de horarios y tarifas según la demanda. También soporta análisis avanzado mediante bibliotecas como Pandas, lo que permite extraer insights a partir del uso de la plataforma.

Django facilita la creación de APIs modernas a través de Django REST Framework, permitiendo la integración fluida con aplicaciones móviles y web para mantener actualizados los datos en tiempo real. Esta capacidad es fundamental para un sistema que gestione reservas dinámicas y perfiles personalizables.

Además, la facilidad de mantenimiento y el desarrollo ágil que ofrece Django, gracias a su sistema de migraciones y arquitectura modular, asegura que el sistema pueda adaptarse rápidamente a nuevos requerimientos sin comprometer la estabilidad del proyecto.

Por ultimo, Django soporta funcionalidades adicionales como:
- Monitoreo y auditoría de acciones realizadas por los usuarios, como cambios en perfiles o historial de reservas, ofreciendo un registro claro para administradores. 
- Tambien permite la integración de pagos en línea mediante plataformas como Stripe o PayPal, facilitando la administración de fondos compartidos por turnos de reserva. 
- Ofrece funcionalidades avanzadas para comentarios y calificaciones, donde los usuarios pueden evaluar y opinar sobre instalaciones para mejorar el servicio.
- Facilita la implementación de notificaciones en tiempo real, enviando alertas sobre cambios en reservas, disponibilidad de instalaciones o mensajes entre usuarios.

En conclusión, Django no solo cumple con los requisitos actuales del sistema, sino que está diseñado para soportar una evolución natural hacia una aplicación más compleja y multifuncional, permitiendo gestionar usuarios, contenido multimedia, transacciones, y análisis de datos de manera eficiente y segura, por ello, he definido la arquitectura del programa de siguiente manera:

1) El sistema es un módulo central basado en Django, diseñado para gestionar usuarios como parte de un ecosistema más grande que incluye microservicios para reservas de instalaciones deportivas.
2) Se adoptó un enfoque modular y desacoplado para garantizar que el UMS funcione independientemente y exponga APIs claras para que otros microservicios interactúen con él.
3) Patrón arquitectónico MVC (Model-View-Controller), sin perjuicio de que Django ofrece un patron MVT (Model-View-Controller), ambos comparten caracteristicas similares que seran amalgamadas de manera organica en nuestro programa.
- Los modelos manejan la persistencia de datos.
- Las vistas gestionan la lógica de negocio y las respuestas.
- Los controladores (implícitos en Django como vistas basadas en funciones o clases) conectan los modelos y las plantillas.
4) Integracion con otros micro servicios:
- Es posible que se deban definir los endpoints RESTful para la integración con los microservicios mediante Django REST Framework (DRF) u otro/s metodos.
- La arquitectura permite escalar el sistema de usuarios sin afectar la lógica de los otros microservicios.
5) Componentes principales:
- Base de datos: SQLite/MySQL y PostgreSQL -Fundamentar uso de SQL- (configuraciones pendientes).
- Autenticación y autorización: Se utiliza el sistema integrado de Django para manejar permisos y roles.
- APIs: CRUD para usuarios y perfiles, con autenticación basada en tokens (JWT).
- Templates: En esta primera etapa se utilizan templates personalizados, con el uso de JSON Responses en lugar de solicitudes HTTP, dejando el uso de las mismas para eventuales modelos basados en Django Rest Framework, dado que estos han sido sustituidos por modelos personalizados con HTML, CSS Y JS.
- Formularios: Al igual que los modelos y plantillas ofrecidos por Django, los formularios no estan definidos en las clases, y se encuentran en los templates anteriormente descriptos, utilizando en algunas circunstancias Bootstrap para una mejor integracion y posible re utilizacion de los mismos readecuandolos segun cada necesidad, externa o interna a nuestro programa.

Para más detalles sobre la arquitectura del sistema, consulta los diagramas en la carpeta -Agregar carpeta docs/documents- [`documents`](./documents).
- [Diagrama entidad-relación](./documents/er_diagram.mmd)
- Data Base Standardization (Agregar archivo xlsx)

## Design
1) Organizacion de directorios: El programa cuenta con la siguiente arquitectura limpia y modular.
- `ums/`:
- `ums/ums`: Configuración del proyecto.
- `ums/users/`: Modelos, vistas, serializadores, apps.
- `tests/`: Pruebas unitarias e integración.
2) Modelos, atributos, atributos de clases, metodos:
- `UserManager`:
- `User`: Modelo principal para gestionar usuarios.
- `Profile`: Se extiende sobre el modelo `User` para manejar sus datos adicionales.
3) Endpoints REST y/u otros metodos (Admin., pendientes de inclusion):
- `GET /users/`: Lista de usuarios.
- `POST /users/`: Crear usuario.
- `PUT /users/<id>/`: Actualizar usuario.
- `DELETE /users/<id>/`: Eliminar usuario.
4) Logica de Negocio (Redireccion a 'project branch'):
5) Estilo de codificacion:
- Separación de responsabilidades: Cada módulo tiene una única responsabilidad.
- Reutilización de código: Tentativamente, se pretende seguir el principio DRY con el uso de mixins en vistas basadas en clases para reducir redundancias.
- Escalabilidad: La aplicación está diseñada para integrarse fácilmente con otros servicios.
6) Componentes principales:
Para más detalles sobre el diseno del sistema, consulta los diagramas en la carpeta -Agregar carpeta docs/documents- [`documents`](./documents)
- [Diagrama de flujo de datos](./documents/data_flow_diagram.drawio)
- [Diagrama de clases](./documents/class_diagram.puml)


## Installation and Configuration
Sigue estos pasos para instalar y ejecutar el programa localmente.

## Use

## Testing

## Contributions

## License

## Security 

