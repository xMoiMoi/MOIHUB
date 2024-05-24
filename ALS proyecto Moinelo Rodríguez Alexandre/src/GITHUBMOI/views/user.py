from flask import Blueprint, request, redirect, flash
from flask_login import login_user
from model.user import User
import sirope
import werkzeug.security as safe

user_blpr = Blueprint('user', __name__, url_prefix='/user')

@user_blpr.route('/add', methods=['POST'])
def user_add():
    srp = sirope.Sirope()
    email = request.form.get('edEmail', '').strip()
    pswd_hash = request.form.get('edPswd', '').strip()

    if not email or not pswd_hash:
        flash('Email y contraseña requeridos')
        return redirect('/')

    usr = User(email, pswd_hash)
    if User.find(srp, email):
        flash('Usuario ya existe')
        return redirect('/')

    srp.save(usr)
    login_user(usr)
    flash('Usuario registrado y logueado')
    return redirect('/')
