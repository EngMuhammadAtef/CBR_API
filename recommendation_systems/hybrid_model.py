from recommendation_systems.CBR import get_recomendation_CBR
from recommendation_systems.NCF import get_recomendation_ncf
from crud_operations import crud
import sys
sys.path.append("..") # Adds higher directory to python modules path.

def get_recomendation(db, nationalId: str):
    # get the First 20 Best Partner by content-based-recommender system
    cbr_users, cbr_scores = get_recomendation_CBR(db, nationalId, 20)

    # get the First 10 Best Partner by hybrid-recommender system
    users_nationalIDs, predicted_ratings = get_recomendation_ncf(nationalId, cbr_users, 10)

    # save recommendations in database
    crud.Update_Recom_List(db, nationalId, users_nationalIDs, predicted_ratings)

    # Return first n users idx and predicted_ratings
    return users_nationalIDs, predicted_ratings

def Update_All_Recommendations(db):
    # get all nationalIds of users
    NIDs, _ = crud.get_all_content(db)

    # get recomendation for each user and update in db
    for nationalId in NIDs:
        get_recomendation(db, nationalId)
    
    print("Updated All Recommendation lists Successfully")