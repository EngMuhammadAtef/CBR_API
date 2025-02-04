# importing libraries
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import sys
sys.path.append("..")
nltk.download('punkt')
nltk.download('wordnet')

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

# preprocessing step
def clean_text(user_cont: dict):
    """
    preprocessing step (Remove special characters - lowercase - Tokenization - Lemmatization - )

    Parameters
        user_cont[dict] -> content data of the user

    return content_data[dict] after preprocessing
    """
    new_user_cont = {}
    for text, rate in user_cont.items():
        # Remove special characters and punctuation
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Convert text to lowercase
        text = text.lower()
        # Tokenization
        tokens = word_tokenize(text)
        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        # Join tokens back into text
        clean_text = ' '.join(tokens)
        new_user_cont[clean_text] = rate
    return new_user_cont

# get content-based recommender recommendations -- O(n_users * m_skills)
def get_recomendation_CBR(nationalId: str, content_data:dict, n_of_recomendation:int):
    """
        recommend partners by computing similarity scores & get the best n_of_recomendation

        Parameters
            nationalId[str] -> nationalId of existing user to get content and compute similarity scores to users_content
            content_data[dict] -> content_data of all users {Nid : content}
            n_of_recomendation[int] -> number of recommendation partners

        return IDs_score[dict] -> CBR Result
    """
    # get content of the user
    u1_c1 = clean_text(content_data[nationalId])
    IDs_scores = {}

    # get scores between user and all partners
    for nid in content_data.keys():
        u2_c2 = clean_text(content_data[nid])
        IDs_scores[nid] = cosine_jaccard(u1_c1, u2_c2) # score

    # get the best n_of_recomendation
    IDs_scores = dict(sorted(IDs_scores.items(), key=lambda u_score: u_score[1], reverse=True)[1:n_of_recomendation+1])
    return IDs_scores
