def get_all_content(sql_conn):
    """
        find all content from SQL_DB

        Parameters
            sql_conn[con object] -> connection of database

        Return
            Data [dict] -> id and content for all users
    """
    # Find all users content
    with sql_conn.cursor() as sql_cursor:
        try:
            sql_cursor.execute("SELECT nationalId, bag_of_content FROM user_content;")
            data = {nationalId: content for nationalId, content in sql_cursor.fetchall()}
            return data
        
        except:
            sql_conn.rollback()
            return dict()

def get_all_ratings(sql_conn):
    """
        find all ratings for user to partners from SQL_DB

        Parameters
            sql_conn[con object] -> connection of database

        Return
            Ratings_Data [dict] -> id and rating for each user_partner
    """
    # Find all users content
    with sql_conn.cursor() as sql_cursor:
        try:
            sql_cursor.execute(f"SELECT * FROM user_rating;")
            data = sql_cursor.fetchall()
            return data
        
        except:
            sql_conn.rollback()
            return tuple()
