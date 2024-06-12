# GRADAUTION-PROJECT
1. **Introduction**

Recommender systems (RS) are a cornerstone of many online experiences today. By leveraging vast amounts of user data, these AI-powered applications suggest products, services, or content tailored to individual preferences. This section explores how recommender systems work and introduces the concept of hybrid recommender systems, which combine multiple recommendation techniques for improved performance.

1.1 **The Power of Recommendations**

Recommendation systems play a crucial role in enhancing user experience and satisfaction. They function by filtering and prioritizing information, making it more relevant to individual users. Through sophisticated algorithms that analyze user behavior, preferences, and interactions, recommender systems learn user habits and predict what they might be interested in next.

These algorithms rely on various data sources, including:

**Explicit Inputs:** User ratings, reviews, and feedback.

**Implicit Inputs:** Browsing history, click patterns, and time spent on specific activities.

The core components of a recommendation system typically include:

- **Data Collection:** Gathering data from various sources, including user interactions, preferences, demographics, and feedback.
- **Data Processing:** Cleaning and organizing the collected data to make it suitable for analysis. This step often involves handling missing values, normalizing data formats, and integrating data from different sources.
- **Modeling:** Applying machine learning algorithms to the processed data to create predictive models. Common techniques include collaborative filtering, content-based filtering, and hybrid methods.
- **Prediction and Recommendation Generation:** Using the models to generate personalized recommendations for each user. This involves ranking items based on predicted relevance and presenting them in an intuitive and engaging manner.
- **Evaluation and Feedback:** Continuously assessing the performance of the recommendation system using metrics like precision, recall, and user satisfaction. Feedback loops are established to refine the models and improve recommendations over time.

****1.2 Types of Recommendation Systems****

While there are a vast number of recommender algorithms and techniques, most fall into these broad categories:

