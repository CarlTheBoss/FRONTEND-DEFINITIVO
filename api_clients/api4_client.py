import requests

API_URL = "https://php-82eb1.wasmer.app/"

def get_all_units():
    """
    Obtiene todas las unidades de la API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json().get("unidades", [])
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Unidades: {e}")
        return []

def validate_quantity(validation_data):
    """
    Valida una unidad y cantidad usando una solicitud POST con formato x-www-form-urlencoded.
    """
    try:
        # La API espera los datos en formato 'data', no 'json'.
        response = requests.post(API_URL, data=validation_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al validar la unidad: {e}")
        return None