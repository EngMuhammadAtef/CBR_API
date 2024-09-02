# import postgres
from psycopg2 import connect

def connect_to_sql():
    """
        Connect to PostgreSQL database on cloud

        return postgres connection
    """
    # Create a new client and connect to the server from cloud
    sql_url = "postgres://avnadmin:AVNS_eDPshr2eBUNqe9ATnWC@pg-33025b18-project-541f.h.aivencloud.com:21402/defaultdb?sslmode=require"
    sql_connection = connect(sql_url)
    return sql_connection
