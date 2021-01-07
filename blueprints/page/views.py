from flask import Blueprint, render_template, flash, redirect,jsonify
import requests
from flask import request,redirect,url_for
page = Blueprint('page', __name__, template_folder='templates')
import pymongo
import json
from flask_login import current_user
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

@page.before_request
def beforeRequest():
    if not request.url.startswith('https'):
        return redirect(request.url.replace('http', 'https', 1))

    

@page.route('/autocomplete',  methods=["GET","POST"])
def auto():
    game = request.args.get('query')
    result = db.recom.aggregate([

            {

                "$search": {

                    "autocomplete": {

                        "query": game,

                        "path": "Autocomplete",

                        "fuzzy": {

                            "maxEdits": 2,

                            "prefixLength": 3

                        }

                    }

                }

            },
            { "$limit" : 5 }

        ])
    l=[]    
    for i in result:
      l.append(i["Autocomplete"])
    return json.dumps(l)   
    
    
@page.route('/',  methods=["GET","POST"])
def start():
      

        return render_template('page/home.html')



@page.route('/search',  methods=["GET","POST"])
def find():
    
    if request.method=="POST":
        game=request.form["submit"]
        return redirect(url_for("page.search",game=game))
   
    elif request.args.get("game") :
        name=request.args.get("game")
       
        name=name.lower()
        name=name.replace(".","*")
        name=name.replace(" ","_")
        name=name.replace("$","&")
        req=db.recom.find({"Key": name})
        for i in req:
            sgames=i[name]  
        
        if current_user.is_authenticated:
                
                user=db.search.find_one({"user":current_user.email})
                if user:
                    
                    user=db.search.find_one({"user":current_user.email})
                    
                    req=db.recom.find_one({"Key": name})
                    name=req["Autocomplete"]
                    games=user["games"]+[name]
                    game=db.games.find_one({"name":name})
                    tags=user["tags"]+[",".join(game["tags"])]
                    rating_codes=user["rating_codes"]+[game["rating_code"]]
                    db.search.update(
                                    { "user": current_user.email },
                                    {
                                        "$inc": { "count": 1 },
                                        "$set": {
                                                    "tags": tags,
                                                    "games": games,
                                                    "rating_codes": rating_codes,
                                                    
                                        }
                                        
                                        
                                    }
                                    )
                else:
                    
                    req=db.recom.find_one({"Key": name})
                    name=req["Autocomplete"]
                    game=db.games.find_one({"name":name})
                    db.search.insert_one({"user":current_user.email
                                        ,"games":[game["name"]]
                                      
                                        ,"tags":[",".join(game["tags"])]
                                        ,"count":0
                                        ,"rating_codes":[game["rating_code"]]})
        else:
                pass 
        return render_template('page/search.html', 
                            games=sgames) 
                         
    
    else:   
        
        return render_template('page/home.html')

@page.route("/game",  methods=["GET","POST"])

