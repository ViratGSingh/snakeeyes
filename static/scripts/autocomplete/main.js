
const MongoClient = require(['mongodb']).MongoClient;
const uri = "mongodb+srv://wooshir:vgs41999@dhost:port/steam";
MongoClient.connect(uri, function(err, db) {
    if(db && !err) {
        console.log("connected to mongodb" + " " + lobby_db);
        }
    else if(err) {
        console.log("NOT connected to mongodb " + err + " " + lobby_db);
        }
    });
