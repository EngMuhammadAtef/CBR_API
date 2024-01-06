from recommendation_systems.CBR import get_recomendation_CBR
from recommendation_systems.NCF import get_recomendation_ncf
import sys
sys.path.append("..")

def get_recomendation(content_data:dict, nationalId: str, n_of_recomendation:int = 10):
    """
        recommend partners by hybrid model through merged-two-models [content-based recommender - collaborative filtering]

        Parameters
            content_data [dict] -> content_data of all users {Nid : content}
            nationalId [str] -> nationalId of existing user to get recomendations
            n_of_recomendation[int] -> number of recommendation partners

        return final_recommendations[dict] -> the best n_of_recomendation partners IDs(keys) and scores(values)
    """

    # get the First 20 Best Partner by content-based-recommender system
    CBR_IDs_scores = get_recomendation_CBR(content_data, nationalId, n_of_recomendation*2)

    # get IDs from content-based recommendations to fit to collaborative filtering [hybrid-recommender system]
    NCF_IDs_ratings = get_recomendation_ncf(nationalId, list(CBR_IDs_scores.keys()), n_of_recomendation) 

    # combine CBR_score and NCF_rate to get IDs and scores
    final_recommendations = {ID:round((rate/5+CBR_IDs_scores[ID]), 2) if round((rate/5+CBR_IDs_scores[ID]), 2)<1 else 1 for ID, rate in NCF_IDs_ratings.items()}
    final_recommendations = dict(sorted(final_recommendations.items(), key=lambda item: item[1], reverse=True))
    
    # Return the best n_of_recomendation partners
    return final_recommendations

def Update_All_Recommendations(content_data: dict):
    """
        recommend partners for all users by hybrid model (cron-job for a specific period)
    """
    # get all nationalIds of users
    NIDs = content_data.keys()

    # get recomendation for each user and update in db
    for nationalId in NIDs:
        get_recomendation(content_data, nationalId)
    
    print("Updated All Recommendation lists Successfully")