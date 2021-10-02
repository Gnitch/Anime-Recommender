import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import statscls
# from ast import literal_eval
import joblib
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

class AnimeRecommender :
    def __init__(self):    
        self.anime_info_df = pd.read_csv(r'recommender\Models\anime.csv')
        self.anime_desc_df = pd.read_csv(r'recommender\Models\anime_with_synopsis.csv')
        self.rating_df = pd.read_csv(r'recommender\Models\rating.csv')
        self.anime_df = pd.merge(self.anime_desc_df,self.anime_info_df[['MAL_ID','Type','Popularity','Members','Favorites']],on='MAL_ID')
        self.anime_df = self.anime_df[(self.anime_df["Score"] != "Unknown") & ((self.anime_df["Type"] == "TV") | (self.anime_df["Type"] == "Movie")) ] 
        self.anime_df['sypnopsis'] = self.anime_df['sypnopsis'].fillna('')
        
        # Content Filtering
        tfidf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.anime_df['sypnopsis'])        
        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        self.anime_df = self.anime_df.reset_index()
        self.titles = self.anime_df['Name']
        self.indices = pd.Series(self.anime_df.index, index=self.anime_df['Name'])   
        print('content initialised')

        # Hybrid Filtering
        # self.model = joblib.load(r'recommender\Models\svd.joblib')                     
        # print('hybrid initialised')


    def content(self,title):  
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        anime_indices = [i[0] for i in sim_scores]
        
        anime_lst = self.anime_df.iloc[anime_indices][['MAL_ID','Name', 'Members', 'Score']]
        favorite_count = anime_lst[anime_lst['Members'].notnull()]['Members'].astype('int')
        score_avg = anime_lst[anime_lst['Score'].notnull()]['Score'].astype('float')
        C = score_avg.mean()
        m = favorite_count.quantile(0.60)
        qualified = anime_lst[(anime_lst['Members'] >= m) & (anime_lst['Members'].notnull()) & (anime_lst['Score'].notnull())]
        qualified['Members'] = qualified['Members'].astype('int')
        qualified['Score'] = qualified['Score'].astype('float')
        def weighted_rating(x):
            v = x['Members']
            R = x['Score']
            return (v/(v+m) * R) + (m/(m+v) * C)           
        qualified['wr'] = qualified.apply(weighted_rating, axis=1)
        qualified = qualified.sort_values('wr', ascending=False)    
        return qualified

    def hybrid(self,user_id,title):
        id_map = self.anime_df[['MAL_ID']]
        id_map['id'] = list(range(1,self.anime_df.shape[0]+1,1))
        id_map = id_map.merge(self.anime_df[['MAL_ID', 'Name','Genres','Score']], on='MAL_ID').set_index('Name')   
        indices_map = id_map.set_index('id')        
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        anime_indices = [i[0] for i in sim_scores]
        anime_lst = self.anime_df.iloc[anime_indices][['MAL_ID','Name', 'Members', 'Score']]          
        anime_lst['id'] = list(range(1,anime_lst.shape[0]+1,1))  
        anime_lst['est'] = anime_lst['id'].apply(lambda x: self.model.predict(user_id, indices_map.loc[x]['MAL_ID']).est)
        anime_lst = anime_lst.sort_values('est', ascending=False)
        result = anime_lst['MAL_ID']         
        return result.head(5)



    
    

