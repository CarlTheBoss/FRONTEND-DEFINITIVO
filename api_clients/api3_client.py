import requests

API_URL = "https://apimarcas.onrender.com/api/marcas"

def get_all_brands():
    """
    Obtiene todas las marcas de la API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Marcas: {e}")
        return []

def get_brand_by_id(brand_id):
    """
    Obtiene una marca específica por su ID.
    """
    try:
        response = requests.get(f"{API_URL}/{brand_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la marca {brand_id}: {e}")
        return None

def create_brand(brand_data):
    """
    Crea una nueva marca usando una solicitud POST.
    """
    try:
        response = requests.post(API_URL, json=brand_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al crear la marca: {e}")
        return None