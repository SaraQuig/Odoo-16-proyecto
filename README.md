# Proyecto Odoo 16 - API Contacts

Descripción breve:  
Este es un proyecto desarrollado en **Odoo 16** con Python, PostgreSQL y dependencias configuradas para Windows. Incluye módulos personalizados y configuración básica lista para desarrollo.

---

## **Requisitos**
- Python 3.11 (o 3.10 compatible con Odoo 16)
- PostgreSQL 14 o 15
- Virtualenv (opcional pero recomendado)
- Git (para control de versiones)
- Dependencias de Odoo 16 (ver requirements.txt)

---

## **Instalación y configuración del entorno de trabajo**
1. Crear la carpeta de trabajo
2. mkdir odoo16
3. cd odoo16
4. Crea un entorno virtual: python -m venv venv
5. Activar el entorno virtual:
       En windows:  venv\Scripts\activate
       En linux:    source venv/bin/activate
7. Clonar el repositorio de odoo 16: git clone https://github.com/odoo/odoo.git -b 16.0
8. Crear carpeta de modulos personalizados: mkdir custom_addons
9. Crea el archivo de configuración odoo.conf en la carpeta general
10. Instala las dependencias (Asegurate de poner bien la contraseña y el usuario en el archivo odoo.conf):

    pip install -r odoo/requirements.txt

    pip install setuptools

    pip install PyJWT
    
12. clonar en custom_addons Módulos OCA requeridos (en server-auth entrar auth_jwt, ahi crear carpeta tools -> crear __init__.py y jwt_auth.py):

       git clone https://github.com/OCA/server-auth.git -b 16.0

       git clone https://github.com/OCA/rest-framework.git -b 16.0
       
13. Inicializa la base de datos: python odoo/odoo-bin -c odoo.conf -d nombre_base_de_datos --dev=all
14. No olvidarse de crear un JWT Validator en odoo, en settings, con la siguiente configuración:

    name: api
    audience: api
    Isuer: odoo
    Signature Type: Secret
    Key: MiClaveJWTsuperSegura123
    Algorithm: HS256 - HMAC using SHA-256
    User Id Strategy: Static
    Static User: Mitchell Admin
    
## **Crea tu módulo**
1. Crea módulo personalizado (MVC)

## **Instalación del módulo personalizado**
1. Entra a http://localhost:8069
2. Activa modo desarrollador
3. Ve a Aplicaciones → Actualizar lista de aplicaciones
4. Busca el nombre de tu módulo
5. Haz clic en Instalar
6. Busca auth_jwt y da clic en instalar

## **Prueba en Postam**

Para obtener el token (POST): http://localhost:8069/api/jwt/login

header: content-Type -> application/json

{
  "params": {
    "login": "tu_login",
    "password": "tu_password"
  }
}

Para crear contactos (POST): http://localhost:8069/api/contacts

header: content-Type -> application/json
       Autorization -> token
       
{
  "name": "nombre_contacto",
  "email": "correo_contacto@correo.com",
  "phone": "0999999999"
}

Obtener contactos (GET): http://localhost:8069/api/contacts

Header: Autorization -> Token

Actualizar un contacto (PUT): http://localhost:8069/api/contacts/41

header: content-Type -> application/json
       Autorization -> token
       
{
  "phone": "098888777",
  "email": "email.actualizado@mail.com"
}

Eliminar contacto (DELETE): http://localhost:8069/api/contacts/41?

Header: Autorization -> Token


   
