from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from gateway import api_bp # Importar el Blueprint
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app) # Habilitar CORS en la app principal

# Registrar el Blueprint del API Gateway con el prefijo /api
app.register_blueprint(api_bp, url_prefix='/api')

# La URL base para las llamadas internas ahora es relativa
GATEWAY_URL = "/api"

# --- Rutas Principales ---
@app.route('/')
def dashboard():
    base_url = request.url_root.rstrip('/') # Obtener la URL base de la app (ej. http://localhost:5000)
    try:
        products = requests.get(f"{base_url}{GATEWAY_URL}/products").json()
        categories = requests.get(f"{base_url}{GATEWAY_URL}/categories").json()
        brands = requests.get(f"{base_url}{GATEWAY_URL}/brands").json()
        units = requests.get(f"{base_url}{GATEWAY_URL}/units").json()
    except requests.exceptions.RequestException as e:
        flash(f"Error al conectar con el API Gateway: {e}", "error")
        products, categories, brands, units = [], [], [], []

    return render_template('index.html', products=products, categories=categories, brands=brands, units=units)

# --- CRUD de Productos ---
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    base_url = request.url_root.rstrip('/')
    if request.method == 'POST':
        units = requests.get(f"{base_url}{GATEWAY_URL}/units").json()
        unit_map = {unit['id']: unit['nombre'] for unit in units}
        selected_unit_id = int(request.form['unit'])
        selected_unit_name = unit_map.get(selected_unit_id)

        if selected_unit_name in ['Unidad', 'Caja']:
            validation_data = {"unidad": selected_unit_name, "cantidad": request.form.get('quantity')}
            validation_result = requests.post(f"{base_url}{GATEWAY_URL}/units/validate", data=validation_data).json()
            if validation_result and validation_result.get('error'):
                flash(f"Error de validación: {validation_result.get('error')}", 'error')
                categories = requests.get(f"{base_url}{GATEWAY_URL}/categories").json()
                brands = requests.get(f"{base_url}{GATEWAY_URL}/brands").json()
                return render_template('product_form.html', product=request.form, categories=categories, brands=brands, units=units, title="Añadir Nuevo Producto")

        product_data = {
            "nom_pro": request.form['name'], "pre_pro": float(request.form['price']),
            "stk_pro": float(request.form['stock']), "id_cat": int(request.form['category']),
            "id_marca": int(request.form['brand']), "id_uni": selected_unit_id,
            "estado": request.form['state']
        }
        requests.post(f"{base_url}{GATEWAY_URL}/products", json=product_data)
        return redirect(url_for('dashboard'))

    categories = requests.get(f"{base_url}{GATEWAY_URL}/categories").json()
    brands = requests.get(f"{base_url}{GATEWAY_URL}/brands").json()
    units = requests.get(f"{base_url}{GATEWAY_URL}/units").json()
    return render_template('product_form.html', product={}, categories=categories, brands=brands, units=units, title="Añadir Nuevo Producto")

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    base_url = request.url_root.rstrip('/')
    if request.method == 'POST':
        units = requests.get(f"{base_url}{GATEWAY_URL}/units").json()
        unit_map = {unit['id']: unit['nombre'] for unit in units}
        selected_unit_id = int(request.form['unit'])
        selected_unit_name = unit_map.get(selected_unit_id)

        if selected_unit_name in ['Unidad', 'Caja']:
            validation_data = {"unidad": selected_unit_name, "cantidad": request.form.get('quantity')}
            validation_result = requests.post(f"{base_url}{GATEWAY_URL}/units/validate", data=validation_data).json()
            if validation_result and validation_result.get('error'):
                flash(f"Error de validación: {validation_result.get('error')}", 'error')
                categories = requests.get(f"{base_url}{GATEWAY_URL}/categories").json()
                brands = requests.get(f"{base_url}{GATEWAY_URL}/brands").json()
                product_data = request.form.to_dict()
                product_data['id_pro'] = product_id
                return render_template('product_form.html', product=product_data, categories=categories, brands=brands, units=units, title="Editar Producto")

        product_data = {
            "id_pro": product_id, "nom_pro": request.form['name'],
            "pre_pro": float(request.form['price']), "stk_pro": float(request.form['stock']),
            "id_cat": int(request.form['category']), "id_marca": int(request.form['brand']),
            "id_uni": selected_unit_id, "estado": request.form['state']
        }
        requests.put(f"{base_url}{GATEWAY_URL}/products", json=product_data)
        return redirect(url_for('dashboard'))

    product_to_edit = requests.get(f"{base_url}{GATEWAY_URL}/products/{product_id}").json()
    categories = requests.get(f"{base_url}{GATEWAY_URL}/categories").json()
    brands = requests.get(f"{base_url}{GATEWAY_URL}/brands").json()
    units = requests.get(f"{base_url}{GATEWAY_URL}/units").json()
    return render_template('product_form.html', product=product_to_edit, categories=categories, brands=brands, units=units, title="Editar Producto")

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    base_url = request.url_root.rstrip('/')
    requests.delete(f"{base_url}{GATEWAY_URL}/products/{product_id}")
    return redirect(url_for('dashboard'))

# --- CRUD de Categorías ---
@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
    base_url = request.url_root.rstrip('/')
    if request.method == 'POST':
        category_data = {"nom_cat": request.form['name'], "descripcion": request.form['description']}
        requests.post(f"{base_url}{GATEWAY_URL}/categories", json=category_data)
        return redirect(url_for('dashboard'))
    return render_template('category_form.html', category={}, title="Añadir Nueva Categoría")

@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    base_url = request.url_root.rstrip('/')
    if request.method == 'POST':
        category_data = {"nom_cat": request.form['name'], "descripcion": request.form['description']}
        requests.put(f"{base_url}{GATEWAY_URL}/categories/{category_id}", json=category_data)
        return redirect(url_for('dashboard'))
    category_to_edit = requests.get(f"{base_url}{GATEWAY_URL}/categories/{category_id}").json()
    return render_template('category_form.html', category=category_to_edit, title="Editar Categoría")

@app.route('/category/delete/<int:category_id>', methods=['POST'])
def delete_category_route(category_id):
    base_url = request.url_root.rstrip('/')
    requests.delete(f"{base_url}{GATEWAY_URL}/categories/{category_id}")
    return redirect(url_for('dashboard'))

# --- CRUD de Marcas ---
@app.route('/brand/add', methods=['GET', 'POST'])
def add_brand():
    base_url = request.url_root.rstrip('/')
    if request.method == 'POST':
        brand_data = {"nombre": request.form['name']}
        requests.post(f"{base_url}{GATEWAY_URL}/brands", json=brand_data)
        return redirect(url_for('dashboard'))
    return render_template('brand_form.html', brand={}, title="Añadir Nueva Marca")

# --- Lógica de Unidades ---
@app.route('/unit/validate', methods=['POST'])
def validate_unit():
    base_url = request.url_root.rstrip('/')
    validation_data = {"unidad": request.form['unit_name'], "cantidad": request.form['quantity']}
    result = requests.post(f"{base_url}{GATEWAY_URL}/units/validate", data=validation_data).json()
    if result:
        message = result.get('ok') or result.get('error') or 'No se recibió un mensaje claro.'
        flash(message, 'info')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)