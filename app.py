# -*- coding: utf-8 -*-
"""
Aplicación Flask principal - SafeZone
Sistema de reportes de anomalías viales
"""
from flask import Flask
from flask_mail import Mail

from admin import admin_bp
from auth import auth_bp, init_auth
from config import MAIL_CONFIG, SECRET_KEY, UPLOAD_FOLDER
from reports import reports_bp
from visualizations import visualizations_bp

mail = Mail()


def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Configurar Flask-Mail
    for key, value in MAIL_CONFIG.items():
        app.config[key] = value

    mail.init_app(app)

    bcrypt = init_auth(app, mail)

    app.register_blueprint(auth_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(visualizations_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5000)
