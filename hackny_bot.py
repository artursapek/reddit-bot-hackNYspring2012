import reddit
import pymongo
#419 reddits

connection = pymongo.Connection('localhost', 27017)
db = connection.new_database
collection = db.comments

def run():
    r = reddit.Reddit("douche-bot v.0.1 alpha release")
    r.login("douche-bot","hackny")
    f = open("subreddits.txt")
    for sub in f.read().split()[0:5]:
        get_threads(sub, r)
   
def get_threads(sub, r):
    submissions = r.get_subreddit(sub).get_top(limit=5)
    try:
        s = submissions.next()
    except StopIteration:
        return
    while s:
        for com in s.comments:
            try:
                process_comments(com)
            except Exception as e:
                print e
                continue
        try:
            s = submissions.next()
        except:
            return

def process_comments(com):
    if 'body' in com.__dict__.keys():
        if com.body == "":
            return
        markovify(com.body)
    else:
        print (process_comments(com.comments))

def markovify(body):
    words = body.split()
    for i in xrange(0,len(words)-1):
        if i == len(words) - 2:
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': None}
        else: 
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': words[i+2]}
        print new_markov
        

def add_to_db(post):
    collection.insert(post)

def generate_sentence(subject):
    

# Reddit functions

def generate_comment(seed):
    comment = seed
    collection = db.comments
    while suffs is not None:
        suffs = collection.find({prefix: seed})

if __name__ == "__main__":
    run()
