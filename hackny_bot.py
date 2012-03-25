import reddit
import pymongo
import re
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import urllib2, urllib
import cookielib

connection = pymongo.Connection('localhost', 27017)
db = connection.new_database
collection = db.comments

def crawl():
    r = reddit.Reddit("acid-trip-bot v.0.1 alpha release")
    r.login("acid-trip-bot","hackny")
    f = open("subreddits.txt")
    for sub in f.read().split()[100:140]:
        get_threads(sub, r)
   
def get_threads(sub, r):
    submissions = r.get_subreddit(sub).get_top(limit=10)
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
        try:
            entries = markovify(sanitize_comment(com.body))
            print entries
            for entry in entries:
                if collection.find({'prefix': entry['prefix'], 'suffix': entry['suffix']}).count() == 0 and len(entry['prefix']) + len(entry['suffix']) < 40:
                    add_to_db(entry)
                    print '.'
        except:
            pass
    else:
        pass

def markovify(body):
    dicts = [ ]
    words = body.split()
    for i in xrange(0,len(words)-1):
        if i == len(words) - 2:
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': None}
        else: 
            new_markov = {'prefix':words[i]+" "+words[i+1], 'suffix': words[i+2]}
        dicts.append(new_markov)
    return dicts

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

def test():
    search = collection.find()
    print search.count()

def drop_db():
    collection.drop()

# Reddit functions

def respond(permalink):
    br = Browser()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1'
    br.addheaders = [('User-agent', user_agent)]

    soup = BeautifulSoup(br.open(permalink).read())

    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.LWPCookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    root_comment = soup.find('form', attrs={'class': 'usertext border'})
    thing_id = root_comment.find('input', attrs={'name': 'thing_id'})['value']
    print 'thing_id', thing_id

    # LOG THE FUCK IN
    req = Request('http://www.reddit.com/api/login/username', urllib.urlencode({'user': 'acid-trip-bot', 'passwd': 'hackny', 'api_type': 'json'}), {'User-Agent': user_agent})
    req_open = urlopen(req)
    read = req_open.read()
    print read



if __name__ == "__main__":
    respond('http://www.reddit.com/r/funny/comments/pa3dh/woody_harrelsons_publicist/c3nqfnv')

