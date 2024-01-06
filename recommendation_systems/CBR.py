# importing libraries
import sys
sys.path.append("..")

# customized content analyzer
def cosine_jaccard(u1_c1: dict, u2_c2: dict):
    """
        computing similarity score between user's content and partner's content with customized content analyzer [jaccard_dis(for string) * cosine_sim(for numbers)]

        Parameters
            u1_c1 [dict] -> content_data of the user 
            u2_c2 [dict] -> content_data of the partner

        return similarity_score
    """
    # jaccard_dis = len(intersection words) / len(union words)
    len_intersec = 0
    len_union = 0
    # cosine_sim = sum_of_dot_product(X1.X2) / SQRT(SUM_X1^2 * SUM_X2^2)
    sum_of_dot_product = 0
    sum_of_r1 = 0
    sum_of_r2 = 0

    for sk1, r1 in u1_c1.items():
        try:
            # intersection part [value in u1_c1 and u2_c2]
            r2 = u2_c2[sk1]
            len_intersec += 1
            len_union += 1
            sum_of_dot_product += r1*r2
            sum_of_r1 += r1*r1
            sum_of_r2 += r2*r2
        except:
            len_union += 1
    len_union += len(set(u2_c2.keys()) - set(u1_c1.keys()))

    jaccard_dis = len_intersec/len_union # cateigorcal dimension
    cosine_similarity = sum_of_dot_product/(sum_of_r1*sum_of_r2)**0.5 # numerical dimension

    return jaccard_dis * cosine_similarity

# get content-based recommender recommendations -- O(n_users * m_skills)
def get_recomendation_CBR(content_data:dict, nationalId: str, n_of_recomendation:int):
    """
        recommend partners by computing similarity scores & get the best n_of_recomendation

        Parameters
            content_data[dict] -> content_data of all users {Nid : content}
            nationalId[str] -> nationalId of existing user to get content and compute similarity scores to users_content
            n_of_recomendation[int] -> number of recommendation partners

        return IDs_score[dict] -> CBR Result
    """
    # get content of the user
    u1_c1 = content_data[nationalId]
    IDs_scores = {}

    # get scores between user and all partners
    for nid in content_data.keys():
        u2_c2 = content_data[nid]
        IDs_scores[nid] = cosine_jaccard(u1_c1, u2_c2) # score

    # get the best n_of_recomendation
    IDs_scores = dict(sorted(IDs_scores.items(), key=lambda u_score: u_score[1], reverse=True)[1:n_of_recomendation+1])
    return IDs_scores