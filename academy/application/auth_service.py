from academy.common.errors import AuthError

def login(users: dict):
    email = input("Email: ")
    password = input("Password: ")

    user = users.get(email)
    if not user or user.password != password:
        raise AuthError("Credenciales inválidas")

    if not user.is_active:
        raise AuthError("Usuario inactivo")

    return user
