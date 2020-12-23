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
        recoms=db.top_g.aggregate([ { "$sample": { "size": 6 } } ])
        games=[]
        for a in recoms:
            
            name=a["name"]
            i_url=a["img_url"]
            r_date=a["release_date"]
            dev=a["developer"]
            t_tags=a["top_tags"]
            is_free=a["free"]
            a_rating=a["all_rating"]
            
            
            games.append(["0",name,dev,r_date,t_tags,i_url,is_free,"0",a_rating])
            
            

        return render_template('page/search.html', 
                                games=games)


@page.route('/search',  methods=["GET","POST"])
def find():
    if request.args.get("item"):
        name=request.args.get("item")
        name=name.lower()
        name=name.replace(".","*")
        name=name.replace(" ","_")
        name=name.replace("$","&")
        req=db.g_recom.find({"Key": name})
        for i in req:
            games=i[name]  
        return render_template('page/search.html', 
                            games=games) 

@page.route("/game",  methods=["GET","POST"])

def search():
   
              
    if request.args.get("recommend"):
        game=request.args.get("recommend")
        if game:
            name=game.replace(".","*")
            name=name.replace(" ","_")
            name=name.replace("$","&")
            name=name.lower()
            req=db.g_recom.find({"Key": name})
            for i in req:
                games=i[name]  
            return render_template('page/search.html', 
                                games=games)    
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
        space=db.games.find_one({"name":saved_game})["min_space"]
        detail.append(space)
        ram=db.games.find_one({"name":saved_game})["min_ram"]
        detail.append(ram) 
        rr=db.games.find_one({"name":saved_game})["recent_rating"]
        detail.append(rr)
        ar=db.games.find_one({"name":saved_game})["all_rating"]
        detail.append(ar)
        price=db.games.find_one({"name":saved_game})["price"]
        detail.append(price)
        pl=db.games.find_one({"name":saved_game})["os_l"]
        try:
            for i in range(0,len(pl)):
                if pl[i]=="win":
                    pl[i]="Windows"
                elif pl[i]=="mac":
                    pl[i]="Mac"
                elif pl[i]=="linux":
                    pl[i]=="Linux"
                else:
                    continue  

        except:
            pass                
        detail.append(",".join(pl))
        return render_template('page/details.html',detail=detail)
        
  

                
                
                
            

            
   

        



@page.route('/terms')
def terms():
    return render_template('page/terms.html')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.html')
