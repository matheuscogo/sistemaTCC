def init_app(app):
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sistemaTCC.db'
    app.config["SQLALCHEMY_BINDS"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['CORS_HEADERS'] = "Content-Type"
    app.config['CORS_RESOURCES'] = {r"/api/v1/*": {"origins": "http://localhost:3000/*"}}
    app.config["CORS_ALLOW_HEADERS"] = "*"
    app.config["CORS_METHODS"] = ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD']
    app.config['Access-Control-Allow-Origin'] = '*'
