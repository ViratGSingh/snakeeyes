from flask import Blueprint, render_template, flash, redirect
import requests
from flask import request,redirect,url_for
page = Blueprint('page', __name__, template_folder='templates')
import pymongo
client = pymongo.MongoClient("mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority")
db = client["itchio"]

@page.route('/loaderio-89e5a74c98935e38038b0c14e5c7e883')
def loader():
    return render_template('page/loaderio-89e5a74c98935e38038b0c14e5c7e883.html')
@page.route('/',  methods=["GET","POST"])
def home():
    if request.method=="POST":
        game=request.form["submit"]
        return redirect(url_for("page.search",game=game))
    else:    
        recoms=db.recom.aggregate([ { "$sample": { "size": 1 } } ])
        for a in recoms:
            name=a["Key"]
            podcast=name.replace(",","_")
            users=a[podcast][:5]  
            
            for items in users:
                name=items[1]
                
                
                image_url=db.listings.find_one({"game_name":name})["image_url"]
               
                
                items.append(image_url)
        

            return render_template('page/search.html', 
                                users=users)

@page.route("/game",  methods=["GET","POST"])

def search():
   
              
    if request.args.get("recommend"):
        podcast=request.args.get("recommend")
        if podcast:
            
            
            recoms=db.recom.find_one({"Key":podcast})
            users=recoms[podcast][:5]  
            for items in users:
                name=items[1]
              
                
                image_url=db.listings.find_one({"game_name":name})["image_url"]
                items.append(image_url)
            return render_template('page/search.html', 
                                users=users)    
    elif request.args.get("details"):
        saved_game=request.args.get("details")
        detail=[]
        name=db.listings.find_one({"game_name":saved_game})["game_name"]
        detail.append(name)
        page_l=db.listings.find_one({"game_name":saved_game})["game_link"]
        detail.append(page_l)
        image_l=db.listings.find_one({"game_name":saved_game})["image_url"]
        detail.append(image_l)
        p_date=db.details.find_one({"game_name":saved_game})["game_published"]
        detail.append(p_date)
        status=db.details.find_one({"game_name":saved_game})["game_status"]
        detail.append(status)
        platforms=db.details.find_one({"game_name":saved_game})["game_platforms"]
        detail.append(",".join(platforms))
        rating=db.details.find_one({"game_name":saved_game})["aggregate_rating"]
        detail.append(rating)
        author=db.details.find_one({"game_name":saved_game})["game_author"]
        detail.append(author)
        engine=db.details.find_one({"game_name":saved_game})["game_engine"]
        detail.append(engine)
        tags=db.details.find_one({"game_name":saved_game})["game_tags"]
        detail.append(",".join(tags))
        avg_session=db.details.find_one({"game_name":saved_game})["game_avg_session"]
        detail.append(avg_session)
        languages=db.details.find_one({"game_name":saved_game})["game_languages"]
        detail.append(",".join(languages)) 
        inputs=db.details.find_one({"game_name":saved_game})["game_inputs"]
        detail.append(",".join(inputs))
        desc=db.details.find_one({"game_name":saved_game})["game_description"]
        detail.append(desc)
        return render_template('page/details.html',detail=detail)
        



                
                
                
            

            
   

        



@page.route('/terms')
def terms():
    return render_template('page/terms.html')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.html')
