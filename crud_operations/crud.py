def Update_Recom_List(db, nationalId:str, IDs_list: list, Scores_list: list):
    """
        insert recommendation list of user

        Parameters
        nationalId -> nationalId of user that you want to update his content
        IDs_list: list -> list of recommended users' IDs list
        Scores_list: list -> list of recommended users' Scores list
    """
    collection = db['recommendations']
    response = collection.update_one( {'nationalId': nationalId}, {'$set': {'userRecommendations':[{'nationalId': IDs_list[i], 'score':Scores_list[i]} for i in range(len(IDs_list))]}})

def get_all_available_IDs(db):
    # Connect to users collection
    collection = db['users']
    users = collection.find({"isAvailable":True})
    NIDs = []
    for user in users:
        NIDs.append(user['nationalId'])
    return NIDs

def get_all_content_for_available_users(db):
    """
        find all content for available users in recommendations collection

        Return
        IDs, contents -> id and content for all users
    """
    # find all of users
    collection = db['recommendations']
    users = collection.find({"nationalId": {"$in": get_all_available_IDs(db)}})
    IDs, contents = [], []

    for user in users:
        IDs.append(user['nationalId'])
        contents.append(' '.join([ user['fieldOfStudy'], user['specialization'], ''.join((content['skillName']+' ')*content['skillRate'] for content in user['userSkills']) ]))
    return IDs, contents
