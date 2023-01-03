
from bson import ObjectId
import os

form_path = "./templates/form"

def list_form_files( directory ):
    return os.listdir( directory )

def get_all_forms(  ):
    return list_form_files( form_path )

def add_data_to_db( collection, data, DB_HOOK, collection_name ):
    #try:
    id =  collection.insert_one( data ).inserted_id
    data[ "link" ] = "/" + str( DB_HOOK ) + "/" + str( collection_name ) + "/" + str( id )
    collection.update_one({"_id": ObjectId( id )}, {"$set": data})
    return id
      
    #except:
    err = "Error: the item was not addded to the DB"
    print( err )
    return err

def fetch_data( collection, filter, projection ):
    try:
        print( "Filter:\t" + str( filter ) , "\tProjection: \t" + str( projection ) )
        print( "Running:\t fetch_data( collection, filters, projection )" )
        if( filter == "all" ):
            print( "\tFlag # 1" )
            res = collection.find(  )

            return res
        else:
            print( "\tFlag # 2" )
            filter = filter.split(',')
            if( projection == "all" ):
                print( "\tFlag # 3" )
                return collection.find( filter )
            else:
                projection = projection.split(',')
                print( "\tFlag # 4" )
                return collection.find( filter, projection )

    except:
        print( "\tFlag # 5" )
        err = "Error: the item was not addded to the DB"
        print( err )
        return err

def filter_collection(collection, field, value):
    """
    Filters a PyMongo collection by a specific field and value.
    
    Parameters:
        - collection: a PyMongo Collection object
        - field: the field to filter on
        - value: the value to filter for
    
    Returns:
        A cursor object containing the documents that match the filter criteria.
    """
    filter = {field: value}
    cursor = collection.find(filter)
    return cursor

def get_possible_values( collection, field ):
    final = []
    possibilities = collection.distinct( field )
    for possibility in possibilities:
        f = {  }
        f[ field ] = possibility
        final.append( f )

    return final

if __name__ == "__main__":
    print( "Locally Ran:\t" + str( "db_get_functions.py" ) )


def strip_whitespace(obj):
    """
    Recursively removes whitespace from the values of a JSON object.
    
    Parameters:
        - obj: the JSON object (can be a dictionary, list, or string)
    
    Returns:
        The JSON object with whitespace removed from all values.
    """
    if isinstance(obj, dict):
        # Iterate over the keys and values in the dictionary
        for key, value in obj.items():
            # Recursively strip whitespace from the value
            obj[key] = strip_whitespace(value)
    elif isinstance(obj, list):
        # Iterate over the elements in the list
        for i, value in enumerate(obj):
            # Recursively strip whitespace from the value
            obj[i] = strip_whitespace(value)
    elif isinstance(obj, str):
        # Strip whitespace from the string
        obj = obj.strip()
    return obj

def create_new_collection( db, name ): # Create the collection
    db.create_collection(name)
    """
    try:
      
       print( "Successfully creted collection:\t" + str( name ) )
    except:
        print( "Failed to create collection:\t" + str( name ) )
    """