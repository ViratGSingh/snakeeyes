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
        recoms=db.indie.aggregate([ { "$sample": { "size": 6 } } ])
        games=[]
        for a in recoms:
            name=a["name"]
            i_url=a["img_url"]
            r_date=a["release_date"]
            dev=a["developer"]
            t_tags=a["top_tags"]
            p_rating=a["all_p"]
            tr_code=str(a["tag_code"])+','+str(a["rating_code"])
            
            games.append([name,i_url,r_date,dev,t_tags,p_rating,tr_code])
            
            

        return render_template('page/search.html', 
                                games=games)


@page.route("/game",  methods=["GET","POST"])

def search():
   
              
    if request.args.get("recommend"):
        game=request.args.get("recommend")
        if game:
            codes=game.split(",")
            t_code=int(codes[0])
            r_code=int(codes[1])
            r=db.indie.find({'$and':[{"tag_code":{'$lte':t_code}},{"rating_code":{'$lte':r_code}}]}).sort([("tag_code", -1), ("rating_code", -1)]).limit(5)
            games=[]
            for a in r:
                name=a["name"]
                i_url=a["img_url"]
                r_date=a["release_date"]
                dev=a["developer"]
                t_tags=a["top_tags"]
                p_rating=a["all_p"]
                tr_code=str(a["tag_code"])+','+str(a["rating_code"])
                
                games.append([name,i_url,r_date,dev,t_tags,p_rating,tr_code])

               
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
