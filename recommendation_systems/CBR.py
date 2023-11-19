# importing libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel # cosine_similarity [same but slower method] # k(x,y) = xT.y <TfidfVectorizer returns normalized victors> 
from crud_operations import crud
import sys
sys.path.append("..") # Adds higher directory to python modules path.

def get_recomendation(db, nationalId: str):
    """
        recommend me users with computing similarity scores between my content and other users' content

        Parameters
        db -> DataBase
        nationalId [str] -> nationalId of existing user to get content and compute similarity scores to users_content

        NIDs, bag_of_content -> getting IDs and all content of users

        return users_nationalIDs, users_scores           [first 10 user' IDs and scores that similar to me]
    """

    # get all national IDs & content of all available users
    NIDs, bag_of_content = crud.get_all_content_for_available_users(db)

    # compute similarity between new content and users_content
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(bag_of_content)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim = {id:cos for id, cos in zip(NIDs, cosine_sim)}

    # Get the pairwsie similarity scores of all users_content with that content
    sim_scores = list(zip(NIDs, cosine_sim[nationalId])) # [[1, 0.44], [2, 0.52], ...]

    # Sort first 10 based on similarity scores [DESC]
    for i in range(11): # number of recommendation users[10]
        for j in range(len(sim_scores)-1, i, -1):
            if sim_scores[j][1]>sim_scores[j-1][1]:
                sim_scores[j], sim_scores[j-1] = sim_scores[j-1], sim_scores[j]
    
    # Get the scores of the 10 most similar content
    sim_scores = [ elm for elm in sim_scores if elm[0] != nationalId ]

    # Get the users indices and scores
    users_nationalIDs = [a[0] for a in sim_scores]
    users_scores = [round(a[1]*100, 1) for a in sim_scores]
    
    # save recommendations in database
    crud.Update_Recom_List(db, nationalId, users_nationalIDs, users_scores)

    # Return first 10 users idx and scores
    return users_nationalIDs, users_scores

def Update_All_Recommendations(db):
    """
        Update All Recommendation lists for all users with computing similarity scores
        
        Parameters
        db -> DataBase
    """

    # get all national IDs & content of all available users
    NIDs, bag_of_content = crud.get_all_content_for_available_users(db)

    # compute similarity between new content and users_content
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(bag_of_content)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim = {id:cos for id, cos in zip(NIDs, cosine_sim)}

    # update for every user
    for nationalId in NIDs:
        # Get the pairwsie similarity scores of all users_content with that content
        sim_scores = list(zip(NIDs, cosine_sim[nationalId])) # [[1, 0.44], [2, 0.52], ...]

        # Sort first 10 based on similarity scores [DESC]
        for i in range(11): # number of recommendation users[10]
            for j in range(len(sim_scores)-1, i, -1):
                if sim_scores[j][1]>sim_scores[j-1][1]:
                    sim_scores[j], sim_scores[j-1] = sim_scores[j-1], sim_scores[j]
        
        # Get the scores of the 10 most similar content
        sim_scores = [ elm for elm in sim_scores if elm[0] != nationalId ]

        # Get the users indices and scores
        users_nationalIDs = [a[0] for a in sim_scores]
        users_scores = [round(a[1]*100, 1) for a in sim_scores]

        # save user in database
        crud.Update_Recom_List(db, nationalId, users_nationalIDs, users_scores)

    print("Updated All Recommendation lists Successfully")
