import reddit
import pymongo

#419 reddits

def run():
    global db 
    connection = pymongo.Connection('localhost', 27017)
    db = connection.new_database
    r = reddit.Reddit("hackny_bot")
    r.login("bzzzz3","bzzzz")
    f = open("subreddits.txt")
    for sub in f.read().split():
        get_threads(sub, r)
    
def get_threads(sub, r):
    submissions = r.get_subreddit(sub).get_top(limit=10)
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
        
        collection = db.comments
        collection.insert(new_markov)

if __name__ == "__main__":
    run()
