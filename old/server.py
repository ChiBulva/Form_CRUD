from flask import Flask, jsonify, request, render_template, redirect
import pymongo
from bson import ObjectId
import json

import scripts.db.db_functions as db_functions

# Connect to the MongoDB database
DB_HOOK = "swanson_mongodb"

client = pymongo.MongoClient( "mongodb://localhost:27017/" )
Swanson_MongoDB = client[ DB_HOOK ]

try:

    mongo = pymongo.MongoClient( "mongodb://localhost:27017", serverSelectionTimeoutMS = 1000 )
    Swanson_MongoDB = mongo[ "Swanson_MongoDB" ]
    mongo.server_info(   ) # If not connected exception will trigger

    print( "successfully connected to MongoDB Server!!!" )
except:
    print( "Cannot Connect to MongoDB!!!" )

app = Flask( __name__ )

def try_collection( collection ):
    try:
        collection = Swanson_MongoDB[ collection ]
    except:
        print( "Cannot Connect to MongoDB collection:\t " + str( collection ) )
    return collection

def Get_Keys( collection ):
    # Create an empty set to store the keys
    keys = set()

    # Iterate over the documents in the collection
    for doc in collection.find(  ):
        # Extract the keys from the document and add them to the set
        keys.update( doc.keys(  ) )

    return list( keys )

# This should have you adding a 
@app.route("/form/<form_name>", methods=["GET"])
def form_render( form_name ):
    try:
        if( form_name == "all_users.html" ):
            form_name = ""
            100 / 0 # Error on purpose
        return render_template( "form/" + str( form_name ), db_hook=DB_HOOK, collection_hook=form_name.replace( ".html", "" ) )
    except:        
        forms = db_functions.get_all_forms(  )
        forms.remove( 'all_forms.html' )
        
        return render_template( "form/all_forms.html", forms=forms, wrong_form_name=form_name, db_hook=DB_HOOK, collection_hook=form_name.replace( ".html", "" ) )

KNOWN_KEYS = [ "emp", "location", "support_request" ]
EMP_KEYS = [ "first_name", "last_name", "location", "_id", "link" ]
LOCATION_KEYS = [ "name", "address", "city", "state", "zip_code", "_id", "link" ]
SUPPORT_REQUEST_KEYS = [ "first_name", "last_name", "title", "supervisor", "location", "priority", "email", "submit_time", "date", "phone", "details", "_id", "link" ]
NEW_USER_REQUEST_KEYS = [ "first_name", "last_name", "title", "supervisor", "location", "priority", "email", "submit_time", "date", "phone", "details", "_id", "link" ]

def keys_case( collection_name ):
    if( collection_name == "emp" ):
        return EMP_KEYS
    elif( collection_name == "location" ):
        return LOCATION_KEYS
    elif( collection_name == "support_request" ):
        return SUPPORT_REQUEST_KEYS    
    else:
        return "Not found"

def assign_keys( collection ):
    collection_name = collection
    
    collection = try_collection( collection )

    if collection_name in KNOWN_KEYS:

        print( "keys_case" )
        return keys_case( collection_name ), collection, collection_name
    else: 
        print( "Get_Keys" )
        return Get_Keys( collection ), collection, collection_name

@app.route("/" + str( DB_HOOK.lower(  ) ) + "/<collection>", methods=["GET"])
def get_items( collection ):
    
    keys, collection, collection_name = assign_keys( collection )
  
    # Grabs all objects in collection and makes them a cursor object
    json_collection = collection.find()

    # Gets all keys for a collection
    

    print( "Keys:\t" + str( keys ) )
    print( "Items:\t" + str( json_collection ) )

    return render_template( "list_colloction.html", collection_name=collection_name, json_collection=json_collection, keys=keys )

# Takes a form and makes it into a json object to add to mongoDB
@app.route("/" + str( DB_HOOK.lower(  ) ) + "/<collection>", methods=["POST"])
def add_item( collection ):
    print( collection )

    collection_name = collection
    collection = try_collection( collection )
    # Add a new item to the "items" collection
    form_fields = request.form.to_dict(  )  

    #print( form_fields )
    item_id = db_functions.add_data_to_db( collection, form_fields, DB_HOOK, collection_name )
    #item_id = collection.insert_one(data).inserted_id

    return redirect( "/" + str( DB_HOOK.lower(  ) ) + "/" + str( collection_name ) )
    return redirect( "/" + str( DB_HOOK.lower(  ) ) + "/" + str( collection_name ) + "/" + str( item_id ) )
    
    #return render_template( "form/all_forms.html", forms=forms, wrong_form_name=form_name )

@app.route("/" + str( DB_HOOK.lower(  ) ) + "/<collection>/<item_id>", methods=["GET"])
def get_item(collection, item_id):
    collection = try_collection( collection )
    # Get a single item by its ID
    item = collection.find_one({"_id": ObjectId(item_id)})
    return jsonify(str(item))

@app.route("/" + str( DB_HOOK.lower(  ) ) + "/<collection>/<item_id>", methods=["PUT"])
def update_item(collection, item_id):
    collection = try_collection( collection )
    # Update an item in the "items" collection
    data = request.json
    collection.update_one({"_id": ObjectId(item_id)}, {"$set": data})
    return jsonify(str({"success": True}))

@app.route("/delete/" + str( DB_HOOK.lower(  ) ) + "/<collection>/<item_id>", methods=["POST"])
def delete_item(collection, item_id):
    collection_name = collection
    collection = try_collection( collection )
    # Delete an item from the "items" collection
    collection.delete_one({"_id": ObjectId(item_id)})
    return redirect( "/" + str( DB_HOOK.lower(  ) ) + "/" + str( collection_name ) )

@app.route( "/get_employees", methods=[ "POST" ] )
def get_employees(  ):
    try:
        user = { "name": "Travis", "last":"Gray", "loc": "GPW" } 
        dbResponse = Swanson_MongoDB.emp.insert_one( user )
        user = { "name": "Jason", "last":"Bennett", "loc": "GPW" } 
        dbResponse = Swanson_MongoDB.emp.insert_one( user )
        user = { "name": "Brad", "last":"Depriest", "loc": "RSM" } 
        dbResponse = Swanson_MongoDB.emp.insert_one( user )
        user = { "name": "Joe", "last":"Pesta", "loc": "SPW" } 
        # Adding data here
        print( "Adding data here:\t" + str( user ))
        dbResponse = Swanson_MongoDB.emp.insert_one( user )
        print( "Added:\t" + str( dbResponse.acknowledged ) )

        return ( { "id": str( dbResponse.inserted_id ) } )
    except Exception as ex:
        print(  "Error!" )
        print(  ex )
        return { "error": "Failed!" }

@app.route( "/create_user", methods=[ "POST" ] )
def create_user(  ):
    return "create users"

if __name__ == "__main__":
    app.run( port=5000, debug=True, host="127.0.0.1" )