def search():
   
              
    if request.args.get("recommend"):
            game=request.args.get("recommend")
            
            if current_user.is_authenticated:
                
                user=db.mlt.find_one({"user":current_user.email})
                if user:
                    user=db.mlt.find_one({"user":current_user.email})
                    name=request.args.get("recommend")
                    game=db.games.find_one({"name":name})
                    games=user["games"]+[name]
                    tags=user["tags"]+[",".join(game["tags"])]
                    rating_codes=user["rating_codes"]+[game["rating_code"]]
                    db.mlt.update(
                                    { "user": current_user.email },
                                    {
                                        "$inc": { "count": 1 },
                                        "$set": {
                                                    "tags": tags,
                                                    "games": games,
                                                    "rating_codes": rating_codes,
                                                    
                                        }
                                        
                                        
                                    }
                                    )
                else:
                    name=request.args.get("recommend")
                    game=db.games.find_one({"name":name})
                    db.mlt.insert_one({"user":current_user.email
                                        ,"games":[game["name"]]
                                       
                                        ,"tags":[",".join(game["tags"])]
                                        ,"count":0
                                        ,"rating_codes":[game["rating_code"]]})
            else:
                    pass 
            name=request.args.get("recommend")       
            name=name.replace(".","*")
            name=name.replace(" ","_")
            name=name.replace("$","&")
            name=name.lower()
            req=db.recom.find_one({"Key": name})
            games=req[name]
                  
            return render_template('page/search.html', 
                                games=games) 
             
                                  
    elif request.args.get("details"):
        
        if current_user.is_authenticated:
                
                user=db.details.find_one({"user":current_user.email})
                if user:
                    user=db.details.find_one({"user":current_user.email})
                    name=request.args.get("details")
                    game=db.games.find_one({"name":name})
                    games=user["games"]+[name]
                    tags=user["tags"]+[",".join(game["tags"])]
                    rating_codes=user["rating_codes"]+[game["rating_code"]]
                    db.details.update(
                                    { "user": current_user.email },
                                    {
                                        "$inc": { "count": 1 },
                                        "$set": {
                                                    "tags": tags,
                                                    "games": games,
                                                    "rating_codes": rating_codes,
                                                    
                                        }
                                        
                                        
                                    }
                                    )
                else:
                    name=request.args.get("details")
                    game=db.games.find_one({"name":name})
                    db.details.insert_one({"user":current_user.email
                                        ,"games":[game["name"]]
                                       
                                        ,"tags":[",".join(game["tags"])]
                                        ,"count":0
                                        ,"rating_codes":[game["rating_code"]]})
        else:
                pass 
        saved_game=request.args.get("details")
        detail=[]
        
        name=db.games.find_one({"name":saved_game})["name"]
        detail.append(name)
        page_l=db.games.find_one({"name":saved_game})["link"]
        detail.append(page_l)
        image_l=db.games.find_one({"name":saved_game})["img_url"]
        detail.append(image_l)
        p_date=db.games.find_one({"name":saved_game})["release_date"]
        detail.append(p_date)
        # status=db.games.find_one({"name":saved_game})["game_status"]
        # detail.append(status)
        # platforms=db.details.find_one({"name":saved_game})["game_platforms"]
        # detail.append(",".join(platforms))
        # rating=db.details.find_one({"name":saved_game})["aggregate_rating"]
        # detail.append(rating)
        author=db.games.find_one({"name":saved_game})["developer"]
        detail.append(author)
        
        tags=db.games.find_one({"name":saved_game})["top_tags"]
        detail.append(tags)
        desc=db.games.find_one({"name":saved_game})["description"]
        detail.append(desc)
        ram=db.games.find_one({"name":saved_game})["min_ram"]
        detail.append(ram) 
        rr=db.games.find_one({"name":saved_game})["recent_rating"]
        rr=rr.split('.')
        detail.append(rr[0])
        ar=db.games.find_one({"name":saved_game})["all_rating"]
        ar=ar.split('.')
        detail.append(ar[0])
        price=db.games.find_one({"name":saved_game})["price"]
        if type(price)==int:
            price="₹"+str(price)
        else:
            price="No info"    
        detail.append(price)
        pl=db.games.find_one({"name":saved_game})["os_l"]
        tpl=[]
        try:
            for i in range(0,len(pl)):
                if pl[i]=="win":
                    pl[i]="Windows"
                    tpl.append(pl[i])
                elif pl[i]=="mac":
                    pl[i]="Mac"
                    tpl.append(pl[i])
                elif pl[i]=="linux":
                    pl[i]=="Linux"
                    tpl.append(pl[i])  
                else:
                    continue  

        except:
            tpl.append("No info")               
        detail.append(",".join(tpl))
        return render_template('page/details.html',detail=detail)
        
@page.route('/discover',  methods=["GET","POST"])
def discover(): 
    if current_user.is_authenticated:
        name=current_user.email
        user=db.search.find_one({"user":current_user.email})
        tags=user["tags"]
        games=pr(name,tags)
        return render_template('page/search.html', 
                                games=games) 
    else:
        return render_template('page/home.html')                           


                
                
                
            

            
   

        



