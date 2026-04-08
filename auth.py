# -*- coding: utf-8 -*-
import logging
import os
import uuid

import mysql.connector
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_bcrypt import Bcrypt
from flask_mail import Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS, SECRET_KEY, UPLOAD_FOLDER
from database import get_db, get_user_by_email_with_role

auth_bp = Blueprint('auth', __name__)
bcrypt = None
mail = None


def init_auth(app, mail_instance):
    global bcrypt, mail
    bcrypt = Bcrypt(app)
    mail = mail_instance
    return bcrypt


def _send_verification_email(correo, nombre, token):
    """Envía correo con botón que contiene el enlace de verificación."""
    link = url_for('auth.verificar_token', timed_token=token, _external=True)
    msg = Message(
        subject="Verifica tu cuenta - SafeZone",
        recipients=[correo],
        html=f"""
        <div style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;
                    background: #1f2937; border-radius: 16px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2);
                        padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px;">SafeZone</h1>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0;">Sistema de Gestión Vial</p>
            </div>
            <div style="padding: 40px 30px; color: white;">
                <h2 style="margin: 0 0 10px;">Hola, {nombre} 👋</h2>
                <p style="color: #9ca3af; line-height: 1.6;">
                    Gracias por registrarte en SafeZone. Solo falta un paso:
                    confirma tu correo electrónico haciendo clic en el botón.
                </p>
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{link}"
                       style="background: linear-gradient(135deg, #667eea, #764ba2);
                              color: white; text-decoration: none; padding: 16px 40px;
                              border-radius: 12px; font-size: 16px; font-weight: 700;
                              display: inline-block;">
                        ✅ Verificar Correo
                    </a>
                </div>
                <p style="color: #6b7280; font-size: 13px; text-align: center;">
                    Si no creaste esta cuenta, ignora este mensaje.<br>
                    Este enlace es de un solo uso.
                </p>
            </div>
            <div style="background: #111827; padding: 15px; text-align: center;">
                <p style="color: #4b5563; font-size: 12px; margin: 0;">
                    © 2025 SafeZone · Sistema de Reportes Viales
                </p>
            </div>
        </div>
        """
    )
    mail.send(msg)


@auth_bp.route("/")
@auth_bp.route("/login_html")
def login_html():
    return render_template("login.html")


@auth_bp.route("/register_html")
def register_page():
    return render_template("registro.html")


@auth_bp.route("/guest_login")
def guest_login():
    session['user_role'] = 'guest'
    session['user_id'] = 0
    session['username'] = 'Invitado'
    flash("Has ingresado como invitado. Funciones limitadas.", 'warning')
    return redirect(url_for("reports.registro_html"))


