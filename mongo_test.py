import pymongo

connection = pymongo.Connection('localhost', 27017)
db = connection.new_database

collection = db.comments

for i in range(1, 10):
    post = { 'x': 10,
             'y': i
           }
    collection.insert(post)


