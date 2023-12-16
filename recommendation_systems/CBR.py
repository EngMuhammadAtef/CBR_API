# importing libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel # cosine_similarity [same but slower method] <TfidfVectorizer returns normalized victors> 
from crud_operations import crud
import sys
sys.path.append("..") # Adds higher directory to python modules path.

def get_recomendation_CBR(db, nationalId: str, n_of_recomendation):
    """
        recommend partners by computing similarity scores between user's content and partner's content

        Parameters
            db -> DataBase
            nationalId [str] -> nationalId of existing user to get content and compute similarity scores to users_content

        return users_nationalIDs, users_scores           [first n user' IDs and scores that similar to me]
    """

    # get all national IDs & content of all available users
    NIDs, bag_of_content = crud.get_all_content(db)

    # compute similarity between new content and users_content
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(bag_of_content)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim = {id:cos for id, cos in zip(NIDs, cosine_sim)}

    # Get the pairwsie similarity scores of all users_content with that content
    sim_scores = list(zip(NIDs, cosine_sim[nationalId]))

    # Sort first n_of_recomendation based on similarity scores [DESC]
    for i in range(n_of_recomendation+1):
        for j in range(len(sim_scores)-1, i, -1):
            if sim_scores[j][1]>sim_scores[j-1][1]:
                sim_scores[j], sim_scores[j-1] = sim_scores[j-1], sim_scores[j]
    
    # Get scores of the most similar content
    sim_scores = [ elm for elm in sim_scores[:n_of_recomendation+1] if elm[0] != nationalId ]

    # Get the users indices and scores
    users_nationalIDs = [a[0] for a in sim_scores]
    users_scores = [a[1] for a in sim_scores]

    # Return first n users idx and scores
    return users_nationalIDs, users_scores