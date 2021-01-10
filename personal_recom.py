import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np


def pr(name,tags):
     
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), stop_words='english')
        tfidf_matrix = tf.fit_transform(tags) 
        # http://stackoverflow.com/questions/16078015/
        scores = zip(tf.get_feature_names(),
                    np.asarray(tfidf_matrix.sum(axis=0)).ravel())
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        l=[]
        for item in sorted_scores[:10]:
            l.append(item[0])
        tags= ",".join(l)
        client = pymongo.MongoClient("mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority")
        db = client["steam"]
        df=db["games"]
        item=df.find()
        games=[]
        content=[]
        developer=[]
        r_date=[]
        tt=[]
        iurl=[]
        ifree=[]
        rec_r=[]
        all_r=[]
        games.append(name)
        content.append(tags)
        developer.append("no info")
        r_date.append("no info")
        tt.append("no info")
        iurl.append("no info")
        ifree.append("no info")
        rec_r.append("no info")
        all_r.append("no info")
        for data in item:
          
          
            if int(data["all_p"]) >= 75:
                
                games.append(data["name"])
                developer.append(data["developer"])
                r_date.append(data["release_date"])
                tt.append(data["top_tags"])
                iurl.append(data["img_url"])
                ifree.append(data["price"])
                rec_r.append(data["recent_rating"])
                all_r.append(data["all_rating"])
                tags_list=data["tags"]
                if tags_list:
                  t=",".join(tags_list)
                else:
                  t="no info"
                tags_str=t
                content.append(tags_str)
                
            else:
                continue  
              
        game_df=pd.DataFrame({"Game":games,
                              "Content":content,
                              "Developer":developer,
                              "Release_Date":r_date,
                              "Top_Tags":tt,
                              "Image_url":iurl,
                              "Is_Free":ifree,
                              "Rec_r":rec_r,
                              "All_r":all_r})
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), stop_words='english')
        tfidf_matrix = tf.fit_transform(game_df['Content'])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) 
        results = {}

        for idx, row in game_df[:1].iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-15:-1]
            
            
            similar_items = [(cosine_similarities[idx][i] ,game_df["Game"][i] ,game_df["Developer"][i],game_df["Release_Date"][i],game_df["Top_Tags"][i],game_df["Image_url"][i] ,game_df["Is_Free"][i],game_df["Rec_r"][i],game_df["All_r"][i]) for i in similar_indices]

            # First item is the item itself, so remove it.
            # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
            results[row['Game']] = similar_items[1:]
        return results[name]


client = pymongo.MongoClient("mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority")
db = client["steam"]

users=db.search.find()
if users:
    for i in users:
      name=i["user"]
      check=db.discover.find_one({"user":name})
      if check:
            mlt_tags=db.mlt.find_one({"user":name})
            try:
                mlt_tags=mlt_tags["tags"]
            except:
                mlt_tags=[]  
            try:
                s_tags=i["tags"]
            except:
                s_tags=[]  
            d_tags=db.details.find_one({"user":name})
            try:
                d_tags=d_tags["tags"]
            except:
                d_tags=[]  
            tags=mlt_tags+s_tags+d_tags
            item={
                "user":name,
                "items":pr(name,tags)
            }
            col = db["discover"] 
            col.update_one(
                { "user": name },
                {   
                    "$set":{ "items":item}
                })
        
      else:    
            mlt_tags=db.mlt.find_one({"user":name})
            try:
                mlt_tags=mlt_tags["tags"]
            except:
                mlt_tags=[]  
            try:
                s_tags=i["tags"]
            except:
                s_tags=[]  
            d_tags=db.details.find_one({"user":name})
            try:
                d_tags=d_tags["tags"]
            except:
                d_tags=[]  
            tags=mlt_tags+s_tags+d_tags
            item={
                "user":name,
                "items":pr(name,tags),
              
            }
            col = db["discover"] 
            col.insert_one(item)
else:
  pass
  