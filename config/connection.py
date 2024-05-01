# import postgres
from psycopg2 import connect

def connect_to_sql():
    """
        Connect to PostgreSQL database on cloud

        return postgres connection
    """
    # Create a new client and connect to the server from cloud
    sql_url = "postgres://postgress:viTLZbbS2eREkQ6V5qKwKirxNT90zdha@dpg-con9lda1hbls73ff7gf0-a.oregon-postgres.render.com/study_partner_or6z" # External connection
    sql_connection = connect(sql_url)
    return sql_connection