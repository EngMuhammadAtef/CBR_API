def get_recomendation(nationalId: str):
    """
        recommend me users with computing similarity scores between my content and other users' content

        Parameters
        nationalId [str] -> nationalId of existing user to get content and compute similarity scores to users_content

        return users_nationalIDs, users_scores           [first 10 user' IDs and scores that similar to me]
    """

    # importing libraries
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from DB import DB_Recommendations

    # connect to database and access recommendations collection
    rec_db = DB_Recommendations()

    # get all national IDs & content of all users
    NIDs, bag_of_content = rec_db.get_all_content()

    # compute similarity between new content and users_content
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(bag_of_content)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    cosine_sim = {id:cos for id, cos in zip(NIDs, cosine_sim)}

    # Get the pairwsie similarity scores of all users_content with that content
    sim_scores = list(zip(NIDs, cosine_sim[nationalId])) # [[1, 0.44], [2, 0.52], ...]

    # Sort all the users_content based on the similarity scores DESC
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) # [[2, 0.52], [1, 0.44], ...]
    
    # Get the scores of the 5 most similar content
    sim_scores = sim_scores[1:11]

    # Get the users indices
    users_nationalIDs = [i[0] for i in sim_scores]
    users_scores = [round(i[1]*100, 1) for i in sim_scores]

    # save user in database
    rec_db.insert_RecoList(nationalId, users_nationalIDs, users_scores)

    # Return first 10 users idx and scores
    return users_nationalIDs, users_scores

def Update_All_Recommendations():
    """
        Update All Recommendation lists for all users with computing similarity scores
    """

    # importing libraries
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from DB import DB_Recommendations

    # connect to database and access recommendations collection
    rec_db = DB_Recommendations()

    # get all national IDs & content of all users
    NIDs, bag_of_content = rec_db.get_all_content()

    # compute similarity between new content and users_content
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(bag_of_content)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    cosine_sim = {id:cos for id, cos in zip(NIDs, cosine_sim)}

    # update for every user
    for nationalId in NIDs:
        # Get the pairwsie similarity scores of all users_content with that content
        sim_scores = list(zip(NIDs, cosine_sim[nationalId])) # [[1, 0.44], [2, 0.52], ...]

        # Sort all the users_content based on the similarity scores DESC
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) # [[2, 0.52], [1, 0.44], ...]
        
        # Get the scores of the 5 most similar content
        sim_scores = sim_scores[1:11]

        # Get the users indices
        users_nationalIDs = [i[0] for i in sim_scores]
        users_scores = [round(i[1]*100, 1) for i in sim_scores]

        # save user in database
        rec_db.insert_RecoList(nationalId, users_nationalIDs, users_scores)

    print("Updated All Recommendation lists Successfully")