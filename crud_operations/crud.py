RECO_COLLECTION = 'recommendations'

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

def get_all_content(db):
    """
        find all content in recommendations collection

        Parameters
            db -> connection of database

        Return
            IDs, contents -> id and content for all users
    """
    try:
        def concatenate_skills(user_skills):
            return {
                "$reduce": {
                    "input": user_skills,
                    "initialValue": "",
                    "in": {"$concat": ["$$value", " ", "$$this.skillName"]}
                }
            }

        # Find all users
        rec_cols = db[RECO_COLLECTION]

        # get all nationalIds and contents of available users
        users = [*rec_cols.aggregate([{"$project": {"_id": 0, "nationalId": 1, "bag_of_content": {"$concat": ['$fieldOfStudy', ' ', '$specialization', ' ', concatenate_skills("$userSkills")]}} }])]
        
        IDs, contents = [], []
        for user in users:
            IDs.append(user['nationalId'])
            contents.append(user['bag_of_content'])
        return IDs, contents
    
    except Exception as e:
        print(f"An error occurred in get_all_content(): {e}")
        return [], []
