# importing libraries
import tensorflow as tf
import sys
sys.path.append("..")

def get_recomendation_ncf(nationalId: str, NIDs: list, n_of_recomendation: int):
    """
        recommend partners by neural-collaborative-filtering model through two-towers architecture

        Parameters
            nationalId [str] -> nationalId of existing user 
            NIDs: list -> nationalId of partners to get predicted ratings
            n_of_recomendation: int -> number of recomendation list

        return users_nationalIDs, predicted_ratings
    """

    # load Neural-Collaborative-Filtering model
    ncf_model = tf.saved_model.load("./recommendation_systems/model")

    # predicted ratings from model
    predicted_ratings = [*ncf_model({"nationalId": [nationalId]*len(NIDs), "partnerId":  NIDs}).numpy().reshape(len(NIDs),)]
    
    # merge IDs with Ratings
    users_ratings = list(zip(NIDs, predicted_ratings))

    # Sort first n users based on ratings [DESC]
    for i in range(n_of_recomendation):
        for j in range(len(users_ratings)-1, i, -1):
            if users_ratings[j][1]>users_ratings[j-1][1]:
                users_ratings[j], users_ratings[j-1] = users_ratings[j-1], users_ratings[j]
    
    users_ratings = users_ratings[:n_of_recomendation]

    # Get the users indices and scores
    IDs_ratings = {a[0]:a[1]/5 for a in users_ratings}

    # Return n users idx and scores
    return IDs_ratings