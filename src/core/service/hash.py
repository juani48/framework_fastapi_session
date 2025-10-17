import os
from passlib.context import CryptContext
import string
import secrets
import random
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_string(input: str) -> str:
    return pwd_context.hash(input)


def verify_string(input: str, hashed_value: str) -> bool:
    return pwd_context.verify(input, hashed_value)


def generate_password(length: int = 12, include_upper: bool = True, include_digits: bool = True, include_symbols: bool = True) -> str:
    if length <= 0:
        raise ValueError("length must be a positive integer")

    # Definir conjuntos de caracteres
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = os.getenv("HASH_SYMBOLS")  # Leer desde .env o usar valor por defecto

    # Construir el pool de caracteres y una lista de obligatorios para asegurar presencia de cada clase
    pool = list(lower)
    required = [secrets.choice(lower)]

    if include_upper:
        pool.extend(list(upper))
        required.append(secrets.choice(upper))

    if include_digits:
        pool.extend(list(digits))
        required.append(secrets.choice(digits))

    if include_symbols:
        pool.extend(list(symbols))
        required.append(secrets.choice(symbols))

    # Asegurar que la longitud solicitada pueda acomodar los caracteres obligatorios
    if length < len(required):
        raise ValueError(f"length must be at least {len(required)} for the chosen options")

    # Rellenar el resto con elecciones aleatorias del pool
    remaining = length - len(required)
    password_chars = required + [secrets.choice(pool) for _ in range(remaining)]

    # Mezclar de manera segura
    rand = random.SystemRandom()
    rand.shuffle(password_chars)

    return "".join(password_chars)