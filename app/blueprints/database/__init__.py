from .blueprints import db_blueprint


def init_app(app):
    app.register_blueprint(db_blueprint, url_prefix='/database')
