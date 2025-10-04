# Dashboard de Gestión de Productos

Este proyecto es una aplicación web completa construida con Flask que sirve como un dashboard para visualizar y gestionar datos de productos. La aplicación consume datos de cuatro APIs externas diferentes, los enriquece y los presenta en una interfaz de usuario amigable, al mismo tiempo que expone su propia API Gateway para un acceso a datos centralizado.

## Arquitectura

La aplicación está diseñada con una arquitectura desacoplada que separa la interfaz de usuario del acceso a los datos, todo dentro de una única aplicación Flask para facilitar el despliegue.

1.  **Aplicación Principal (UI - `app.py`)**:

    - Es el punto de entrada principal.
    - Se encarga de renderizar todas las plantillas HTML.
    - Maneja la lógica de los formularios para las operaciones CRUD (Crear, Leer, Actualizar, Borrar).
    - Para obtener los datos necesarios para las vistas, llama directamente a los módulos `api_clients`.

2.  **API Gateway (Blueprint - `gateway.py`)**:

    - Está implementado como un Flask Blueprint y se registra en la aplicación principal bajo el prefijo `/api`.
    - Centraliza toda la comunicación con las 4 APIs externas.
    - Expone endpoints JSON limpios (ej. `/api/products`, `/api/categories`) que otros servicios pueden consumir.
    - Realiza la lógica de negocio de combinar y enriquecer los datos de las diferentes fuentes.

3.  **Clientes de API (`api_clients/`)**:
    - Cada archivo en este directorio es responsable de la comunicación con una API externa específica. Esto mantiene el código organizado y modular.

## Características

- **CRUD Completo:** Gestión total de Productos y Categorías.
- **Creación de Marcas:** Funcionalidad para añadir nuevas marcas.
- **Validación de Unidades:** Herramientas para probar la lógica de negocio de la API de unidades.
- **API Gateway Integrada:** Expone una API JSON centralizada en el endpoint `/api`.
- **Lista para Despliegue:** Configurada con Docker y Gunicorn para un despliegue sencillo en plataformas como Render.

## Instalación Local

Para ejecutar el proyecto en tu máquina local, sigue estos pasos:

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/CarlTheBoss/FRONTEND-DEFINITIVO.git
    cd <NOMBRE-DEL-DIRECTORIO>
    ```

2.  **Crea un entorno virtual (recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python app.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000`.

## Despliegue en Render

El proyecto está listo para ser desplegado usando Docker.

1.  **Sube tu código a un repositorio de GitHub.**
2.  En [Render](https://render.com), crea un nuevo **"Web Service"** y conéctalo a tu repositorio.
3.  Render detectará automáticamente el `Dockerfile` y configurará el entorno.
4.  El despliegue se iniciará automáticamente. Una vez completado, Render te proporcionará la URL pública de tu aplicación.

## Estructura de Archivos

```
.
├── app.py              # Aplicación principal de Flask (UI y registro de Blueprint)
├── gateway.py          # Blueprint del API Gateway (lógica de datos)
├── Dockerfile          # Instrucciones para construir la imagen de producción
├── requirements.txt    # Dependencias de Python
├── api_clients/        # Módulos para comunicarse con las APIs externas
│   ├── __init__.py
│   ├── api1_client.py  # Productos
│   ├── api2_client.py  # Categorías
│   ├── api3_client.py  # Marcas
│   └── api4_client.py  # Unidades
├── templates/          # Plantillas HTML
│   ├── index.html
│   ├── product_form.html
│   ├── category_form.html
│   └── brand_form.html
└── static/             # Archivos estáticos
    └── css/
        └── style.css
```
