import requests

API_URL = "https://api-categoria-a8hp.onrender.com/categorias"

def get_all_categories():
    """
    Obtiene todas las categorías de la API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Categorías: {e}")
        return []

def get_category_by_id(category_id):
    """
    Obtiene una categoría específica por su ID.
    """
    try:
        response = requests.get(f"{API_URL}/{category_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la categoría {category_id}: {e}")
        return None

def create_category(category_data):
    """
    Crea una nueva categoría usando una solicitud POST.
    """
    try:
        response = requests.post(API_URL, json=category_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al crear la categoría: {e}")
        return None

def update_category(category_id, category_data):
    """
    Actualiza una categoría existente usando una solicitud PUT.
    """
    try:
        response = requests.put(f"{API_URL}/{category_id}", json=category_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar la categoría {category_id}: {e}")
        return None

def delete_category(category_id):
    """
    Elimina una categoría por su ID usando una solicitud DELETE.
    """
    try:
        response = requests.delete(f"{API_URL}/{category_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar la categoría {category_id}: {e}")
        return None