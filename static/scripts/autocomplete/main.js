
var MongoClient = require(['mongodb']).MongoClient;

var uri = "mongodb://wooshir:vgs41999@items-shard-00-00.uxp6f.mongodb.net:27017,items-shard-00-01.uxp6f.mongodb.net:27017,items-shard-00-02.uxp6f.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-wbruxm-shard-0&authSource=admin&retryWrites=true&w=majority";
MongoClient.connect(uri, function(err, client) {
  const collection = client.db("test").collection("devices");
  // perform actions on the collection object
  console.log("success")
  client.close();
});