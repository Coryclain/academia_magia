solicitud_schema = {
    "type": "object",
    "properties": {
        "nombre": {"type": "string", "pattern": "^[a-zA-zñÑ]*$", "maxLength": 20, "minLength": 1},
        "apellido": {"type": "string", "pattern": "^[a-zA-zñÑ]*$", "maxLength": 20, "minLength": 1},
        "identificacion": {"type": "string", "pattern": "^[0-9a-zA-z]*$", "maxLength": 10, "minLength": 1},
        "edad": {"type": "integer", "minimum": 0, "maximum": 99},
        "afinidad_magica": {"type": "string", "enum": ["Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra"]}
    },
    "required": ["nombre", "apellido", "identificacion", "edad", "afinidad_magica"]
}