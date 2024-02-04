from recommendation_systems.CBR import get_recomendation_CBR
from recommendation_systems.CF import get_recomendation_cf
from recommendation_systems.Matrix_Factors import MFmodel
import sys
sys.path.append("..")

def get_recomendation(nationalId: str, content_data:dict, n_of_recomendation:int = 10):
    """
        recommend partners by hybrid model through merged-two-models
          [content-based recommender - collaborative filtering]

        Parameters
            nationalId [str] -> nationalId of existing user to get recomendations
            content_data [dict] -> content_data of all users {Nid : content}
            n_of_recomendation[int] -> number of recommendation partners

        return final_recommendations[tuple] -> ID, Content_score, predicted_rating
    """

    # get the First N Best Partner by content-based-recommender system
    CBR_IDs_scores = get_recomendation_CBR(nationalId, content_data, n_of_recomendation*2)

    # get IDs from content-based recommendations to fit to collaborative filtering
    CF_IDs_ratings = get_recomendation_cf(nationalId, list(CBR_IDs_scores.keys()), n_of_recomendation) 

    # combine CBR_score and NCF_rate to get IDs & score & rate
    final_recommendations = ((ID, round(CBR_IDs_scores[ID], 2), round(rate, 1)) for ID, rate in CF_IDs_ratings.items())
    final_recommendations = sorted(final_recommendations, key=lambda recom: (recom[1]*0.8 + recom[2]/5*0.2), reverse=True) # weighted average 80% of CBR_score and 20% of normalized pred_rate
    
    # Return the best n_of_recomendation partners
    return final_recommendations

def Update_All_Embeddings(all_ratings_data: tuple):
    """
        improve model performance with SGD for all ratings and continoues feedback rating improvement (cron-job for a specific period)
    """

    # improve model performance with SGD for all ratings
    for user_id, partner_id, rating in all_ratings_data:
        MFmodel.update_model_with_new_rating(str(user_id), str(partner_id), rating)

    MFmodel.save_embeddings()
    
    print("Updated CF Model & All Embeddings for all users Successfully")
    print("NEW RMSE for the model", MFmodel.rmse())