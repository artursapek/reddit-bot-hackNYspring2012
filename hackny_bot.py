import reddit
import pymongo
import re

#419 reddits

connection = pymongo.Connection('localhost', 27017)
db = connection.new_database
collection = db.comments

def run():
    r = reddit.Reddit("acid-trip-bot v.0.1 alpha release")
    r.login("acid-trip-bot","hackny")
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
        for i, com in enumerate(s.comments):
            process_comments(com)
        try:
            s = submissions.next()
        except:
            return

def process_comments(com):
    if 'body' in com.__dict__.keys():
        if com.body == "":
            return
        print com.body

        try:
            add_to_db(markovify(com.body))
        except:
            pass
    else:
        print (process_comments(com.comments))

def markovify(body):
    words = body.split()
    for i in xrange(0,len(words)-1):
        if i == len(words) - 2:
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': None}
        else: 
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': words[i+2]}
        return new_markov

def add_to_db(post):
    collection.insert(post)

def sanitize_comment(comment):
    if len(comment.split()) < 3:
        return None
    while True:
        link = re.search(r'\[(?P<text>.*)\]\(http://.*\)', comment, re.I)
        if not link:
            break
        comment = comment.replace(link.group(0), link.group('text'))
    comment = comment.strip()
    comment = ''.join(re.findall(r'[\w\d\s]', comment))
    return comment 

def read_db():
    for i, x in enumerate(collection.find()):
        print x

def drop_db():
    collection.drop()

if __name__ == "__main__":
    run()
