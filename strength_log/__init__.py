import logging
from logging.handlers import SMTPHandler
import os

from strength_log.config import Config, config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect
from loguru import logger


# configuration

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap()
moment = Moment()
toolbar = DebugToolbarExtension()
login.login_view = "users.login"
login.login_message_category = "info"


def initialize_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)


def register_blueprints(app):
    from strength_log.users.routes import users
    from strength_log.posts.routes import posts
    from strength_log.main.routes import main
    from strength_log.maxes.routes import maxes
    from strength_log.personal_records.routes import personal_records
    from strength_log.errors.routes import errors
    from strength_log.training_volume.routes import training_volume

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(maxes)
    app.register_blueprint(personal_records)
    app.register_blueprint(training_volume)
    app.register_blueprint(errors)


# app factory
def create_app(config_class=Config):
    app = Flask(__name__)
    config_env = os.getenv("FLASK_CONFIG", "default")
    app.config.from_object(config[config_env])
    logger.info("App init")

    initialize_extensions(app)

    register_blueprints(app)

    return app


app = create_app()


if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"],
            subject="Strength Log Failure",
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
