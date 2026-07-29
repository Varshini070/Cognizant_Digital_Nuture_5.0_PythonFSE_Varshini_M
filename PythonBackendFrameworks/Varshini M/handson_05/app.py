from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from courses.routes import courses_bp

    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(error):
        return {'status': 'error', 'message': 'Resource not found'}, 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return {'status': 'error', 'message': 'Internal server error'}, 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
