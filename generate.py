import pymongo
import random
import string

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

def gen(seed, subreddit = None):
    #return markov_concat(seed, seed)
    rando = random.randint(12,20)
    comment = seed
    if subreddit:
        suff = get_suffix(seed)
    else:
        suff = get_suffix(seed, subreddit)
    while suff is not None and len(comment.split()) < rando:
	print comment
        print
        comment += " " + suff
        seed = " ".join(comment.split()[-2:])
        suff = get_suffix(seed)
    return prettify(comment)

def markov_concat(comment, seed):
    suffix = get_suffix(seed)
    if suffix is None or len(comment.split()) >= 10: #max=10
        return comment
    else:
        comment += " %s" % suffix
        suffix = " ".join(comment.split()[-2:])
        return markov_concat(comment, suffix)
    
def get_suffix(prefix, subreddit = None):
    connection = pymongo.Connection('localhost', 27017)
    db = connection.new_database
    collection = db.comments
    if subreddit:
        query = {"prefix": prefix, "subreddit":subreddit}
        suffs = collection.find(query).distinct("suffix")
    else:
        suffs = collection.find({"prefix": prefix}).distinct("suffix")
    if len(suffs) == 0:
        return None
    return random.choice(suffs)

def prettify(comment):
    if comment.split()[0].lower() in QUESTION_WORDS:
        comment += "?"
    return comment[0].capitalize() + comment[1:].lower()
