from io import BytesIO

import pymysql
import traceback
import pandas as pd

from src.BoschRpaMagicBox.smb_functions import smb_store_remote_file_by_obj


def start_mysql_server_connection(host, port, user, password, database):
    """ This function is used to connect to the MySQL server.

    Args:
        host(str): The host of the MySQL server.
        port(int): The port of the MySQL server.
        user(str): The user of the MySQL server.
        password(str): The password of the MySQL server.
        database(str): The database of the MySQL server.

    """
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print('MySQL connection is ready!')
    return connection


def close_mysql_server_connection(connection):
    """ This function is used to close the MySQL server connection.

    Args:
        connection(pymysql.connections.Connection): The MySQL server connection.
    """
    if connection:
        connection.close()
        print("MySQL connection is closed!")
    else:
        print("No MySQL connection to close!")


def execute_mysql_query(connection, sql_query):
    """ This function is used to execute a MySQL query.

    Args:
        connection(pymysql.connections.Connection): The MySQL server connection.
        sql_query(str): The SQL query to execute.

    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def fetch_data_from_mysql_server(host, port, user, password, database, sql_query):
    """

    Args:
        host(str): The host of the MySQL server.
        port(int): The port of the MySQL server.
        user(str): The user of the MySQL server.
        password(str): The password of the MySQL server.
        database(str): The database of the MySQL server.
        sql_query(str): The SQL query to execute.

    """
    connection = None
    try:
        connection = start_mysql_server_connection(host, port, user, password, database)
        if connection:
            results = execute_mysql_query(connection, sql_query)
            close_mysql_server_connection(connection)
            return results
        else:
            print("Failed to connect to MySQL server.")
            return None
    except:
        print(f"Error connecting to MySQL server:\n{traceback.format_exc()}")
        close_mysql_server_connection(connection)
        return None


def save_mysql_data_to_excel(host, mysql_port, mysql_user, mysql_password, database, sql_query, username, password, server_name, share_name, remote_file_path, port=445,
                             sheet_name='Sheet1'):
    """
    This function is used to save MySQL data to a CSV file.

    Args:
        host(str): The host of the MySQL server.
        mysql_port(int): The port of the MySQL server.
        mysql_user(str): The user of the MySQL server.
        mysql_password(str): The password of the MySQL server.
        database(str): The database of the MySQL server.
        sql_query(str): The SQL query to execute.
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
        sheet_name(str): The name of the sheet in the Excel file.

    """
    try:
        fetch_data = fetch_data_from_mysql_server(host, mysql_port, mysql_user, mysql_password, database, sql_query)
        if fetch_data is not None:
            df_data = pd.DataFrame(fetch_data)
            file_obj = BytesIO()

            with pd.ExcelWriter(file_obj, engine='xlsxwriter') as writer:
                df_data.to_excel(writer, index=False, sheet_name=sheet_name)
            file_obj.seek(0)

            smb_store_remote_file_by_obj(username, password, server_name, share_name, remote_file_path, file_obj, port)
        else:
            print("No data fetched from MySQL server.")
    except:
        print(f"Error saving MySQL data to Excel:\n{traceback.format_exc()}")
