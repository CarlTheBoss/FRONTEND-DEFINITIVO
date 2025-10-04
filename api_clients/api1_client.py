import requests

API_URL = "https://8080-firebase-product-service-java-1759371536787.cluster-fsmcisrvfbb5cr5mvra3hr3qyg.cloudworkstations.dev/api/v1/products"

def get_all_products():
    """
    Obtiene todos los productos de la API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Productos: {e}")
        return []

def get_product_by_id(product_id):
    """
    Obtiene un producto específico por su ID.
    """
    try:
        response = requests.get(f"{API_URL}/{product_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el producto {product_id}: {e}")
        return None

def update_product(product_data):
    """
    Actualiza un producto existente usando una solicitud PUT.
    """
    try:
        response = requests.put(API_URL, json=product_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar el producto: {e}")
        return None

def create_product(product_data):
    """
    Crea un nuevo producto usando una solicitud POST.
    """
    try:
        response = requests.post(API_URL, json=product_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al crear el producto: {e}")
        return None

def delete_product(product_id):
    """
    Elimina un producto por su ID usando una solicitud DELETE.
    """
    try:
        response = requests.delete(f"{API_URL}/{product_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar el producto {product_id}: {e}")
        return None