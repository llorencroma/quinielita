import re
import json
import os
from functools import lru_cache

# ---------- ruta del archivo de credenciales ----------
SECRETS_FILE = "../../config_quiniela/credentials.json"

# ---------- valores por defecto (por si falta el archivo) ----------
DEFAULTS = {
    "admin_password": "admin123",
    "pin": "1234"
}

# ---------- helpers ------------------------------------
@lru_cache(maxsize=1)
def _load_secrets() -> dict:
    """
    Lee el JSON de credenciales una sola vez y lo memoriza.
    Estructura esperada:
    {
        "admin_password": "superSecreta",
        "pin": "9876"
    }
    """
    if os.path.exists(SECRETS_FILE):
        try:
            with open(SECRETS_FILE, encoding="utf-8") as f:
                data = json.load(f)
                # combinamos con defaults para campos faltantes
                merged = {**DEFAULTS, **data}
                return merged
        except (json.JSONDecodeError, IOError):
            print("Going to basics")

            pass  # devolverá DEFAULTS
    return DEFAULTS


# ---------- validaciones públicas ----------------------
def authenticate_admin(password_input: str) -> bool:
    """Devuelve True si la contraseña coincide con la almacenada."""
    return password_input == _load_secrets()["admin_password"]


def validate_phone(phone: str) -> bool:
    """
    Teléfono español:
      · 9 dígitos iniciando en 6-9           → 612345678
      · o con prefijo +34 / 0034            → +34612345678   0034612345678
    """
    pattern = r"^(?:\+34|0034)?[6-9]\d{8}$"
    return bool(re.fullmatch(pattern, phone.strip()))


def validate_name(name: str) -> bool:
    """Letras, espacios y algunos signos; 2-50 caracteres."""
    pattern = r"^[A-Za-zÀ-ÿ ,.'-]{2,50}$"
    return bool(re.fullmatch(pattern, name.strip()))


def validate_pin(pin_input: str) -> bool:
    """True si el PIN coincide con el configurado en backend."""
    return pin_input == _load_secrets()["pin"]
