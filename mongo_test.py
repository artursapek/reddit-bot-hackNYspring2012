import pymongo

connection = pymongo.Connection('localhost', 27017)
db = connection.new_database

collection = db.comments

#new_comment = {
#                'author': 'AndrewSmith1986',
#                'body': 'Wedep'
#              }
#collection.insert(new_comment)

print db.collection_names()

    

