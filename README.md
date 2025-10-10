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
8. Craer carpeta de modulos personalizados: mkdir custom_addons
9. Crea el archivo de configuración odoo.conf en la carpeta general
10. Instala las dependencias (Asegurate de poner bien la contraseña y el usuario en el archivo odoo.conf): pip install -r odoo/requirements.txt
11. Inicializa la base de datos: python odoo/odoo-bin -c odoo.conf -d nombre_base_de_datos --dev=all

##**Crea tu módulo**
1. Crea tu primer módulo personalizado (MVC)

##**Instalación del módulo personalizado**
1. Entra a http://localhost:8069
2. Activa modo desarrollador
3. Ve a Aplicaciones → Actualizar lista de aplicaciones
4. Busca el nombre de tu módulo
5. Haz clic en Instalar
   
