from flask import Flask, render_template, request, redirect, url_for, flash
from gateway import api_bp # Importar y registrar el Blueprint sigue siendo una buena práctica
from api_clients import api1_client, api2_client, api3_client, api4_client
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

# Registrar el Blueprint del API Gateway para que las rutas /api sigan existiendo
app.register_blueprint(api_bp, url_prefix='/api')

# --- Rutas Principales ---
@app.route('/')
def dashboard():
    # Volvemos a llamar a los clientes directamente para evitar el deadlock
    try:
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
    except Exception as e:
        flash(f"Error al obtener los datos: {e}", "error")
        enriched_products, categories, brands, units = [], [], [], []

    return render_template('index.html', products=enriched_products, categories=categories, brands=brands, units=units)

# --- CRUD de Productos ---
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        units = api4_client.get_all_units()
        unit_map = {unit['id']: unit['nombre'] for unit in units}
        selected_unit_id = int(request.form['unit'])
        selected_unit_name = unit_map.get(selected_unit_id)

        if selected_unit_name in ['Unidad', 'Caja']:
            validation_data = {"unidad": selected_unit_name, "cantidad": request.form.get('quantity')}
            validation_result = api4_client.validate_quantity(validation_data)
            if validation_result and validation_result.get('error'):
                flash(f"Error de validación: {validation_result.get('error')}", 'error')
                categories = api2_client.get_all_categories()
                brands = api3_client.get_all_brands()
                return render_template('product_form.html', product=request.form, categories=categories, brands=brands, units=units, title="Añadir Nuevo Producto")

        product_data = {
            "nom_pro": request.form['name'], "pre_pro": float(request.form['price']),
            "stk_pro": float(request.form['stock']), "id_cat": int(request.form['category']),
            "id_marca": int(request.form['brand']), "id_uni": selected_unit_id,
            "estado": request.form['state']
        }
        api1_client.create_product(product_data)
        return redirect(url_for('dashboard'))

    categories = api2_client.get_all_categories()
    brands = api3_client.get_all_brands()
    units = api4_client.get_all_units()
    return render_template('product_form.html', product={}, categories=categories, brands=brands, units=units, title="Añadir Nuevo Producto")

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        units = api4_client.get_all_units()
        unit_map = {unit['id']: unit['nombre'] for unit in units}
        selected_unit_id = int(request.form['unit'])
        selected_unit_name = unit_map.get(selected_unit_id)

        if selected_unit_name in ['Unidad', 'Caja']:
            validation_data = {"unidad": selected_unit_name, "cantidad": request.form.get('quantity')}
            validation_result = api4_client.validate_quantity(validation_data)
            if validation_result and validation_result.get('error'):
                flash(f"Error de validación: {validation_result.get('error')}", 'error')
                categories = api2_client.get_all_categories()
                brands = api3_client.get_all_brands()
                product_data = request.form.to_dict()
                product_data['id_pro'] = product_id
                return render_template('product_form.html', product=product_data, categories=categories, brands=brands, units=units, title="Editar Producto")

        product_data = {
            "id_pro": product_id, "nom_pro": request.form['name'],
            "pre_pro": float(request.form['price']), "stk_pro": float(request.form['stock']),
            "id_cat": int(request.form['category']), "id_marca": int(request.form['brand']),
            "id_uni": selected_unit_id, "estado": request.form['state']
        }
        api1_client.update_product(product_data)
        return redirect(url_for('dashboard'))

    product_to_edit = api1_client.get_product_by_id(product_id)
    categories = api2_client.get_all_categories()
    brands = api3_client.get_all_brands()
    units = api4_client.get_all_units()
    return render_template('product_form.html', product=product_to_edit, categories=categories, brands=brands, units=units, title="Editar Producto")

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    api1_client.delete_product(product_id)
    return redirect(url_for('dashboard'))

# --- CRUD de Categorías ---
@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_data = {"nom_cat": request.form['name'], "descripcion": request.form['description']}
        api2_client.create_category(category_data)
        return redirect(url_for('dashboard'))
    return render_template('category_form.html', category={}, title="Añadir Nueva Categoría")

@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'POST':
        category_data = {"nom_cat": request.form['name'], "descripcion": request.form['description']}
        api2_client.update_category(category_id, category_data)
        return redirect(url_for('dashboard'))
    category_to_edit = api2_client.get_category_by_id(category_id)
    return render_template('category_form.html', category=category_to_edit, title="Editar Categoría")

@app.route('/category/delete/<int:category_id>', methods=['POST'])
def delete_category_route(category_id):
    api2_client.delete_category(category_id)
    return redirect(url_for('dashboard'))

# --- CRUD de Marcas ---
@app.route('/brand/add', methods=['GET', 'POST'])
def add_brand():
    if request.method == 'POST':
        brand_data = {"nombre": request.form['name']}
        api3_client.create_brand(brand_data)
        return redirect(url_for('dashboard'))
    return render_template('brand_form.html', brand={}, title="Añadir Nueva Marca")

# --- Lógica de Unidades ---
@app.route('/unit/validate', methods=['POST'])
def validate_unit():
    validation_data = {"unidad": request.form['unit_name'], "cantidad": request.form['quantity']}
    result = api4_client.validate_quantity(validation_data)
    if result:
        message = result.get('ok') or result.get('error') or 'No se recibió un mensaje claro.'
        flash(message, 'info')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
