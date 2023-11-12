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

    def print_all(self, query={}):
        """
            find all users in recommendations collection

            Parameters
            query[dict] -> filter query   ex:// {'fieldOfStudy': 'Computer Science'} 

            Return
            collection content from database
        """
        try:
            # connect to db and find content
            users = self.__collection.find(query)

            # print all users in db
            for user in users:
                print(user)
                print("#"*100)

        except Exception as e:
            print(e)

    def print_all_users(self):
        # Connect to users collection
        self.__users = self.__db['users']
        users = self.__users.find()
        for user in users:
            print(user)
            print("#"*100)

    def insert_user(self, fieldOfStudy, specialization, skills, skills_level, nationalId='', userRecommendations=[]):
        """
            insert new user in recommendations collection

            Parameters
            ['id', 'fieldOfStudy', 'specialization', 'skills', 'skills level','nationalId', 'userRecommendations'] of new user's content

        """
        doc_data = {
            'fieldOfStudy':fieldOfStudy, 
            'specialization': specialization, 
            'userSkills': [{'skillName': skills[i], 'skillRate':skills_level[i]} for i in range(len(skills))], 
            'nationalId': nationalId,
            'partnerRate': [], 
            'userRecommendations': userRecommendations, 
            }
            
        
        response = self.__collection.insert_one( doc_data )
        print('Inserted Successfully')

    def delete_user(self, nationalId: int):
        """
            delete document in recommendations collection

            Parameters
            id[int] -> id of user that you want to delete

        """
        try:
            response = self.__collection.delete_one( {'nationalId':nationalId} )
            print('Deleted Successfully')
        except Exception as e:
            print(e)

    def Update_Recom_List(self, nationalId:int, IDs_list: list, Scores_list: list):
        """
            insert recommendation list of user

            Parameters
            nationalId -> nationalId of user that you want to update his content
            recom_list [list] -> list of recommended users' IDs list
        """
        response = self.__collection.update_one( {'nationalId': nationalId}, {'$set': {'userRecommendations':[{'nationalId': IDs_list[i], 'score':Scores_list[i]} for i in range(len(IDs_list))]}})

    def update_attr(self, nationalId:int, col_name: str, value):
        """
            update attribute's value of user

            Parameters
            nationalId -> nationalId of user that you want to update his content
            col_name str -> name of attributes you need to update
            value -> the new value
        """
        response = self.__collection.update_one( {'nationalId': nationalId}, {'$set': {col_name:value}})

    def get_all_content_for_available_users(self):
        """
            find all content in recommendations collection

            Return
            IDs, contents -> id and content for all users
        """
        # find all content of users
        users = self.__collection.find({"nationalId": {"$in": self.get_all_available_IDs()}})
        IDs, contents = [], []

        for user in users:
            IDs.append(user['nationalId'])
            contents.append( ' '.join([user['fieldOfStudy'], user['specialization'], ' '.join(content['skillName'] for content in user['userSkills'])]) )
        
        return IDs, contents

    def get_recommedation_list(self, nationalId:str):
        return self.__collection.find_one({"nationalId":nationalId})['userRecommendations']

    def get_all_available_IDs(self):
        # Connect to users collection
        self.__users = self.__db['users']
        users = self.__users.find({"partnerId":None})
        NIDs = []
        for user in users:
            NIDs.append(user['nationalId'])
        return NIDs








d = DB_Recommendations()
# d.delete_user('1')
# d.delete_user('2')

# co0 = ['Computer Science', 'Web Development', ['back end', 'problem solving', 'competitive programming', 'java script', 'node.js', 'c++', 'software architecture', 'Databases'], [3, 4, 4, 3, 3, 2, 2, 4], '1']
# co1 = ['Computer Science', 'Web Development', ['front end', 'problem solving', 'competitive programming', 'design', 'html', 'css', 'java script', 'react.js', 'c++'], [4, 4, 4, 2, 3, 3, 3, 4, 2], '2']
# co2 = ['Computer Science', 'Mobile Application', ['flutter', 'dart', 'OOP', 'Data Structures', 'problem solving', 'software engineering'], [3, 3, 3, 2, 2, 2], '3']
# co3 = ['Computer Science', 'Data Science', ['python', 'problem solving', 'competitive programming', 'machine learning', 'deep learning', 'artificial intelligence', 'SQL', 'Databases'], [5, 3, 3, 3, 1, 2, 3, 3], '123']
# co4 = ['Computer Science', 'Cyber Security', ['python', 'networks', 'information technology', 'operating system', 'Databases'], [5, 3, 3, 3, 3], '4']

# d.update_attr("1","userSkills", [{'skillName': 'python', 'skillRate':5}])
# co5 = ['Computer Science', 'Graphic Designer', ['user interface', 'user experience', 'designer', 'front end', 'figma', 'XD', 'ui/ux', 'html', 'css'], [3, 3, 3, 3, 3, 3, 3, 2, 2], '6']
# co6 = ['Computer Science', 'Data Science', ['data analysis', 'statistical analysis', 'data visualization', 'problem solving', 'sampling', 'machine learning'], [3, 3, 4, 2, 2, 2], '2']

# co = [co0, co1, co2, co3, co4]
# for c in co:
#     d.insert_user(*c)

# d.insert_user(*co0)

# print(d.get_all_content_for_available_users())
# print(d.get_all_available_IDs())
# d.print_all_users()

d.print_all()
# print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
# d.print_all_users()

#### Link: https://sysadmins.co.za/mongodb-cheatsheet-with-pymongo/