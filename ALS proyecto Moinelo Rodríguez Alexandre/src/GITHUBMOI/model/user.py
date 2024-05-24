import flask_login
import sirope
import werkzeug.security as safe

class User(flask_login.UserMixin):
    def __init__(self, email, pswd):
        self.email = email
        self.pswd = safe.generate_password_hash(pswd)

    def get_id(self):
        return self.email

    def chk_pswd(self, other_pswd):
        return safe.check_password_hash(self.pswd, other_pswd)

    @staticmethod
    def current():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None

        return usr

    @staticmethod
    def find(srp: sirope.Sirope, email: str) -> "User":
        return srp.find_first(User, lambda u: u.email == email)
