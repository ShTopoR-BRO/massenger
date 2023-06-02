import hashlib

def hash_password(password):
    """Хеширует пароль с использованием алгоритма SHA-256"""
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def verify_password(password, hashed_password):
    """Проверяет валидность пароля"""
    return hash_password(password) == hashed_password