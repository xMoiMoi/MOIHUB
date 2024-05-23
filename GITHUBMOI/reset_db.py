import sirope
from model.user import User
from model.code_file import CodeFile
from model.comment import Comment

def reset_database():
    srp = sirope.Sirope()

    # Borra todos los datos existentes de la base de datos
    srp.multi_delete(list(srp.load_all_keys(User)))
    srp.multi_delete(list(srp.load_all_keys(CodeFile)))
    srp.multi_delete(list(srp.load_all_keys(Comment)))
    print("Base de datos reseteada")

if __name__ == "__main__":
    reset_database()
