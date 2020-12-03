from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
import datetime
import os
import hashlib
from typing import Tuple
from backend.db import DB
from backend.setup.config import MY_KEY

# Password Hashing: https://nitratine.net/blog/post/how-to-hash-passwords-in-python/

class User:
    """
    A class used to represent the User. 

    ...

    Attributes
    ----------
    _db : DB
        The database manager.
    _key : int
        The unique user id.

    Methods
    -------
    check_password_match(email: str, password: str) -> int
        Checks if the user password matches with the one stored in the database.
    check_email_match(email: str) -> int
        Checks if a similar email is present in the database.
    create_new_user(email: str, password: str, fullname: str) -> bool
        Creates a new user.
    encode_token(id: int) -> Tuple[str, int]
        Encodes token for authentication.
    decode_token(token: str) -> Tuple[str, int]
        Decodes token for authentication.
    """
    def __init__(self, db: DB) -> None:
        """
        Initialize the user.
        
        Parameters
        ----------
        db : DB
            The database manager.
        """
        self._db = db
        self._key = MY_KEY

    def check_password_match(self, email: str, password: str) -> int:
        """
        Checks if the user password matches with the one in the database.

        Parameters
        ----------
        email : str
            The user email id.
        password : str
            The entered password
            
        Returns
        -------
        id : int
            The user id.
        """
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
        """
        Checks is the user is already registered. If True returns the user id.
        
        Parameters
        ----------
        email : str
            The user email.
        
        Returns
        -------
        id : int
            The user id.
        """
        query = f"select * from Users where email='{email}';"
        data = self._db.select_data(query)
        if data:
            data = data[0]
        else:
            return -1
        return int(data['id'])

    def create_new_user(self, email: str, password: str, fullname: str) -> bool:
        """
        Creates a new user using password hashing.
        
        Parameters
        ----------
        email : str
            The user email id.
        password : str
            The entered user password.
        fullname : str
            The users full name.
        
        Returns
        -------
        success : bool
            True if a new user is created otherwise False.
        """
        existing = self.check_email_match(email)
        if existing < 0:
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            data = {'email': email, 'password': key, 'salt': salt, 'fullname': fullname}
            self._db.insert_row_1('Users', data)
            return True
        else:
            return False

    # source: https://realpython.com/token-based-authentication-with-flask/#jwt-setup
    def encode_token(self, id: int) -> Tuple[str, int]:
        """
        Encodes token
        
        Parameters
        ----------
        id : int
        
        Returns
        -------
        encoding : str
            The payload encoding.
        code : int
            Success code.
        """
        payload = { 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=10),
                    'iat': datetime.datetime.utcnow(),
                    'sub': id}
        try:
            return encode(payload, self._key, algorithm='HS256'), 200
        except Exception as exc:
            return f"Failed to create an auth token: {exc}", 500

    # source: https://realpython.com/token-based-authentication-with-flask/#jwt-setup 
    def decode_token(self, token: str) -> Tuple[str, int]:
        """
        Decodes token
        
        Parameters
        ----------
        token : str
            The token
            
        Returns
        -------
        payload : str
            The payload
        code : int
            Success code.
        """
        try:
            payload = decode(token, self._key, algorithms=['HS256'])
            return payload['sub'], 200
        except ExpiredSignatureError:
            return 'Signature expired. Please log in again.', 401
        except InvalidTokenError:
            return 'Invalid token. Please log in again.', 401


