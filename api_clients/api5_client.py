import requests
import os

# La URL de la API se obtendrá de una variable de entorno para mayor flexibilidad.
# Si no se define, se usará una URL local por defecto.
# Asegúrate de configurar esta variable en tu entorno de producción.
API_URL = os.environ.get("PURCHASE_HISTORY_API_URL", "https://historial-productos.onrender.com/compras")

def get_all_purchases():
    """
    Obtiene todo el historial de compras de la API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Historial de Compras: {e}")
        return []

def add_purchase(purchase_data):
    """
    Registra una nueva compra usando una solicitud POST.
    """
    try:
        response = requests.post(API_URL, json=purchase_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al registrar la compra: {e}")
        return None

def delete_purchase(purchase_id):
    """
    Elimina un registro de compra por su ID usando una solicitud DELETE.
    """
    try:
        response = requests.delete(f"{API_URL}/{purchase_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar la compra {purchase_id}: {e}")
        return None