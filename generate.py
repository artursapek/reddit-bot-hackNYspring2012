import pymongo
import random

QUESTION_WORDS = ["what",
                  "where",
                  "who",
                  "would",
                  "why",
                  "what",
                  "who",
                  "how",
                  "when",
                  "do",
                  "did",
                  "would",
                  "will",
                  "is",
                  "was"]

def gen(seed):
    rando = random.randint(12,20)
    comment = seed
    suff = get_suffix(seed)
    while suff is not None and len(comment.split()) < rando:
	print comment
        print
        comment += " " + suff
        seed = " ".join(comment.split()[-2:])
        suff = get_suffix(seed)
    return prettify(comment)
    

def get_suffix(prefix):
    connection = pymongo.Connection('localhost', 27017)
    db = connection.new_database
    collection = db.comments
    suffs = collection.find({"prefix": prefix}).distinct("suffix")
    if len(suffs) == 0:
        return None
    return random.choice(suffs)

def prettify(comment):
    if comment.split()[0].lower() in QUESTION_WORDS:
        comment += "?"
    return comment[0].capitalize()[0] + comment[1:].lower()
