# Academia de Magia - Reino Trébol

En el Reino del Trébol, el Rey Mago necesita un sistema para la academia de magia
que administre el registro de solicitud de estudiantes y la asignación aleatoria de
sus Grimorios. Los Grimorios se clasifican según el tipo de trébol en la portada, y
los estudiantes según sus afinidades mágicas específicas.

### Requisitos

- Python 3.12.2 o superior

### Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/Coryclain/academia_magia.git
cd academia_magia
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar el proyecto de forma local

```bash
python run.py
```
El endpoint generado sera 127.0.0.1:5000

<img src="https://github.com/Coryclain/academia_magia/blob/main/images/pyrun.png?raw=true">

La base de datos se creara al ejecutarse por primera vez, después se quedara almacenada en instance/database.db

## Pruebas unitarias

Para ejecutar las pruebas unitarias desde la raíz del proyecto:

```bash
python -m unittest discover -s tests
```

<img src="https://github.com/Coryclain/academia_magia/blob/main/images/unittest.png?raw=true">

### API Swagger

Accede a la documentación de la API Swagger:

Local: http://127.0.0.1:5000/apidocs/

Remoto: [https://academia-magia.onrender.com/apidocs](https://academia-magia.onrender.com/apidocs)

<img src="https://github.com/Coryclain/academia_magia/blob/main/images/api_swagger.png?raw=true">

### URL API

La aplicación está desplegada en Render:

URL pública: [https://academia-magia.onrender.com](https://academia-magia.onrender.com)

<img src="https://github.com/Coryclain/academia_magia/blob/main/images/render.png?raw=true">

Ejemplo de consumo:

<img src="https://github.com/Coryclain/academia_magia/blob/main/images/uso_url.png?raw=true">

### Créditos

Autor: Abigail Reyes
