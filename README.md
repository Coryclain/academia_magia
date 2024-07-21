# Academia de Magia - Reino Trébol

En el Reino del Trébol, el Rey Mago necesita un sistema para la academia de magia
que administre el registro de solicitud de estudiantes y la asignación aleatoria de
sus Grimorios. Los Grimorios se clasifican según el tipo de trébol en la portada, y
los estudiantes según sus afinidades mágicas específicas.

### Requisitos

- Python 3.12.2 o superior

### Instalación

Comienza por clonar el repositorio
```bash
git clone https://github.com/Coryclain/prueba_tecnica.git
```

Para instalar las dependencias, utiliza pip con el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar el proyecto de forma local:

```bash
python run.py
```

La base de datos se creara al ejecutarse por primera vez, después se quedara almacenada en instance/database.db

## Pruebas unitarias

Para correr las pruebas desde la raíz del proyecto

```bash
python -m unittest discover -s tests
```

### API Swagger

local: http://127.0.0.1:5000/apidocs/

remoto: http://url_pagina/apidocs/

### URL API

https://prueba-tecnica-9odf.onrender.com

### Créditos

Autor: Abigail Reyes
