from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
import datetime
import os
import hashlib
from typing import Tuple
from backend.db import DB

# Password Hashing: https://nitratine.net/blog/post/how-to-hash-passwords-in-python/

class User:
    def __init__(self, db: DB) -> None:
        self._db = db
        self._key = os.getenv('MY_KEY', 'other')

    def check_password_match(self, email: str, password: str) -> int:
        query = f"select * from Users where email='{email}';"
        data = self._db.select_data(query)
        if data:
            key = data[0]['password']
            salt = data[0]['salt']
            new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            if not key == new_key:
                return -1
            data = data[0]
        else:
            return -1
        return int(data['id'])

    def check_email_match(self, email: str) -> int:
        query = f"select * from Users where email='{email}';"
        data = self._db.select_data(query)
        if data:
            data = data[0]
        else:
            return -1
        return int(data['id'])

    def create_new_user(self, email: str, password: str) -> bool:
        existing = self.check_email_match(email)
        if existing < 0:
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            data = {'email': email, 'password': key, 'salt': salt }
            self._db.insert_row_1('Users', data)
            return True
        else:
            return False

    # source: https://realpython.com/token-based-authentication-with-flask/#jwt-setup
    def encode_token(self, id: int) -> Tuple[str, int]:
        payload = { 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30),
                    'iat': datetime.datetime.utcnow(),
                    'sub': id}
        try:
            return encode(payload, self._key, algorithm='HS256'), 200
        except Exception as exc:
            return f"Failed to create an auth token: {exc}", 500

    # source: https://realpython.com/token-based-authentication-with-flask/#jwt-setup
    def decode_token(self, token: str) -> Tuple[str, int]:
        try:
            payload = decode(token, self._key)
            return payload['sub'], 200
        except ExpiredSignatureError:
            return 'Signature expired. Please log in again.', 400
        except InvalidTokenError:
            return 'Invalid token. Please log in again.', 400
