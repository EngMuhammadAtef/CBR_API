class DB_Recommendations:
    def __init__(self):
        """
            Connect to database and get access for recommendations collection
        """
        # import MongoDB Client
        from pymongo.mongo_client import MongoClient

        # Create a new client and connect to the server from cloud
        # database link from cloud # dataAnalysis:khadiga
        uri = "mongodb+srv://MLrecommendation:atef@cluster0.lr1t0or.mongodb.net/?retryWrites=true&w=majority" 
        client = MongoClient(uri)
        
        # Connect to Database
        self.__db = client['test'] # database name

        # Connect to collection
        self.__collection = self.__db['recommendations']
        
    def insert_RecoList(self, nationalId:str, IDs_list: list, Scores_list: list):
        """
            insert recommendation list of user

            Parameters
            nationalId -> nationalId of user that you want to update his content
            IDs_list: list -> list of recommended users' IDs list
            Scores_list: list -> list of recommended users' Scores list
        """
        response = self.__collection.update_one( {'nationalId': nationalId}, {'$set': {'userRecommendations':[{'nationalId': IDs_list[i], 'score':Scores_list[i]} for i in range(len(IDs_list))]}})

    def get_all_content(self):
        """
            find all content in recommendations collection

            Return
            IDs, contents -> id and content for all users
        """
        # find all of users
        users = self.__collection.find()
        IDs, contents = [], []

        for user in users:
            IDs.append(user['nationalId'])
            contents.append( ' '.join([user['fieldOfStudy'], user['specialization'], ' '.join(content['skillName'] for content in user['userSkills'])]) )
        
        return IDs, contents
    