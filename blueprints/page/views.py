from flask import Blueprint, render_template, flash, redirect
import requests
from flask import request,redirect,url_for
page = Blueprint('page', __name__, template_folder='templates')
import pymongo
client = pymongo.MongoClient("mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority")
db = client["steam"]

@page.route('/loaderio-89e5a74c98935e38038b0c14e5c7e883/')
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
                
                
                image_url=db.games.find_one({"name":name})["img_url"]
               
                
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
              
                
                image_url=db.games.find_one({"name":name})["img_url"]
                items.append(image_url)
            return render_template('page/search.html', 
                                users=users)    
    elif request.args.get("details"):
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
        
        tags=db.games.find_one({"name":saved_game})["tags"]
        detail.append(",".join(tags))
        avg_session=db.games.find_one({"name":saved_game})["min_space"]
        detail.append(avg_session)
        languages=db.games.find_one({"name":saved_game})["min_ram"]
        detail.append(languages) 
        inputs=db.games.find_one({"name":saved_game})["price"]
        detail.append(inputs)
        desc=db.games.find_one({"name":saved_game})["description"]
        detail.append(desc)
        return render_template('page/details.html',detail=detail)
        



                
                
                
            

            
   

        



@page.route('/terms')
def terms():
    return render_template('page/terms.html')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.html')
