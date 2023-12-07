RECO_COLLECTION = 'recommendations'
USERS_COLLECTION = 'users'

def Update_Recom_List(db, nationalId:str, IDs_list: list, Scores_list: list):
    """
        insert recommendation list for user

        Parameters
            nationalId -> nationalId of user that you want to update his content
            IDs_list: list -> list of recommended users' IDs list
            Scores_list: list -> list of recommended users' Scores list
    """
    try:
        # get recommendations collection
        rec_cols = db[RECO_COLLECTION]
        
        # Create a list of recommendations
        recommendations = [{'nationalId': ID, 'score': score} for ID, score in zip(IDs_list, Scores_list)]

        # update recommendations for user nationalId
        response = rec_cols.update_one( {'nationalId': nationalId}, {'$set': {'userRecommendations':recommendations}})
    except Exception as e:
        print(f"An error occurred in Update_Recom_List: {e}")

def get_all_available_IDs(db):
    try:
        # get users collection
        users_cols = db[USERS_COLLECTION]
        
        # get all users have not partners
        Available_users = users_cols.find({"isAvailable":True})

        # get nationalId of these users
        return [user['nationalId'] for user in Available_users]
    
    except Exception as e:
        print(f"An error occurred in get_all_available_IDs: {e}")
        return []

def get_all_content_for_available_users(db):
    """
        find all content for available users in recommendations collection

        Return
        IDs, contents -> id and content for all users
    """
    try:
        # Find all users with available IDs
        available_ids = get_all_available_IDs(db)
        rec_cols = db[RECO_COLLECTION]

        # get all nationalIds and contents of available users
        users = rec_cols.find({"nationalId": {"$in": available_ids}})
        IDs, contents = [], []
        for user in users:
            IDs.append(user['nationalId'])
            contents.append(f"{user['fieldOfStudy']} {user['specialization']} {''.join((content['skillName'] + ' ') * content['skillRate'] for content in user['userSkills'])}")
        return IDs, contents
    
    except Exception as e:
        print(f"An error occurred in get_all_content_for_available_users: {e}")
        return [], []
