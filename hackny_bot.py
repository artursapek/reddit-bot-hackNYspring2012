import reddit
import pymongo

#419 reddits
N = 2

def run():
    connection = pymongo.Connection('localhost', 27017)
    global db = connection.new_database
    r = reddit.Reddit("hackny_bot")
    r.login("bzzzz3","bzzzz")
    f = open("subreddits.txt")
    for sub in f.read().split():
        get_threads(sub, r)
    
def get_reddit_id(url):
    result = re.search('/comments/(.*?)/', url)
    return result.group(1)

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
            except:
                continue
        try:
            s = submissions.next()
        except:
            return

def process_comments(com):
    if 'body' in com.__dict__.keys():
        if com.body == "":
            return
        add_to_db(com_body)
    else:
        print (process_comments(com.comments))

def add_to_db(body):
    new_comment = {'body': body}
    collection = db.comments
    collection.insert(new_comment)

def markovify(body):
    words = body.split()
    for i in xrange(0,len(words)):
        if i == len(words) - N:
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': None}
        else:    
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': words[i+2]}

if __name__ == "__main__":
    run()
