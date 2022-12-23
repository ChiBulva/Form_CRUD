
from bson import ObjectId
import os

form_path = "./templates/form"

def list_form_files( directory ):
  return os.listdir( directory )

def get_all_forms(  ):
    return list_form_files( form_path )


def add_data_to_db( collection, data, DB_HOOK, collection_name ):
  try:
    id =  collection.insert_one( data ).inserted_id
    data[ "link" ] = "/" + str( DB_HOOK ) + "/" + str( collection_name ) + "/" + str( id )
    collection.update_one({"_id": ObjectId( id )}, {"$set": data})
    return id
    
  except:
    err = "Error: the item was not addded to the DB"
    print( err )
    return err


if __name__ == "__main__":
    print( "Locally Ran:\t" + str( "db_get_functions.py" ) )