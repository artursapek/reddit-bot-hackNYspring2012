import pymongo

def generate_comment(seed):
    comment = seed
    suff = get_suffix(seed)
    while suff is not None:
        comment += " " + suff
        seed = comment.split()[-2:]
        suff = get_suffix(seed)
    return comment

def get_suffix(prefix):
    connection = pymongo.Connection('localhost', 27017)
    db = connection.new_database
    collection = db.comments
    return random.choice(collection.find({prefix: prefix}))
    
