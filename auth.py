from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from db import get_connection

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, senha FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[1], senha):
            session['user_id'] = user[0]
            session['email'] = email
            return redirect(url_for('listar_tarefas'))
        else:
            flash('E-mail ou senha incorretos')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
