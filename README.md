# 🚗 AutoPy System - Gestión de Alquiler de Vehículos

**AutoPy System** es una aplicación de escritorio moderna y robusta desarrollada en Python, diseñada para automatizar la gestión operativa de una agencia de alquiler de vehículos. Este proyecto fue desarrollado como parte de la certificación técnica a docentes de programaciòn del **INATEC**.

---

## 📋 Características Principales

* **Seguridad:** Sistema de Login con encriptación de contraseñas (`bcrypt`) y manejo de roles (Administrador y Agente).
* **Interfaz Moderna:** Diseño UI/UX profesional con modo oscuro en el Login y Dashboard estilo "Enterprise" con accesos rápidos.
* **Gestión Integral (CRUD):**
    * **Clientes:** Registro y administración de cartera de clientes.
    * **Vehículos:** Control de flota, tarifas y estado de disponibilidad.
* **Rentas Transaccionales:** Registro de alquileres con validación automática de stock (impide rentar vehículos ocupados).
* **Reportes Avanzados:** Generación automática de archivos Excel (`.xlsx`) para inventarios y análisis de ventas.
* **Respaldo de Datos:** Herramienta integrada para crear y restaurar copias de seguridad de la base de datos SQLite.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.12
* **Interfaz Gráfica:** Tkinter (con estilos personalizados `ttk`).
* **Base de Datos:** SQLite 3 (Relacional).
* **Librerías Clave:**
    * `Pandas` & `OpenPyXL`: Generación de reportes Excel.
    * `Bcrypt`: Hashing y seguridad.
    * `Pillow (PIL)`: Manejo de imágenes y logotipos.

---

## 🚀 Instalación y Configuración

Sigue estos pasos para ejecutar el sistema en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/AutoPy-System.git](https://github.com/TU_USUARIO/AutoPy-System.git)

cd AutoPy-System

## Crear Entorno Virtual
## Es recomendable usar un entorno virtual para aislar las dependencias.
python -m venv .venv
.\.venv\Scripts\activate

## Instalar Dependencias
pip install -r requirements.txt

## Ejecutar la Aplicación

python main.py



