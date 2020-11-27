import pymysql
import datetime
from typing import Any, List, Dict

class DB:
    def __init__(self, host: str = 'localhost', user: str = 'root',
                 password: str = 'naveena1999', db: str = 'cs130') -> None:
        self._host = host
        self._user = user
        self._password = password
        self._db = db

    def _get_connection(self) -> pymysql.connections.Connection:
        connection = pymysql.connect(host=self._host, user=self._user, password=self._password, db=self._db)
        return connection

    def _close_connection(self, connection: pymysql.connections.Connection) -> None:
        connection.close()

    def select_data(self, query: str) -> List:
        connection = self._get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        self._close_connection(connection)
        return data

    def insert_data(self, cmd: str) -> None:
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(cmd)
        connection.commit()
        self._close_connection(connection)
        
    def insert_data_1(self, cmd: str, values) -> None:
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(cmd, values)
        connection.commit()
        self._close_connection(connection)

    def insert_row(self, table: str, data_dict: Dict[str, Any]) -> None:
        keys = ""
        vals = ""
        for k, v in data_dict.items():
            keys += k + ', '
            vals += str(v) + ', '
        keys = keys[:-2]
        vals = vals[:-2]
        cmd = f"insert into {table} ({keys}) values ({vals});"
        self.insert_data(cmd)
        
    def insert_row_1(self, table: str, data_dict: Dict[str, Any]) -> None:
        keys = ""
        vals = ""
        data = []
        for k, v in data_dict.items():
            keys += k + ', '
            vals += "%s" + ', '
            data.append(v)
        keys = keys[:-2]
        vals = vals[:-2]
        cmd = f"insert into {table} ({keys}) values ({vals});"
        self.insert_data_1(cmd,data)

    def sel_time_frame(self, table: str, start_date: str, end_date: str, userID: int, params: str = "*"):
        query = f"select {params} from {table} "
        query += f"join Users on Users.id={table}.UserID "
        query += f"where Datetime >= '{start_date}' and Datetime <= '{end_date}' "
        query += f"and Users.id = '{userID}';"
        data = self.select_data(query)
        return data
