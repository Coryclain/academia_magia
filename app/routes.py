from flask import Blueprint, request, jsonify
from .models import Application
from .controllers import create_application, update_application, delete_application, update_application_status, get_applications_info, get_assignments_info

bp = Blueprint('routes', __name__)

@bp.route('/solicitud', methods=['POST'])
def create_request():
    """
    Crear una nueva solicitud de ingreso.

    Esta función permite enviar una solicitud de ingreso para un estudiante 
    a la academia de magia en el Reino del Trébol.

    ---
    tags:
      - Solicitudes
    parameters:
      - in: body
        name: solicitud
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              maxLength: 20
              minLength: 1
              pattern: '^[a-zA-ZñÑ]+$'
              example: "Alice"
            apellido:
              type: string
              maxLength: 20
              minLength: 1
              pattern: '^[a-zA-ZñÑ]+$'
              example: "Johnson"
            identificacion:
              type: string
              maxLength: 10
              minLength: 1
              pattern: '^[0-9a-zA-Z]+$'
              example: "ID123456"
            edad:
              type: integer
              minimum: 0
              maximum: 99
              example: 25
            afinidad_magica:
              type: string
              enum: ["Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra"]
              example: "Luz"
          required:
            - nombre
            - apellido
            - identificacion
            - edad
            - afinidad_magica
        examples:
          ejemplo1:
            value:
              nombre: "Noelle"
              apellido: "Silva"
              identificacion: "ID123456"
              edad: 25
              afinidad_magica: "Luz"
    responses:
      201:
        description: Solicitud creada correctamente.
      400:
        description: Error en la validación de datos o solicitud inválida.
      409:
        description: Ya existe una solicitud con esta identificación.
    """
    data = request.json
    return create_application(data)

@bp.route('/solicitud/<int:id>', methods=['PUT'])
def update_request(id):
    """
    Actualizar una solicitud existente.

    Esta función permite actualizar una solicitud de ingreso existente.

    ---
    tags:
      - Solicitudes
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: ID de la solicitud a actualizar.
      - in: body
        name: solicitud
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              maxLength: 20
              minLength: 1
              pattern: '^[a-zA-ZñÑ]+$'
              example: "Alice"
            apellido:
              type: string
              maxLength: 20
              minLength: 1
              pattern: '^[a-zA-ZñÑ]+$'
              example: "Johnson"
            identificacion:
              type: string
              maxLength: 10
              minLength: 1
              pattern: '^[0-9a-zA-Z]+$'
              example: "ID123456"
            edad:
              type: integer
              minimum: 0
              maximum: 99
              example: 25
            afinidad_magica:
              type: string
              enum: ["Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra"]
              example: "Luz"
          required:
            - nombre
            - apellido
            - identificacion
            - edad
            - afinidad_magica
        examples:
          ejemplo1:
            value:
              nombre: "Noelle"
              apellido: "Silva"
              identificacion: "ID123456"
              edad: 25
              afinidad_magica: "Luz"
    responses:
      200:
        description: Solicitud actualizada correctamente.
      400:
        description: Error en la validación de datos.
      404:
        description: Solicitud no encontrada.
      409:
        description: Ya existe una solicitud con esta identificación.
    """
    application = Application.query.get(id)
    if not application:
        return jsonify({'error': 'Solicitud no encontrada'}), 404
    data = request.json
    return update_application(data, application)

@bp.route('/solicitud/<int:id>', methods=['DELETE'])
def delete_request(id):
    """
    Eliminar una solicitud existente.

    Esta función permite eliminar una solicitud de ingreso existente

    ---
    tags:
      - Solicitudes
    parameters:
    - in: path
      name: id
      required: true
      schema:
        type: integer
      description: ID de la solicitud a eliminar.
    responses:
      200:
        description: Solicitud eliminada correctamente.
      404:
        description: Solicitud no encontrada.
    """
    application = Application.query.get(id)
    if not application:
        return jsonify({'error': 'Solicitud no encontrada'}), 404
    return delete_application(application)

@bp.route('/solicitud/<int:id>/estatus', methods=['PATCH'])
def update_request_status(id):
    """
    Actualizar el estatus de una solicitud existente.

    Esta función permite actualizar el estatus de una solicitud de ingreso existente.

    ---
    tags:
      - Solicitudes
    parameters:
    - in: path
      name: id
      required: true
      schema:
        type: integer
      description: ID de la solicitud a actualizar.
    - in: body
      name: estatus
      required: true
      schema:
        type: object
        properties:
          estatus:
            type: string
            enum: ["aprobada", "rechazada"]
        required:
          - estatus
    responses:
      200:
        description: Estatus de solicitud actualizado correctamente.
      400:
        description: Error en la validación de datos.
      404:
        description: Solicitud no encontrada.
      409:
        description: No se puede modificar el estatus de esta solicitud.
    """
    application = Application.query.get(id)
    if not application:
        return jsonify({'error': 'Solicitud no encontrada'}), 404
    data = request.json
    return update_application_status(data, application)

@bp.route('/solicitudes', methods=['GET'])
def get_requests():
    """
    Obtener todas las solicitudes existentes.

    Esta función permite obtener todas las solicitudes de ingreso existentes.

    ---
    tags:
      - Solicitudes
    responses:
      200:
        description: Listado de solicitudes obtenidas correctamente.
    """
    return get_applications_info()

@bp.route('/asignaciones', methods=['GET'])
def get_assignments():
    """
    Obtener todas las asignaciones existentes.

    Esta función permite obtener todas las asignaciones de Grimorios existentes.

    ---
    tags:
      - Asignaciones
    responses:
      200:
        description: Listado de asignaciones obtenidas correctamente.
    """
    return get_assignments_info()
