# import postgres
from psycopg2 import connect

def connect_to_sql():
    """
        Connect to PostgreSQL database on cloud

        return postgres connection
    """
    # Create a new client and connect to the server from cloud
    sql_url = "postgres://admin:DqzLVWbQx6WGGB1v06trija1zZ0dCMjg@dpg-cmoq7s6g1b2c73f6nsl0-a/study_partner_uhpx" # internal connection
    sql_connection = connect(sql_url)
    return sql_connection