

require('mongodb').MongoClient.connect("mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority",function(err,db){
   if(err)
     throw err;
   console.log("connected successfully");
   db.close();
});