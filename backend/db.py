import pymysql
import datetime
from typing import Any, List, Dict, Optional
from backend.setup.config import TEST_DB, PRODUCTION_DB

class DB:
    """
    This class contains the code to access and connect with the database safely.

    ...

    Attributes
    ----------
    _host : str
        Hostname for the database server. (Private member variable)
    _user : str
        Username for the database server. (Private member variable)
    _password : str
        Password to connect to the database. (Private member variable)
    _db : str
        Name of the database to connect to. (Private member variable)

    Methods
    -------
    _get_connection() -> pymysql.connections.Connection
        Get a connection to the database with the credentials in the config. (Private member method)
    _close_connection(connection: pymysql.connections.Connection) -> None
        Close the given connection to a database. (Private member method)
    select_data(query: str) -> List
        Run a select statement in the database based on the entered query and return the data from database.
    insert_data(cmd: str) -> None
        Run an insert or alter statement that enters a command in the database without expecting a return value.
    insert_data_1(cmd: str, values: List[Any]) -> None
        Create an insert command and format the values and insert the data in the database, this formats
        the values for mysql without the user needing to.
    insert_row(table: str, data_dict: Dict[str, Any]) -> None
        Given a table name and the data dict of keys and values to enter (formatted in mysql style),
        insert the new row in the database.
    insert_row_1(table: str, data_dict: Dict[str, Any]) -> None
        Given a table name and the data dict of keys and values to enter, this formats in mysql style and
        insert the new row in the database.
    sel_time_frame(table: str, start_date: str, end_date: str, userID: int, params: Optional[str] = "*") -> List
        Given the parameters, construct a query within the specified dates and return the data from the database.
    """
    def __init__(self, test: Optional[bool] = True) -> None:
        """
        Initialization for this class, it takes in one bool for production vs. test instance and uses the
        config file.

        Parameters
        ----------
        test : Optional[bool]
            This boolean parameter determones whether to use the test or production instance of the database.
        """
        config_info = TEST_DB
        if not test:
            config_info = PRODUCTION_DB
        self._host = config_info['host']
        self._user = config_info['user']
        self._password = config_info['password']
        self._db = config_info['db']

    def _get_connection(self) -> pymysql.connections.Connection:
        """
        Get a connection to the database with the credentials in the config. (Private member method)

        Parameters
        ----------
        test : Optional[bool]
            This boolean parameter determones whether to use the test or production instance of the database.

        Returns
        -------
        connection : pymysql.connections.Connection
            The pymysql connection object to the database.
        """
        connection = pymysql.connect(host=self._host, user=self._user, password=self._password, db=self._db)
        return connection

    def _close_connection(self, connection: pymysql.connections.Connection) -> None:
        """
        Close the given connection to a database. (Private member method)

        Parameters
        ----------
        connection : pymysql.connections.Connection
                The pymysql connection object to the database.
        """
        connection.close()

    def select_data(self, query: str) -> List:
        """
        Run a select statement in the database based on the entered query and return the data from database.

        Parameters
        ----------
        query : str
            The query to run and get data based on in the database.

        Returns
        -------
        data : List
            List of dictionary entries for corresponding rows in the database that match the search query.
        """
        connection = self._get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        self._close_connection(connection)
        return data

    def insert_data(self, cmd: str) -> None:
        """
        Run an insert or alter statement that enters a command in the database without expecting a return value.

        Parameters
        ----------
        cmd : str
            Command to enter or alter data in thre database.
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(cmd)
        connection.commit()
        self._close_connection(connection)
        
    def insert_data_1(self, cmd: str, values: List[Any]) -> None:
        """
        Create an insert command and format the values and insert the data in the database, this formats
        the values for mysql without the user needing to.

        Parameters
        ----------
        cmd : str
            Command to enter or alter data in thre database.
        values: List[Any]
            Values to enter in the database, these do not have to be formatted as per mysql.
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(cmd, values)
        connection.commit()
        self._close_connection(connection)

    def insert_row(self, table: str, data_dict: Dict[str, Any]) -> None:
        """
        Given a table name and the data dict of keys and values to enter (formatted in mysql style),
        insert the new row in the database.

        Parameters
        ----------
        table: str
            Name of table in databsase.
        data_dict: Dict[str, Any]
            Dictionary of keys and values that correspond to fields in the database, formatted in mysql style.
        """
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
        """
        Given a table name and the data dict of keys and values to enter, this formats in mysql style and
        insert the new row in the database.

        Parameters
        ----------
        table: str
            Name of table in databsase.
        data_dict: Dict[str, Any]
            Dictionary of keys and values that correspond to fields in the database.
        """
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

    def sel_time_frame(self, table: str, start_date: str, end_date: str, userID: int, params: Optional[str] = "*") -> List:
        """
        Given the parameters, construct a query within the specified dates and return the data from the database.

        Parameters
        ----------
        table: str
            Name of table in databsase.
        start_date: str
            Starting date value for the range to check for values.
        end_date: str
            Starting date value for the range to check for values.
        userID: int
            Foreign key constraint of userID to search for a single, specific user.
        params: Optional[str]
            Specific fields to return for each row of database, defaulted to all fields per row.

        Returns
        -------
        data : List
            Data selected from the database based on given criteria as a List of Dict entries where each Dict
            correspionds to a row in the database.
        """
        query = f"select {params} from {table} "
        query += f"join Users on Users.id={table}.UserID "
        query += f"where Datetime >= '{start_date}' and Datetime <= '{end_date}' "
        query += f"and Users.id = '{userID}';"
        data = self.select_data(query)
        return data
