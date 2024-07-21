from flask import Flask, jsonify
from .models import db
from .routes import bp as routes_bp
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)

    # Configuración de Swagger
    @app.route("/apidocs/swagger.json")
    def create_swagger_spec():
        swag = swagger(app)
        swag['info'] = {
            'title': 'API de la Academia de Magia del Reino del Trébol',
            'version': '1.0',
            'description': "En el Reino del Trébol, el Rey Mago necesita un sistema para la academia de magia que administre el registro de solicitud de estudiantes y la asignación aleatoria de sus Grimorios. Los Grimorios se clasifican según el tipo de trébol en la portada, y los estudiantes según sus afinidades mágicas específicas."
        }
        return jsonify(swag)

    SWAGGER_URL = '/apidocs'
    API_URL = '/apidocs/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Academia de Magia - Swagger"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app

def create_app_test():
    app = Flask(__name__)

    app.config.from_mapping({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)

    # Configuración de Swagger
    @app.route("/apidocs/swagger.json")
    def create_swagger_spec():
        swag = swagger(app)
        swag['info'] = {
            'title': 'API de la Academia de Magia del Reino del Trébol',
            'version': '1.0',
            'description': "En el Reino del Trébol, el Rey Mago necesita un sistema para la academia de magia que administre el registro de solicitud de estudiantes y la asignación aleatoria de sus Grimorios. Los Grimorios se clasifican según el tipo de trébol en la portada, y los estudiantes según sus afinidades mágicas específicas."
        }
        return jsonify(swag)

    SWAGGER_URL = '/apidocs'
    API_URL = '/apidocs/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Academia de Magia - Swagger"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
