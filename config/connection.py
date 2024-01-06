# import postgres & MongoDB
import psycopg2
from pymongo.mongo_client import MongoClient

def connect_to_sql():
    """
        Connect to PostgreSQL database on cloud

        return postgres connection
    """
    # Create a new client and connect to the server from cloud
    sql_url = "postgres://admin:Nt4y3kTzTQE28PZkVPDqZG0eNYam2Rb0@dpg-cmauojta73kc73bnk7cg-a/study_partner_xiby"
    sql_connection = psycopg2.connect(sql_url)
    return sql_connection

def connect_to_mongo():
    """
        Connect to mongo database on cloud

        return mongo connection
    """
    # Create a new client and connect to the server from cloud
    mongo_url = "mongodb+srv://MLrecommendation:atef@cluster0.lr1t0or.mongodb.net/?retryWrites=true&w=majority" 
    mongo_connection = MongoClient(mongo_url)['test'] # database name
    return mongo_connection