@auth_bp.route("/register", methods=["POST"])
def register():
    conn = get_db()
    if conn is None:
        flash("Error de conexión. Intenta de nuevo.", 'error')
        return redirect(url_for('auth.register_page'))

    nombres = request.form.get('registerNombres', '').strip()
    apellidos = request.form.get('registerApellidos', '').strip()
    nombre_usuario = f"{nombres} {apellidos}".strip()
    telefono = request.form.get('registerPhone', '').strip()
    correo = request.form.get('registerEmail', '').strip()
    contrasena = request.form.get('registerPassword', '')

    if not all([nombre_usuario, correo, contrasena, telefono]):
        flash("Todos los campos son obligatorios.", 'error')
        return redirect(url_for('auth.register_page'))

    hashed_password = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    token = str(uuid.uuid4())

    serializer = URLSafeTimedSerializer(SECRET_KEY)
    timed_token = serializer.dumps(token, salt='email-confirm')

    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Usuarios
               (nombre_usuario, correo_electronico, contrasena_hash, telefono, codigo_verificacion, verificado)
               VALUES (%s, %s, %s, %s, %s, 0)""",
            (nombre_usuario, correo, hashed_password, telefono, token),
        )
        conn.commit()
        _send_verification_email(correo, nombre_usuario, timed_token)
        flash(
            "Te enviamos un correo. Haz clic en el botón 'Verificar Correo' para activar tu cuenta.",
            'success')
        return redirect(url_for('auth.esperando_verificacion'))

    except mysql.connector.IntegrityError:
        flash("El correo electrónico ya está registrado.", 'error')
    except Exception as e:
        logging.error(f"Error al crear la cuenta: {e}", exc_info=True)
        flash(f"Error al crear la cuenta: {str(e)}", 'error')
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

    return redirect(url_for('auth.register_page'))


@auth_bp.route("/esperando_verificacion")
def esperando_verificacion():
    return render_template("esperando_verificacion.html")


@auth_bp.route("/verificar/<timed_token>")
def verificar_token(timed_token):

    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        # Verifica si el token expiró (24 horas = 86400 segundos)
        token = serializer.loads(
            timed_token,
            salt='email-confirm',
            max_age=86400)
    except SignatureExpired:
        flash(
            "El enlace de verificación ha expirado (validez de 24 horas). Por favor, solicita de nuevo o vuelve a registrarte.",
            'error')
        return render_template("verificacion_invalida.html")
    except BadSignature:
        flash("El enlace de verificación es inválido o está corrupto.", 'error')
        return render_template("verificacion_invalida.html")

    conn = get_db()
    if conn is None:
        flash("Error de conexión.", 'error')
        return redirect(url_for('auth.login_html'))

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre_usuario FROM Usuarios WHERE codigo_verificacion = %s AND verificado = 0",
            (token,)
        )
        user = cursor.fetchone()

        if not user:
            return render_template("verificacion_invalida.html")

        cursor.execute(
            "UPDATE Usuarios SET verificado = 1, codigo_verificacion = NULL WHERE id = %s",
            (user['id'],)
        )
        conn.commit()

        session['user_id'] = user['id']
        session['username'] = user['nombre_usuario']
        session['user_role'] = 'user'
        session['foto_perfil'] = None  # Usuario recién verificado no tiene foto todavía
        flash("¡Cuenta activada exitosamente! Bienvenido al sistema.", 'success')
        return redirect(url_for('reports.inicio_html'))

    except Exception as e:
        logging.error(f"Error al verificar token: {e}", exc_info=True)
        flash(f"Error al verificar: {str(e)}", 'error')
        return redirect(url_for('auth.login_html'))
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    correo = request.form.get('loginEmail', '').strip()
    contrasena = request.form.get('loginPassword', '')
    user = get_user_by_email_with_role(correo)

    if not user:
        flash("Correo o contraseña incorrectos.", 'error')
        return redirect(url_for('auth.login_html'))

    if not bcrypt.check_password_hash(user['contrasena_hash'], contrasena):
        flash("Correo o contraseña incorrectos.", 'error')
        return redirect(url_for('auth.login_html'))

    # Verificación de correo solo para usuarios normales (no admins ni
    # técnicos)
    role_name = user.get('nombre_rol', 'usuario')
    if role_name not in ('admin_principal', 'admin_tecnico'):
        conn = get_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT verificado FROM Usuarios WHERE correo_electronico = %s", (correo,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row and row['verificado'] == 0:
                flash(
                    "Debes verificar tu correo antes de iniciar sesión.",
                    'warning')
                return redirect(url_for('auth.esperando_verificacion'))

    session['user_id'] = user['id']
    session['username'] = user['nombre_usuario']
    session['foto_perfil'] = user.get('foto_perfil')

    if role_name == 'admin_principal':
        session['user_role'] = 'admin_principal'
        flash("Bienvenido al panel de administración.", 'success')
        return redirect(url_for('admin.panel_admin'))
    elif role_name == 'admin_tecnico':
        session['user_role'] = 'admin_tecnico'
        flash("Bienvenido al panel técnico.", 'success')
        return redirect(url_for('admin.panel_tecnico'))
    else:
        session['user_role'] = 'user'
        flash("Bienvenido al sistema.", 'success')
        return redirect(url_for('reports.inicio_html'))


@auth_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    if 'user_id' not in session or session['user_role'] == 'guest':
        flash(
            "Debes iniciar sesión con tu cuenta para ver y actualizar tu perfil.",
            'error')
        return redirect(url_for('auth.login_html'))

    conn = get_db()
    if not conn:
        flash("Error de conexión.", 'error')
        return redirect(url_for('reports.inicio_html'))

    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        telefono = request.form.get("telefono", "").strip()
        direccion = request.form.get("direccion_residencia", "").strip()
        documento = request.form.get("numero_documento", "").strip()

        errores = []
        if not telefono or not direccion or not documento:
            errores.append(
                "Los campos Celular, Dirección y Documento son totalmente obligatorios.")
        elif len(telefono) != 10 or not telefono.isdigit():
            errores.append(
                "El número de celular debe contener exactamente 10 dígitos y solo números.")

        if documento and any(c.isalpha() for c in documento):
            errores.append(
                "El número de documento no puede contener ninguna letra.")

        if errores:
            for e in errores:
                flash(e, 'error')
        else:
            try:
                # Manejo de la foto de perfil
                foto = request.files.get("foto_perfil")
                foto_filename = session.get('foto_perfil')

                if foto and foto.filename:
                    ext = foto.filename.rsplit('.', 1)[1].lower() if '.' in foto.filename else ''
                    if ext in ALLOWED_EXTENSIONS:
                        filename = f"avatar_{session['user_id']}_{uuid.uuid4().hex[:8]}.{ext}"
                        # Eliminar foto anterior si existe
                        if foto_filename:
                            old_path = os.path.join(UPLOAD_FOLDER, foto_filename)
                            if os.path.exists(old_path):
                                try: os.remove(old_path)
                                except: pass
                        
                        foto.save(os.path.join(UPLOAD_FOLDER, filename))
                        foto_filename = filename
                        session['foto_perfil'] = filename
                    else:
                        flash("Formato de imagen no permitido.", 'error')

                cursor.execute("""
                    UPDATE Usuarios 
                    SET telefono = %s, direccion_residencia = %s, numero_documento = %s, foto_perfil = %s
                    WHERE id = %s
                """, (telefono, direccion, documento, foto_filename, session['user_id']))
                conn.commit()
                flash("Perfil guardado exitosamente.", 'success')
            except Exception as e:
                logging.error(f"Error actualizando perfil: {e}", exc_info=True)
                flash("Error técnico al actualizar el perfil.", 'error')

    cursor.execute(
        "SELECT nombre_usuario, correo_electronico, telefono, direccion_residencia, numero_documento, foto_perfil FROM Usuarios WHERE id = %s",
        (session['user_id'],
         ))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("perfil.html", user=user_data)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", 'info')
    return redirect(url_for('auth.login_html'))
