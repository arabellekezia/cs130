import pymysql

class DB:
    def __init__(self, host, user, password, db):
        self._host = host
        self._user = user
        self._password = password
        self._db = db

    def get_connection(self):
        connection = pymysql.connect(host=self._host, user=self._user, password=self._password, db=self._db)
        return connection

    def close_connection(self, connection):
        connection.close()

    def select_data(self, query):
        connection = self.get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        self.close_connection(connection)
        return data

    def insert_data(self, cmd):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(cmd)
        connection.commit()
        self.close_connection(connection)

    def insert_row(self, table, data_dict):
        keys = ""
        vals = ""
        for k, v in data_dict.items():
            keys += k + ', '
            vals += v + ', '
        keys = keys[:-2]
        vals = vals[:-2]
        cmd = f"insert into {table} ({keys}) values ({vals});"
        self.insert_data(cmd)

    def sel_time_frame(self, table, start_date, end_date, userID, params="*"):
        query = f"select {params} from {table} "
        query += f"join Users on Users.id={table}.UserID "
        query += f"where date >= {start_date} and date <= {end_date};"
        data = self.select_data(query)
        return data

    def get_sleep_minutes(self, start_date, end_date, userID):
        data = self.sel_time_frame("Sleep", start_date, end_date, userID, params="Minutes")
        return data

    def get_goals(self, userID):
        query = f"select * from Goals join Users on Users.id={table}.UserID;"
        data = self.sel_data(query)
        return data

