from recommendation_systems.CBR import get_recomendation_CBR
from recommendation_systems.NCF import get_recomendation_ncf
from crud_operations import crud
import sys
sys.path.append("..") # Adds higher directory to python modules path.

def get_recomendation(db, nationalId: str):
    """
        recommend partners by hybrid model through merged-two-models [content-based recommender - collaborative filtering]

        Parameters
            db [con obj] -> DataBase
            nationalId [str] -> nationalId of existing user to get recomendations

        return first n users IDs(keys) and scores(values) -> final_IDs_scores[dict]
    """

    # get the First 20 Best Partner by content-based-recommender system
    IDs_scores = get_recomendation_CBR(db, nationalId, 20)

    # get IDs from content-based recommendations to fit to collaborative filtering [hybrid-recommender system]
    IDs_ratings = get_recomendation_ncf(nationalId, list(IDs_scores.keys()), 10) 

    # combine CBR_score and NCF_rate to get IDs and average scores
    final_IDs_scores = {ID:round((rate+IDs_scores[ID])/2, 3) for ID, rate in IDs_ratings.items()}
    final_IDs_scores = dict(sorted(final_IDs_scores.items(), key=lambda item: item[1], reverse=True))
    
    # save recommendations in database
    crud.Update_Recom_List(db, nationalId, final_IDs_scores)

    # Return first n users IDs and scores
    return final_IDs_scores

def Update_All_Recommendations(db):
    # get all nationalIds of users
    NIDs, _ = crud.get_all_content(db)

    # get recomendation for each user and update in db
    for nationalId in NIDs:
        get_recomendation(db, nationalId)
    
    print("Updated All Recommendation lists Successfully")