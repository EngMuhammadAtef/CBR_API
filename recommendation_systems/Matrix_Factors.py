import numpy as np
import sys
sys.path.append("..")

class MatrixFactorization:
    def __init__(self, num_factors=5, learning_rate=0.01, lambda_=0.1):
        # Initialize user and partner matrices
        self.user_embeddings, self.partner_embeddings, self.embedd_IDs = self.load_embeddings()
        self.num_users = len(self.user_embeddings)
        self.num_factors = num_factors
        self.learning_rate = learning_rate
        self.lambda_ = lambda_
        self.sum_of_squered_error = 0 # rmse = np.root( np.sum( error*2 ) / N_err )
        self.n_of_error = 0

    def save_embeddings(self):
        np.save("recommendation_systems/model/user_embeddings.npy", self.user_embeddings)
        np.save("recommendation_systems/model/partner_embeddings.npy", self.partner_embeddings)
        np.save("recommendation_systems/model/embedd_IDs.npy", self.embedd_IDs)

    def load_embeddings(self):
        """
        load user_embeddings partner_embeddings embedd_IDs
        """
        try:
            return np.load("recommendation_systems/model/user_embeddings.npy"), np.load("recommendation_systems/model/partner_embeddings.npy"), np.load("recommendation_systems/model/embedd_IDs.npy", allow_pickle=True)
        except:
            return np.random.random((0, 0)), np.random.random((0, 0)), np.array([{}])

    def add_new_embedding(self): 
        # add new user-partner reprensentation for new user
        new_embeddings = np.random.random((1, self.num_factors))
        self.user_embeddings = np.vstack((self.user_embeddings, new_embeddings)) if self.num_users else new_embeddings
        self.partner_embeddings = np.hstack((self.partner_embeddings, new_embeddings.T)) if self.num_users else new_embeddings.T
        self.num_users += 1

    def get_idxEmbed(self, user_id):
        try: # if already user has embeddings representaion
            return self.embedd_IDs[0][user_id]
        except: # if not 
            self.embedd_IDs[0][user_id] = self.num_users
            self.add_new_embedding()
            return self.embedd_IDs[0][user_id]

    def predict(self, user_embad_idx, partner_embad_idx):
        pred_rating = np.dot(self.user_embeddings[user_embad_idx, :], self.partner_embeddings[:, partner_embad_idx])
        return self.scale_ratings(pred_rating)

    def update_model_with_new_rating(self, user_id:str, partner_id:str, rating:int):
        # Update the user and partner matrices with the new rating
        user_embad_idx = self.get_idxEmbed(user_id)
        partner_embad_idx = self.get_idxEmbed(partner_id)

        # Update user and partner matrices using SGD(the incremental update)
        rating_pred = self.predict(user_embad_idx, partner_embad_idx)
        error = rating - rating_pred
        self.user_embeddings[user_embad_idx, :] += self.learning_rate * (2 * error * self.partner_embeddings[:, partner_embad_idx] - self.lambda_ * self.user_embeddings[user_embad_idx, :])
        self.partner_embeddings[:, partner_embad_idx] += self.learning_rate * (2 * error * self.user_embeddings[user_embad_idx, :] - self.lambda_ * self.partner_embeddings[:, partner_embad_idx])
        
        # mentoring performance
        self.sum_of_squered_error += (error**2)
        self.n_of_error += 1

    def predict_rating(self, user_id:str, partner_id:str):
        # Update the user and partner matrices with the new rating
        user_embad_idx = self.get_idxEmbed(user_id)
        partner_embad_idx = self.get_idxEmbed(partner_id)
        pred_rating = self.predict(user_embad_idx, partner_embad_idx)
        return pred_rating
    
    def predict_for_all(self):
        pred_rating = np.dot(self.user_embeddings, self.partner_embeddings)
        return self.scale_ratings(pred_rating)

    def scale_ratings(self, ratings, min_rate=1, max_rate=5):
        return 1/(1+np.e**-ratings)*(max_rate-min_rate)+min_rate

    def rmse(self):
        return (self.sum_of_squered_error / self.n_of_error) ** 0.5

# Instantiate the MatrixFactorization model
MFmodel = MatrixFactorization()