![1-s2 0-S1110866515000341-gr2](https://github.com/EngMuhammadAtef/GRADAUTION-PROJECT/assets/96551959/2968642b-6134-4996-bed5-21ee67b1646d)

- **Content-Based Filtering:** Recommends items similar to those a user has interacted with in the past. Here, items are categorized, and users with similar preferences are matched.
- **Collaborative Filtering:** Recommends items based on the preferences of similar users. This approach analyzes user interactions and identifies users with similar tastes.

And we can combine these algorithms in ****Hybrid Recommender System.****

****1.3 Hybrid Recommendation System****

**Hybrid recommender systems** combine content-based and collaborative filtering approaches, leveraging the strengths of each. This strategy addresses limitations inherent in individual techniques, such as the "cold start problem" where new users or items lack sufficient data for accurate recommendations. Many popular recommendation systems, like those used by Google and YouTube, utilize hybrid filtering for improved performance.

Our proposed system delves into a user-recommender interaction based hybrid recommender system. This framework considers user-recommender behavior and incorporates a random algorithm to address the cold-start problem. As user data accumulates, the system transitions to an incremental recommendation approach, where the sequence of user choices influences subsequent recommendations, creating an active learning scenario.

Several studies comparing **the performance** of hybrid filtering systems with the collaborative and content systems alone have shown that hybrid systems have **better accuracy**.Combining both algorithms can remove multiple issues like the cold-start problem and help gather data quickly.

![5-Figure5-1](https://github.com/EngMuhammadAtef/GRADAUTION-PROJECT/assets/96551959/d8550a1c-55b8-4650-953d-a94957487f41)

**In this section,** we propose a hybrid recommender system based on user-recommender interaction. The interaction provides a framework for user-recommender behavior and recommender algorithms. We employ the random algorithm to deal with cold-start problem in the face of data sparsity.

The hybrid algorithm is applied to incremental recommendation when the data reaches a certain degree. The sequence of the user’s choice affects subsequent recommendation in the process of user-recommender interaction. Consequently, the interaction forms an active learning scenario.

2. **Why **Hybrid Recommender System**?**

**2.1 Content-based filtering Drawbacks**:

**Problem 1: over-specialization issue**

The inability of the program to suggest to the user objects that are distinct from those he has already observed is only one aspect of the over-specialization problem but also that it must not recommend items that are too close to those he has enjoyed in the past. As a result, certain recommendation algorithms exclude not just things that differ from the user profile, but also those that are highly similar to those already followed by the present user.The diversity of the recommendations is a criterion for evaluating the quality of the recommendations.The user must receive diversified and not homogeneous relevant recommendations.For example, it is not wise to recommend all of author’s books to a user who has enjoyed one of his books.

**Problem 2: serendipity issue**

It is a technique for increasing the variety of suggestions,

Serendipitous recommendations are suggestions that may interest users, even if they aren't directly related to their previous behavior or preferences by introducing unexpected recommendations.

**Problem 3: limited content issue**

Content-based approaches restrict the number and type of common qualities

they may offer manually or automatically with objects. Expertise in the domain and taxonomies relevant to the field are also essential, could not provide appropriate suggestions if the examined content lacks sufficient information.

**Problem 4: Synonym issue**

Synonyms are two or more words expressing the same thing or concept.

However, recommendation algorithms are unable to distinguish between these terms. A memory-based CF method, for example, determines between ”comedy movie” and ”comedy film”. Synonym overuse degrades the quality of a recommender system.

**2.2 Collaborative filtering Drawbacks**:

**Problem 1: Cold-Start Problem and Latency**

It occurs when a new user (or even a new item) enters the system. That user’s lack of item-interaction history prevents the system from being able to evaluate the new user’s similarity or association with existing users. By contrast, content-based systems are more adept at handling new items, although they also struggle with recommendations for new users.

it concerns the issue that the system cannot draw any inferences for users or items about which it has not yet gathered sufficient information.

**Problem 2: Data Sparseness**

recommender systems typically lack data on user preferences for most items in the system. This means that most of the system’s feature space is empty, a condition called data sparsity. As data sparsity increases, vector points become so dissimilar that predictive models become less effective at identifying explanatory patterns. This is a primary reason why matrix factorization and related latent factor methods such as singular value decomposition(SVD) is popular in collaborative filtering, as it alleviates data sparsity by reducing features. Other methods implemented for resolving this issue may also involve users themselves assessing and providing information on their own interests, which the system can then use to filter recommendations.

3. **Model Design and Architecture**

In this section, we will describe the design of the study-partner recommendation system. We will begin with the high level components of the network and explain how and why they have been assembled together in a particular way, with implications for future model design, then characterize the low level operators and primitives that make up the model, with implications for future hardware and system design.

**3.1 Components of Content-Based Recommender**

The high-level components of the content-based recommender can be more easily understood by reviewing early models. We will avoid the full scientific literature review and focus instead on the three techniques used in early models that can be interpreted as salient high-level components of the CBR.

**3.1.1 Customized Content Analyzer**

This is the most important part of the content-based component, it is a component responsible for analyzing the characteristics and attributes of content users to compute similarity score between user's content and partner's content with customized content analyzer.

**Consists of two-merged formulas**

\- **Jaccard Similarity Index**: It’s a measure of similarity for the two sets of data

****J(X,Y) = |X∩Y| / |X∪Y| For Skill Names \[Strings\]****

\- **Cosine Similarity**: It is measured by the cosine of the angle between two vectors and determines whether two vectors are pointing in roughly the same direction.

****C(X, Y) = (X.Y) / (||X||\*||Y||) For Skill Rates \[Int/Float\]****

**Merged Formula (weighted average)** = Jaccard Score \* Cosine Score

**For Content-Sim Score**

**Note:** we used a weighted average not a simple average for two reasons:

1. The cosine-similarity score is calculated based on rates of the common skills between the user and partner as a factor of change levels between the user and partner on a specific skill e.g. user1 rates skill1 5 and user2 rates skill1 1, there is a difference factor.
2. If there is no common skill between user and partner, the Jaccard score will be zero, and the Cosine score will be one. So if we calculate simple-avg,

the similarity score between user and partner is 50%, which makes no sense. On the contrary, the weighted average is 0\*1 = 0%.

Before the Content-Analyzer step, the text goes to the pre-processed step.

**3.1.2 Content Cleaner (NLP Component)**

The Content Cleaner typically employs various techniques in natural language processing (NLP) such as

\- **Clean**: Remove special characters and punctuation

\- **Lowercase**: Converting all characters to lowercase

\- **Tokenization**: is the process of breaking down text into smaller units, typically words or subwords, called tokens, e.g. “Going to New York!” to \[“Going”, “to”, “New York”, “!”\]

**Note: (Not just split text but split with some knowledge)**

\- **Lemmatization**: Reducing words to their base or root form, called the lemma.

e.g. the lemma of "running" is "run", "mice" is "mouse".

**3.1.3 Filtering Component**

This component is responsible for applying the content cleaner function to the user text and the partner text to get the content-based recommender scores for all partners for a specific user and sorting for getting the best K partners.

**3.2 Components of Neural Collaborative Filtering**

The high-level components of the neural collaborative filtering recommender can be more easily understood by reviewing early models. We will focus on the four techniques used in early models that can be interpreted as salient high-level components of the NCF.

**3.2.1 Embeddings**

An embedding is a numerical representation of a piece of information, for example, text, documents, images, audio, etc. The representation captures the semantic meaning of what is being embedded, making it robust for many recommendation systems.

In order to handle categorical data, embeddings map each category to a dense representation in an abstract space, The values of the embeddings are learnable with a machine learning model.

NCF will use embedding tables to map user and partner features to dense representations, according to the history of all user ratings, so we represent each user with a vector \[list\] in the user matrix (user embeddings) and each partner with a vector \[list\] in the partner matrix (partner embeddings).

To predict the rating of the user i-th to the partner j-th, you calculate the dot product of the user vector(v) and the partner vector(w).

**ȓ**ij = **v**i **.** **w**j

This is called **matrix factorization**.

**3.2.2 Matrix Factorization**

The idea behind matrix factorization is to represent users and partners in a lower dimensional latent space. Since the initial work by Funk in 2006 a multitude of matrix factorization approaches have been proposed for recommender systems.

Recall that in the typical formulation of the recommendation problem, we are given a set ‘R’ of users that have rated some partners. We would like to represent partners by a matrix ‘W’ and users by a matrix ‘V’ and multiply ‘V’ by ‘W’ to find all the predicted ratings.

**Note:** that W and V may be interpreted as two embedding tables, where each row represents a user/partner in a latent factor space. The dot product of these embedding vectors yields a meaningful prediction of the subsequent rating.

The matrix factorization approach solves this problem by minimizing

min || **R** - **V.W** ||²

\[**R** actual rates matrix, **V** user embeddings matrix, **W** partner embeddings matrix\]

To do this task we use stochastic gradient descent.

**3.2.3 Stochastic Gradient Descent (SGD)**

SGD is an iterative method for getting the learnable embeddings of the users and the partners by optimizing an objective function with suitable smoothness properties (e.g. differentiable or sub-differentiable). It can be regarded as a stochastic approximation of gradient descent optimization.

**Reason:** SGD not Gradient Descent because we get data iterative on real-time.

**Goal:** extract and optimize user and partner embeddings to predict ratings.

**How:** minimizing this function min || **Σ** **r**ij - (**v**i **. w**j) ||² when each user rates his partner.

**v**i := **v**i - **α** \* (**2** \* (**r**ij - (**v**i **. w**j)) \* **w**j) \[**r** is the actual rating for user i to partner j\]

**w**j := **w**i - **α** \* (**2** \* (**r**ij - (**v**i **. w**j)) \* **v**j) \[**α** is the learning rate of gradient\]

These are the two-optimized functions to get the learnable embeddings for predicting the ratings by calculating the dot product between **v**i and **w**j. **ȓ**ij = **v**i **.** **w**j

**Note**: We try to know the taste of the user **i** and the opinion of the user **i** in the partner **j**, Mathematically, the user vector was treated as parameters one time, and the partner vector was treated as parameters another time.

**Overfitting Problem:**

SGD works but is very noisy. The term "stochastic" indicates that if one example comprising each batch is chosen at random, it's prone to a problem called overfitting, where the model performs well on the training data but poorly on unseen data. **Regularization** helps combat this issue through improved generalization.

And the full functions will be:

**v**i := **v**i - **α** \* (**2** \* (**r**ij - (**v**i **. w**j)) \* **w**j) - **λ** \* **V**i \[**λ** is the regularizer term\]

**w**j := **w**i - **α** \* (**2** \* (**r**ij - (**v**i **. w**j)) \* **v**j) - **λ** \* **w**i \[**λ** is the regularizer term\]

After all processes, we have the embeddings for each user and partner to treat with.

When the future partner has the learned embedding and the user has not rated him before, the model can predict the rating according to the user’s taste.

**3.2.4 Filtering Component**

This component is responsible for applying the matrix factorization model to the user embeddings and the partner embeddings to get the collaborative-filtering recommender scores for all partners for a specific user and sorting for getting the best k users.

4. **Hybrid-Recommender System**

**(Put It All Together)**

Now that we've explored the individual components, here's how they work together in the hybrid recommender system:

1. **Leveraging Content-based Recommendations:** The system first retrieves the top 'K' partner IDs based on content-based recommender scores.
2. **Refining with Collaborative Filtering:** These top 'K' partners are then fed into the NCF component to generate collaborative filtering recommender scores. This step refines the recommendations based on user-partner interaction patterns.
3. **Combining Strengths:** The system combines the content-based recommender scores (CBR scores) and the NCF-predicted ratings using a weighted average. This weighting prioritizes content-based similarity (80%) while incorporating insights from collaborative filtering (20%).
4. **Final Ranking:** The final step involves sorting the list of potential partners based on the combined hybrid recommender scores. This results in a ranked list of the most suitable study partners for a particular user.

This combined approach addresses the limitations of content-based and collaborative filtering techniques individually. The system leverages user profile information for initial filtering and then refines the recommendations using user-partner interaction data, leading to more accurate and diverse study partner suggestions.

To mentor the performance of the actual rates and predicted rates, we used RMSE.

5. **Evaluation and Performance:**

Evaluating the effectiveness of a recommender system is crucial to ensure it delivers valuable recommendations to users. Our system utilizes several key metrics to assess its performance:

**Root Mean Square Error (RMSE):** This metric measures the average difference between predicted and actual user-partner ratings. Lower RMSE values indicate better prediction accuracy by the recommender system.

Utilizing the standard deviation of residuals, RMSE illuminates the average difference between predicted and actual values, offering invaluable insights into model efficacy and performance. By scrutinizing the fidelity of predictions across diverse datasets, RMSE fosters continuous refinement and enhancement of recommendation systems.

**5.1 Refinement Strategies**

Based on the evaluation results, we can employ various strategies to refine the hybrid recommender system:

- **Hyperparameter Tuning:** Adjusting hyperparameters within the content-based recommender and NCF components can improve the accuracy and relevance of recommendations. Examples include modifying the weighting scheme used to combine content-based and collaborative filtering scores or adjusting the learning rate in the SGD optimization algorithm.
- **Incorporating Additional Data Sources:** Integrating user demographics, learning styles, or study goals can further personalize recommendations and enhance the system's ability to identify compatible study partners.
- **Cold-Start Problem Mitigation Strategies:** Techniques like content-based filtering or leveraging social network data can be further explored to improve recommendations for new users with limited interaction data.
- **Online Learning:** The system can be designed to continuously learn from user interactions and update the model over time. This allows the system to adapt to user preferences and evolving study partner characteristics.

By continuously evaluating and refining the system, we can ensure it delivers increasingly relevant and valuable study partner recommendations to users.

6. Conclusion

In this work, we explored the development of a hybrid recommender system for recommending study partners. This system leverages the strengths of both content-based and collaborative filtering techniques to overcome limitations inherent in individual approaches. The content-based recommender utilizes user and partner profile information to identify potential matches based on skill set similarity. The NCF component refines these recommendations using user-partner interaction data, leading to more accurate and diverse suggestions.

The system employs a combination of NLP techniques for text pre-processing and utilizes matrix factorization and stochastic gradient descent for collaborative filtering. The evaluation process involves metrics like RMSE to assess the effectiveness of the recommendations. Additionally, refinement strategies like hyperparameter tuning, data source incorporation, and cold-start mitigation techniques are explored to continuously improve the system's performance.

7. System Architecture

![two tower architecture](https://github.com/EngMuhammadAtef/GRADAUTION-PROJECT/assets/96551959/6ccae4e5-7ca5-4d36-bb39-940ca6397925)

The diagram illustrates the core architecture of our hybrid recommender system, which combines content-based filtering and collaborative filtering techniques. Data flows through several key stages:

- **Data Warehouse:** This component acts as the central repository for user data, including user profiles, skill sets, and potentially explicit ratings or feedback provided by users on past study partners.
- **Data Source and ETL Process:** Data is extracted from various sources, such as user profiles and potentially a MongoDB database containing user interactions. This data is then transformed and loaded into the data warehouse for further processing.
- **Content-Based Filtering Branch:** User and partner profiles are analyzed in this branch to compute a content-based recommender score.
  - **User Content Analyzer:** Extracts and analyzes relevant information from user profiles, potentially including skills and their corresponding ratings.
  - **Partner Content Analyzer:** Extracts and analyzes relevant information from partner profiles, potentially including skills and their corresponding ratings.
  - **Dot Product Layer:** Calculates the similarity between user and partner profiles based on the content analysis, potentially using a weighted combination of Jaccard similarity and cosine similarity.
- **Collaborative Filtering Branch:** User-partner interaction data is processed in this branch to generate collaborative filtering recommendations.
  - **User-latent Vectors and Partner-latent Vectors:** These represent embeddings, which are numerical representations of users and partners in a lower-dimensional latent space. These embeddings are learned through matrix factorization, a technique that decomposes the user-partner interaction matrix into two lower-dimensional matrices.
  - **Rating Prediction:** The user and partner embeddings are used to predict the likelihood of a user interacting with a particular partner. This prediction serves as the collaborative filtering recommender score.
- **Feedback and Update Embeddings:** The system may incorporate user feedback to refine the recommendations over time. Additionally, the user and partner latent vectors (embeddings) are likely updated through an iterative process, such as stochastic gradient descent, to improve the accuracy of rating predictions.

**Overall, the hybrid recommender system architecture leverages both content-based profile information and user-partner interaction data to generate personalized study partner recommendations.**

**References**

<https://www.nvidia.com/en-us/glossary/recommendation-system/>

<https://bluepiit.com/hybrid-recommender-systems/>

<https://www.researchgate.net/publication/374170261_Towards_a_robust_solution_to_mitigate_all_content-based_filtering_drawbacks_within_a_recommendation_system>

[What is collaborative filtering? | IBM](https://www.ibm.com/topics/collaborative-filtering)

[1906.00091 (arxiv.org)](https://arxiv.org/pdf/1906.00091)

[Hybrid recommendation model based on incremental collaborative filtering and content-based algorithms | Semantic Scholar](https://www.semanticscholar.org/paper/Hybrid-recommendation-model-based-on-incremental-Wang-Zhang/3f092f1895077dc64cec5efd5d29b0e1dbf1017c)
