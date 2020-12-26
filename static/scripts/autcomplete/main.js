const { MongoClient, ObjectID } = require("mongodb");

const Express = require("express");

const Cors = require("cors");

const BodyParser = require("body-parser");

const { request } = require("express");

const client = new MongoClient("mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority",{useUnifiedTopology: true});

const server = Express();

server.use(BodyParser.json());

server.use(BodyParser.urlencoded({ extended: true }));

server.use(Cors());

var collection;





server.listen("https://snake-eyes.herokuapp.com", async () => {

    try {

        await client.connect( );

        collection = client.db("steam").collection("g_recom");

    } catch (e) {

        console.error(e);

    }

});


server.get("/search", async (request, response) => {

    try {
        
        let result = await collection.aggregate([

            {

                "$search": {

                    "autocomplete": {

                        "query": `${request.query.query}`,

                        "path": "Key",

                        "fuzzy": {

                            "maxEdits": 2,

                            "prefixLength": 3

                        }

                    }

                }

            }

        ]).toArray();

        response.send(result);

    } catch (e) {

        response.status(500).send({ message: e.message });

    }

});

