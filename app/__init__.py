from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder="app/templates",
        static_folder="static"
    )
    app.secret_key = "supersecretkey"

    # Register blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app
