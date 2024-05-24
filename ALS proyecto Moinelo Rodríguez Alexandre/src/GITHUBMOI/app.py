import json
import flask
import flask_login
import sirope
import os
from model.user import User
from model.code_file import CodeFile
from model.comment import Comment
from views.user import user_blpr
from views.code_file import code_file_blpr

def create_app():
    flapp = flask.Flask(__name__)
    sirop = sirope.Sirope()
    login = flask_login.LoginManager()

    flapp.config.from_file("instance/config.json", json.load)
    flapp.secret_key = flapp.config["SECRET_KEY"]
    login.init_app(flapp)
    flapp.register_blueprint(user_blpr)
    flapp.register_blueprint(code_file_blpr, url_prefix='/code_file')
    return flapp, sirop, login

app, srp, lm = create_app()

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized access", "error")
    return flask.redirect("/")

@lm.user_loader
def user_loader(email: str) -> User:
    return User.find(srp, email)

@app.route("/favicon.ico")
def get_fav_icon():
    return app.send_static_file("favicon.ico")

@app.route("/login", methods=["POST"])
def login():
    if User.current():
        flask_login.logout_user()
        flask.flash("Ha pasado algo extraño. Por favor, entra de nuevo.", "error")
        return flask.redirect("/")

    usr_email = flask.request.form.get("email", "").strip()
    usr_pswd = flask.request.form.get("password", "").strip()

    if not usr_email or not usr_pswd:
        flask.flash("Credenciales incompletas", "error")
        return flask.redirect("/")

    usr = User.find(srp, usr_email)

    if not usr or not usr.chk_pswd(usr_pswd):
        flask.flash("Credenciales incorrectas: ¿has hecho el registro?", "error")
        return flask.redirect("/")

    flask_login.login_user(usr)
    
    return flask.redirect("/dashboard")

@app.route("/logout", methods=["POST"])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if flask.request.method == "POST":
            email = flask.request.form.get("email", "").strip()
            password = flask.request.form.get("password", "").strip()

            if not email or not password:
                flask.flash("Por favor, introduce un correo electrónico y una contraseña válidos.", "error")
                return flask.redirect("/register")

            existing_user = User.find(srp, email)
            if existing_user:
                flask.flash("Este correo electrónico ya está registrado. Por favor, utiliza otro.", "error")
                return flask.redirect("/register")

            user = User(email, password)
            srp.save(user)
            flask.flash("¡Registro exitoso! Por favor, inicia sesión.", "success")
            return flask.redirect("/")

    except Exception as e:
        app.logger.error('Error during registration: %s', e)
        flask.flash("Ha ocurrido un error durante el registro. Inténtalo de nuevo.", "error")
        return flask.redirect("/register")

    return flask.render_template("register.html")


@app.route("/", methods=["GET", "POST"])
def main():
    if flask.request.method == "POST":
        usr_email = flask.request.form.get("email", "").strip()
        usr_pswd = flask.request.form.get("password", "").strip()

        if not usr_email or not usr_pswd:
            flask.flash("Credenciales incompletas", "error")
            return flask.redirect("/")

        usr = User.find(srp, usr_email)

        if not usr or not usr.chk_pswd(usr_pswd):
            flask.flash("Credenciales incorrectas: ¿has hecho el registro?", "error")
            return flask.redirect("/")

        flask_login.login_user(usr)
        return flask.redirect("/dashboard")

    usr = User.current()
    if usr is None:
        return flask.render_template("index.html", usr=None, srp=srp)

    code_files = list(srp.load_all(CodeFile))

    sust = {
        "usr": usr,
        "code_files": code_files,
        "srp": srp
    }

    return flask.render_template("index.html", **sust)

@app.route("/dashboard", methods=["GET"])
@flask_login.login_required
def dashboard():
    code_files = list(srp.load_all(CodeFile))
    return flask.render_template("dashboard.html", code_files=code_files, srp=srp)

@app.route("/upload_code", methods=["GET", "POST"])
@flask_login.login_required
def upload_code():
    # Aquí va la lógica para subir código
    return "Upload Code Page"

@app.route("/my_codes", methods=["GET"])
@flask_login.login_required
def my_codes():
    # Aquí va la lógica para mostrar los códigos del usuario
    return "My Codes Page"

@app.route("/reset_db", methods=["POST"])
def reset_db():
    srp = sirope.Sirope()

    # Borra todos los datos existentes de la base de datos
    srp.multi_delete(list(srp.load_all_keys(User)))
    srp.multi_delete(list(srp.load_all_keys(CodeFile)))
    srp.multi_delete(list(srp.load_all_keys(Comment)))
    flask.flash("Base de datos reseteada", "success")
    return flask.redirect("/")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
