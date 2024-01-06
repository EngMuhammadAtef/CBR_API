# importing libraries
import tensorflow as tf
import sys
sys.path.append("..")

# load Neural-Collaborative-Filtering model
ncf_model = tf.saved_model.load("./recommendation_systems/model")

def get_recomendation_ncf(nationalId: str, NIDs: list, n_of_recomendation: int):
    """
        recommend partners by neural-collaborative-filtering model through two-towers architecture

        Parameters
            nationalId [str] -> nationalId of existing user 
            NIDs [list] -> nationalId of partners to get predicted ratings
            n_of_recomendation[int] -> number of recommendation partners

        return users_nationalIDs, predicted_ratings
    """
    # predicted ratings from model
    predicted_ratings = [*ncf_model({"nationalId": [nationalId]*len(NIDs), "partnerId":  NIDs}).numpy().reshape(len(NIDs),)]
    
    # merge IDs and Ratings and get the best n_of_recomendation partners
    users_ratings = list(zip(NIDs, predicted_ratings))
    users_ratings = dict(sorted(users_ratings, key=lambda u_rate: u_rate[1], reverse=True)[:n_of_recomendation])

    # Return n users idx and scores
    return users_ratings