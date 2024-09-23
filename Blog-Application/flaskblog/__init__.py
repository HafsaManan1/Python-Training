from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_ckeditor import CKEditor

# Initialize extensions
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()

login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app(config_class = Config):
    # Create app instance
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    from flaskblog.errors.errors import errors
    from flaskblog.author.author import author
    from flaskblog.main.main import main
    from flaskblog.blog.blog import blog

    app.register_blueprint(errors)
    app.register_blueprint(author)
    app.register_blueprint(main)
    app.register_blueprint(blog)
    return app


