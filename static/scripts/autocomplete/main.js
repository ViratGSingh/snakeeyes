
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });
client.connect(err => {
  const collection = client.db("steam").collection("g_recom");
  // perform actions on the collection object
  console.log("success");
  client.close();
});