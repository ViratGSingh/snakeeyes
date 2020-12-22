
var MongoClient = require(['mongodb']).MongoClient;
var uri = "mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/steam?retryWrites=true&w=majority";
var client = new MongoClient(uri, { native_parser: true });
client.connect(err => {
  const collection = client.db("steam").collection("g_recom");
  // perform actions on the collection object
  client.close();
});