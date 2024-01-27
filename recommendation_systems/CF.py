# importing libraries
from recommendation_systems.Matrix_Factors import MFmodel
import sys
sys.path.append("..")

def get_recomendation_cf(nationalId: str, NIDs: list, n_of_recomendation: int):
    """
        recommend partners by collaborative-filtering model

        Parameters
            nationalId [str] -> nationalId of existing user 
            NIDs [list] -> nationalId of partners to get predicted ratings
            n_of_recomendation[int] -> number of recommendation partners

        return users_ratings[dict] -> users_nationalIDs, predicted_ratings
    """
    # get predicted ratings between user and partners
    users_ratings = {}
    for partner_id in NIDs:
        users_ratings[partner_id] = MFmodel.predict_rating(nationalId, partner_id)

    # get the best n_of_recomendation
    users_ratings = dict(sorted(users_ratings.items(), key=lambda u_rating: u_rating[1], reverse=True)[:n_of_recomendation])
    return users_ratings
