RECO_COLLECTION = 'recommendations'

def Update_Recom_List(db, nationalId:str, IDs_Scores: dict):
    """
        insert recommendation list for user

        Parameters
            nationalId -> nationalId of user that you want to update his content
            IDs_Scores[dict] -> users' IDs and users' Scores
    """
    try:
        # get recommendations collection
        rec_cols = db[RECO_COLLECTION]
        
        # Create a list of recommendations
        recommendations = [{'nationalId': ID, 'score': score} for ID, score in IDs_Scores.items()]

        # update recommendations for user nationalId
        response = rec_cols.update_one( {'nationalId': nationalId}, {'$set': {'userRecommendations':recommendations}})
    except Exception as e:
        print(f"An error occurred in Update_Recom_List: {e}")

def get_all_content(db):
    """
        find all content in recommendations collection

        Parameters
            db[con object] -> connection of database

        Return
            IDs, contents -> id and content for all users
    """
    try:
        # Find all users
        rec_cols = db[RECO_COLLECTION]

        # get all nationalIds and contents
        users = [*rec_cols.aggregate([{"$project": {"_id": 0, "nationalId": 1, "bag_of_content": {"$concat": ['$fieldOfStudy', ' ', '$specialization', ' ', {"$reduce": {"input": "$userSkills", "initialValue": "", "in": {"$concat": ["$$value", " ", "$$this.skillName"]}}}]}}}])]
        
        IDs, contents = [], []
        for user in users:
            IDs.append(user['nationalId'])
            contents.append(user['bag_of_content'])
        return IDs, contents
    
    except Exception as e:
        print(f"An error occurred in get_all_content(): {e}")
        return [], []
