from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
import datetime
import os

class User:
    def __init__(self, db):
        self._db = db
        self._key = os.getenv('MY_KEY', 'other')

    def check_password_match(self, email, password):
        query = f"select * from Users where email='{email}' and password='{password}';"
        data = self._db.select_data(query)
        if data:
            data = data[0]
        else:
            return -1
        return int(data['id'])

    def check_email_match(self, email):
        query = f"select * from Users where email='{email}';"
        data = self._db.select_data(query)
        if data:
            data = data[0]
        else:
            return -1
        return int(data['id'])

    def create_new_user(self, email, password):
        existing = self.check_email_match(email)
        if existing < 0:
            data = {'email': f"'{email}'", 'password': f"'{password}'"}
            self._db.insert_row('Users', data)
            return True
        else:
            return False

    # source: https://realpython.com/token-based-authentication-with-flask/#jwt-setup
    def encode_token(self, id):
        payload = { 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30),
                    'iat': datetime.datetime.utcnow(),
                    'sub': id}
        try:
            return encode(payload, self._key, algorithm='HS256'), 200
        except Exception as exc:
            return f"Failed to create an auth token: {exc}", 500

    # source: https://realpython.com/token-based-authentication-with-flask/#jwt-setup
    def decode_token(token):
        try:
            payload = decode(token, self._key)
            return payload['sub'], 200
        except ExpiredSignatureError:
            return 'Signature expired. Please log in again.', 400
        except InvalidTokenError:
            return 'Invalid token. Please log in again.', 400
