from db import DB

class User:
    def __init__(self):
        self._db = DB()

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
            self._db.inset_row('Users', data)
            return True
        else:
            return False
