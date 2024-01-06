from json import dumps 

def Extract_Transform_Load(mongo_con, nationalId, sql_conn):
    """
        get all content of the new user(nationalId) from mongo_db and save in sql_db

        Parameters
            mongo_con -> connection of the mongo db
            nationalId -> nationalId of the new user
            sql_conn  -> connection of the SQL db
    """
    with sql_conn.cursor() as sql_cursor:
        try:
            # check if user already exist
            sql_cursor.execute(f"SELECT nationalId FROM user_content WHERE nationalId = '{nationalId}';")
            if sql_cursor.fetchone():
                return # stop
            
            # Extract new user content from mongoDB
            rec_cols = mongo_con['recommendations']
            new_user_content = rec_cols.find_one({'nationalId': nationalId}, { "_id": 0, "fieldOfStudy": 1, "specialization": 1, "userSkills": 1})
            users_cols = mongo_con['users']
            new_user_info = users_cols.find_one({'nationalId': nationalId}, { "_id": 0, "age": 1, "gender": 1, "location": 1})

            # transform content of the SQL table format
            bag_of_content = {}
            bag_of_content[new_user_content['fieldOfStudy']] = 5
            bag_of_content[new_user_content['specialization']] = 5
            for content in new_user_content['userSkills']:
                bag_of_content[content['skillName']] = content['skillRate']
            bag_of_content['age'] = new_user_info['age']
            bag_of_content['gender'] = 1 if new_user_info['gender']=='male' else 0
            bag_of_content['longitude'], bag_of_content['latitude'] = list(map(int, new_user_info['location'].split()))

            # load new data in SQL_DB
            new_user = (nationalId, dumps(bag_of_content))
            sql_cursor.execute(f"INSERT INTO user_content VALUES (%s, %s)", new_user)
            sql_conn.commit()

        except:
            sql_conn.rollback()