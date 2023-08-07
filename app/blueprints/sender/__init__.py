from .blueprints import sender_blueprint


def init_app(app):
    app.register_blueprint(sender_blueprint, url_prefix='/sender')
