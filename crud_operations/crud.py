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
