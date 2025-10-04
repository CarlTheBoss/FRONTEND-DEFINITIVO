//API PRODUCTOS
https://8080-firebase-product-service-java-1759371536787.cluster-fsmcisrvfbb5cr5mvra3hr3qyg.cloudworkstations.dev/api/v1/products
API ROUTES

GET /api/v1/products

RETURNS {

"items": {

    "id_pro": bigint PK,

    "nom_pro": varchar(100) NOT NULL UNIQUE,

    "pre_pro": double NOT NULL,

    "id_uni": bigint,

    "id_marca": bigint,

    "id_cat": bigint,

    "stk_pro": double NOT NULL,

    "estado": char(1) DEFAULT 'Y'

}[],

"numberOfElements": bigint

}

GET /api/v1/products/{id}

WHERE id = bigint NOT NULL

RETURNS {

"id_pro": bigint,

"nom_pro": varchar(100),

"pre_pro": double,

"id_uni": bigint,

"id_marca": bigint,

"id_cat": bigint,

"stk_pro": double,

"estado": char(1)

}

POST /api/v1/products

BODY:

- Content-Type: "application/json"

- Structure: {

  "nom_pro": varchar(100) NOT NULL,

  "pre_pro": double NOT NULL,

  "id_uni": bigint,

  "id_marca": bigint,

  "id_cat": bigint,

  "stk_pro": double NOT NULL,

  "estado": char(1)
  }

PUT /api/v1/products

BODY:

- Content-Type: "application/json"

- Structure: {

  "id_pro": bigint NOT NULL,

  "nom_pro": varchar(100),

  "pre_pro": double,

  "id_uni": bigint,

  "id_marca": bigint,

  "id_cat": bigint,

  "stk_pro": double,

  "estado": char(1)

}

DELETE /api/v1/products/{id}

WHERE id = bigint

RETURNS {

"register_deleted_id": id,

"result": "DELETED"

}

//API CATEGORIAS
https://api-categoria-a8hp.onrender.com/categorias

# Listar todas las categorías

GET /categorias

# Obtener categoría por ID

GET /categorias/<id>

# Crear una nueva categoría

POST /categorias
Body JSON:
{
"nom_cat": "Parlantes",
"descripcion": "Dispositivos de sonido"
}

# Actualizar una categoría

PUT /categorias/<id>
Body JSON:
{
"nom_cat": "Mouse Gamer",
"descripcion": "Ratón con luces RGB"
}

# Eliminar una categoría

DELETE /categorias/<id>

//API MARCAS
GET
https://apimarcas.onrender.com/api/marcas
https://apimarcas.onrender.com/api/marcas/{id}

POST
{
"nombre": "Carambas"
}

//API UNIDADES

1. Listar Unidades

Método: GET
Endpoint: /

Ejemplo de Request
GET https://php-82eb1.wasmer.app/

Ejemplo de Respuesta
{
"unidades": [
{ "id": 1, "nombre": "Unidad" },
{ "id": 2, "nombre": "Caja" },
{ "id": 5, "nombre": "nombre" },
{ "id": 9, "nombre": "hola" },
{ "id": 12, "nombre": "unidad" },
{ "id": 13, "nombre": "unidad" },
{ "id": 14, "nombre": "hyundai" }
]
}
Ejemplo de Request en Postman

URL: https://php-82eb1.wasmer.app/

Método: POST

Body → x-www-form-urlencoded

KEY VALUE
unidad Unidad
cantidad 5
Ejemplo de Respuesta Exitosa
{
"success": true,
"unidad": "Unidad",
"cantidad": 5,
"message": "Cantidad válida"
}

Ejemplo de Respuesta con Error (regla de negocio)

Si se envía "Unidad" con cantidad mayor a 12:

{
"success": false,
"message": "Si la cantidad es mayor a 12, debes usar Caja"
}
