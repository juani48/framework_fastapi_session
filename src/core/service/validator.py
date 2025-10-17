def validate_signin_json(data: dict):
    for field in ["name", "email", "password", "confirm_password", "last_name"]:
        if field not in data or not isinstance(data[field], str) or len(data[field]) == 0:
            raise ValueError(f"Falta el campo obligatorio: {field}.")
        if not isinstance(data[field], str) or len(data[field]) == 0:
            raise ValueError(f"El campo {field} es inválido.")
    if data["password"] != data["confirm_password"]:
        raise ValueError("Las contraseñas no coinciden.")
    return

def validate_login_json(data: dict):
    for field in ["email", "password"]:
        if field not in data or not isinstance(data[field], str) or len(data[field]) == 0:
            raise ValueError(f"Falta el campo obligatorio: {field}.")
        if not isinstance(data[field], str) or len(data[field]) == 0:
            raise ValueError(f"El campo {field} es inválido.")
    return