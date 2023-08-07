from .blueprints import account_blueprint


def init_app(app):
    app.register_blueprint(account_blueprint, url_prefix='/account')
