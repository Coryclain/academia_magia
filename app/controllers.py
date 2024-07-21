from flask import jsonify
from .models import db, Application, Grimorio
from .utils import assign_grimorio
from jsonschema import validate, ValidationError


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

def create_application(data):
    """
        Función para crear una nueva solicitud de aprendizaje.
        :param data: Datos de la solicitud
        :return: Mensaje de éxito o error
    """
    try:
        validate(instance=data, schema=solicitud_schema)

        # Verificar si ya existe una solicitud con la misma identificación
        existing_solicitud = Application.query.filter_by(identity=data['identificacion']).first()
        if existing_solicitud:
            return jsonify({'message': 'Ya existe una solicitud con esta identificación'}), 409

        nueva_solicitud = Application(name=data['nombre'], lastname=data['apellido'],
                                    identity=data['identificacion'], age=data['edad'],
                                    magical_affinity=data['afinidad_magica'])
        db.session.add(nueva_solicitud)
        db.session.commit()
        return jsonify({'message': 'Solicitud creada correctamente'}), 201

    except ValidationError as e:
        return jsonify({'message': 'Error en la validación de datos', 'details': e.message}), 400
    except Exception as error:
        return jsonify({'message': 'Internal server error'}), 500

def update_application(data, application):
    """
        Función para actualizar una solicitud existente.
        :param data: Datos de la solicitud
        :param application: Solicitud a actualizar
        :return: Mensaje de éxito o error
    """
    try:
        validate(instance=data, schema=solicitud_schema)

        # Validar que la solicitud siga pendiente
        if application.status != 'Pending':
            return jsonify({'message': 'No se puede modificar una solicitud aprobada'}), 400

        # Verificar si ya existe una solicitud con la nueva identificación
        if 'identificacion' in data and data['identificacion'] != application.identity:
            existing_solicitud = Application.query.filter_by(identity=data['identificacion']).first()
            if existing_solicitud:
                return jsonify({'message': 'Ya existe una solicitud con esta identificación'}), 409

        application.name = data.get('nombre', application.name)
        application.lastname = data.get('apellido', application.lastname)
        application.age = data.get('edad', application.age)
        application.magical_affinity = data.get('afinidad_magica', application.magical_affinity)
        db.session.commit()
        return jsonify({'message': 'Solicitud actualizada correctamente'})
    except ValidationError as e:
        return jsonify({'message': 'Error en la validación de datos', 'details': e.message}), 400
    except Exception as error:
        print(error)
        return jsonify({'message': 'Internal server error'}), 500

def delete_application(application):
    """
        Función para eliminar una solicitud existente.
        :param application: Solicitud a eliminar
        :return: Mensaje de éxito o error
    """
    try:
        grimorio = Grimorio.query.filter_by(assignment=application.id).first()
        if grimorio:
            db.session.delete(grimorio)

        db.session.delete(application)
        db.session.commit()
        return jsonify({'message': 'Solicitud eliminada correctamente'})
    except Exception as error:
        print(error)
        return jsonify({'message': 'Internal server error'}), 500

def update_application_status(data, application):
    """
        Función para actualizar el estatus de una solicitud existente.
        :param data: Datos de la solicitud
        :param application: Solicitud a actualizar
        :return: Mensaje de éxito o error
    """
    try:
        if 'estatus' not in data or data['estatus'] not in ['aprobada', 'rechazada']:
            return jsonify({'message': 'El estatus indicado es inválido'}), 400

        # Validar que la solicitud siga pendiente
        if application.status == 'rechazada':
            return jsonify({'message': 'No se puede modificar el estatus de esta solicitud.'}), 400
        if application.status == 'aprobada':
            return jsonify({'message': 'Esta solicitud ya fue aprobada.'}), 400

        if data['estatus'] == 'aprobada':
            message = assign_grimorio(application)
            application.status = data['estatus']
            db.session.commit()
            return jsonify({'message': 'Solicitud Aprobada', 'Grimorio': message})

        application.status = data['estatus']
        db.session.commit()
        return jsonify({'message': 'Solicitud Rechazada'})
    except Exception as error:
        print(error)
        return jsonify({'message': 'Internal server error'}), 500

def get_applications_info():
    """
        Función para obtener todas las solicitudes existentes.
        :return: Lista de solicitudes
    """
    try:
        applications = Application.query.all()
        if applications is None:
            return jsonify([])

        return jsonify([application.serialize() for application in applications])
    except Exception as error:
        print(error)
        return jsonify({'message': 'Internal server error'}), 500

def get_assignments_info():
    """
        Función para obtener todas las asignaciones existentes.
        :return: Lista de asignaciones
    """
    try:
        asignaciones = Grimorio.query.all()
        if not asignaciones:
            return jsonify([])

        asignaciones_info = []
        for asignacion in asignaciones:
            solicitud = Application.query.filter_by(identity=asignacion.assignment).first()
            if solicitud:
                asignacion_info = dict()
                asignacion_info['Nombre'] = solicitud.name
                asignacion_info['Apellido'] = solicitud.lastname
                asignacion_info['Identificación'] = solicitud.identity
                asignacion_info['Edad'] = solicitud.age
                asignacion_info['Afinidad Mágica'] = solicitud.magical_affinity
                asignacion_info['Grimorio'] = asignacion.rarity
                asignaciones_info.append(asignacion_info)
            else:
                print(f"No se encontró la solicitud para la asignación {asignacion.id}")

        return jsonify(asignaciones_info)
    except Exception as error:
        print(error)
        return jsonify({'message': 'Internal server error'}), 500
