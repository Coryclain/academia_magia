import unittest
import json
from app import create_app, db
from app.models import Application 
from app.utils import assign_grimorio

class TestSolicitudEndpoint(unittest.TestCase):
    
    def setUp(self):
        # Configura la aplicación Flask en modo de prueba
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()  # Crea las tablas en la base de datos de prueba

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_solicitud(self):
        solicitud_data = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 25,
            "afinidad_magica": "Luz"
        }
        
        # Realiza una solicitud POST al endpoint /solicitud
        response = self.client.post('/solicitud', json=solicitud_data)
        
        # Verifica el código de respuesta y el contenido
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], 'Solicitud creada correctamente')

        # Verifica que la solicitud esté en la base de datos
        solicitud = db.session.query(Application).filter_by(identity="ID123456").first()
        self.assertIsNotNone(solicitud)
        self.assertEqual(solicitud.name, "Noelle")
        self.assertEqual(solicitud.lastname, "Silva")
        self.assertEqual(solicitud.age, 25)
        self.assertEqual(solicitud.magical_affinity, "Luz")

    def test_create_duplicate_solicitud(self):
        # Crea una solicitud inicial
        solicitud_data = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 25,
            "afinidad_magica": "Luz"
        }
        self.client.post('/solicitud', json=solicitud_data)

        # Intenta crear otra solicitud con la misma identificación
        response = self.client.post('/solicitud', json=solicitud_data)
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], 'Ya existe una solicitud con esta identificación')

    def test_update_solicitud(self):
        # Crea una solicitud inicial
        solicitud_data = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 25,
            "afinidad_magica": "Luz"
        }
        self.client.post('/solicitud', json=solicitud_data)

        # Obtiene el ID de la solicitud creada
        solicitud = db.session.query(Application).filter_by(identity="ID123456").first()

        # Actualiza la solicitud
        updated_data = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 30,
            "afinidad_magica": "Agua"
        }
        response = self.client.put(f'/solicitud/{solicitud.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], 'Solicitud actualizada correctamente')

        # Verifica que los cambios se hayan aplicado correctamente
        updated_solicitud = db.session.query(Application).filter_by(id=solicitud.id).first()
        self.assertEqual(updated_solicitud.magical_affinity, "Agua")
        self.assertEqual(updated_solicitud.age, 30)

    def test_delete_solicitud(self):
        # Crea una solicitud inicial
        solicitud_data = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 25,
            "afinidad_magica": "Luz"
        }
        self.client.post('/solicitud', json=solicitud_data)

        # Obtiene el ID de la solicitud creada
        solicitud = db.session.query(Application).filter_by(identity="ID123456").first()

        # Elimina la solicitud
        response = self.client.delete(f'/solicitud/{solicitud.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], 'Solicitud eliminada correctamente')

        # Verifica que la solicitud ya no exista en la base de datos
        deleted_solicitud = db.session.query(Application).filter_by(id=solicitud.id).first()
        self.assertIsNone(deleted_solicitud)

    def test_update_solicitud_status(self):
        # Crea una solicitud inicial
        solicitud_data = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 25,
            "afinidad_magica": "Luz"
        }
        self.client.post('/solicitud', json=solicitud_data)

        # Obtiene el ID de la solicitud creada
        solicitud = db.session.query(Application).filter_by(identity="ID123456").first()

        # Actualiza el estatus de la solicitud
        updated_status = {
            "estatus": "aprobada"
        }
        response = self.client.patch(f'/solicitud/{solicitud.id}/estatus', json=updated_status)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], 'Solicitud Aprobada')

    def test_get_all_solicitudes(self):
        # Crea algunas solicitudes de ejemplo
        solicitud_data1 = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 25,
            "afinidad_magica": "Luz"
        }
        solicitud_data2 = {
            "nombre": "Astolfo",
            "apellido": "Klaus",
            "identificacion": "ID789012",
            "edad": 30,
            "afinidad_magica": "Oscuridad"
        }
        self.client.post('/solicitud', json=solicitud_data1)
        self.client.post('/solicitud', json=solicitud_data2)

        # Obtiene todas las solicitudes
        response = self.client.get('/solicitudes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))

        # Verifica que las solicitudes retornadas coincidan con las creadas
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Noelle")
        self.assertEqual(data[1]['magical_affinity'], "Oscuridad")

    def test_get_all_asignaciones(self):
        # Crea una solicitud inicial
        solicitud_data = {
            "nombre": "Noelle",
            "apellido": "Silva",
            "identificacion": "ID123456",
            "edad": 25,
            "afinidad_magica": "Luz"
        }
        self.client.post('/solicitud', json=solicitud_data)

        # Obtiene el ID de la solicitud creada
        solicitud = db.session.query(Application).filter_by(identity="ID123456").first()

        # Asigna un Grimorio a la solicitud
        assigned_type = assign_grimorio(solicitud)

        # Obtiene todas las asignaciones de Grimorios
        response = self.client.get('/asignaciones')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))

        # Verifica que la asignación de Grimorio coincida con la solicitud creada
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['Nombre'], "Noelle")
        self.assertEqual(data[0]['Grimorio'], assigned_type)

if __name__ == '__main__':
    unittest.main()

