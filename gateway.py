from flask import Blueprint, jsonify, request
from api_clients import api1_client, api2_client, api3_client, api4_client

# Crear un Blueprint llamado 'api'. Todas las rutas definidas aquí
# tendrán el prefijo que se configure al registrarlo (ej. /api)
api_bp = Blueprint('api', __name__)

# --- Endpoints de Productos ---
@api_bp.route('/products', methods=['GET'])
def get_products():
    products = api1_client.get_all_products()
    categories = api2_client.get_all_categories()
    brands = api3_client.get_all_brands()
    units = api4_client.get_all_units()
    category_map = {cat['id_cat']: cat['nom_cat'] for cat in categories}
    brand_map = {brand['id']: brand['nombre'] for brand in brands}
    unit_map = {unit['id']: unit['nombre'] for unit in units}
    enriched_products = []
    for product in products:
        product['nom_cat'] = category_map.get(product.get('categoryId'), 'N/A')
        product['nom_marca'] = brand_map.get(product.get('marcaId'), 'N/A')
        product['nom_uni'] = unit_map.get(product.get('unitId'), 'N/A')
        enriched_products.append(product)
    return jsonify(enriched_products)

@api_bp.route('/products', methods=['POST'])
def create_product():
    product_data = request.get_json()
    result = api1_client.create_product(product_data)
    return jsonify(result)

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = api1_client.get_product_by_id(product_id)
    return jsonify(product)

@api_bp.route('/products', methods=['PUT'])
def update_product():
    product_data = request.get_json()
    result = api1_client.update_product(product_data)
    return jsonify(result)

@api_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = api1_client.delete_product(product_id)
    return jsonify(result)

# --- Endpoints de Categorías ---
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = api2_client.get_all_categories()
    return jsonify(categories)

@api_bp.route('/categories', methods=['POST'])
def create_category():
    category_data = request.get_json()
    result = api2_client.create_category(category_data)
    return jsonify(result)

@api_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = api2_client.get_category_by_id(category_id)
    return jsonify(category)

@api_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category_data = request.get_json()
    result = api2_client.update_category(category_id, category_data)
    return jsonify(result)

@api_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    result = api2_client.delete_category(category_id)
    return jsonify(result)

# --- Endpoints de Marcas ---
@api_bp.route('/brands', methods=['GET'])
def get_brands():
    brands = api3_client.get_all_brands()
    return jsonify(brands)

@api_bp.route('/brands', methods=['POST'])
def create_brand():
    brand_data = request.get_json()
    result = api3_client.create_brand(brand_data)
    return jsonify(result)

# --- Endpoints de Unidades ---
@api_bp.route('/units', methods=['GET'])
def get_units():
    units = api4_client.get_all_units()
    return jsonify(units)

@api_bp.route('/units/validate', methods=['POST'])
def validate_unit():
    validation_data = request.form.to_dict()
    result = api4_client.validate_quantity(validation_data)
    return jsonify(result)