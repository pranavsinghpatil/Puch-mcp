# app/services/recommend_service.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("app/data/recipes.csv")  # Must have 'name' & 'ingredients' columns

def recommend_dishes(dish_name, top_n=3):
    if dish_name.lower() not in df['name'].str.lower().values:
        return []
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['ingredients'])
    
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    idx = df[df['name'].str.lower() == dish_name.lower()].index[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    return df.iloc[[i[0] for i in sim_scores]]['name'].tolist()
