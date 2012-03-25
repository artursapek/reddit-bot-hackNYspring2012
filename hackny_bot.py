import reddit
import pymongo
import re
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import urllib2, urllib
import cookielib
import json
import generate
import sys

connection = pymongo.Connection('localhost', 27017)
db = connection.new_database
collection = db.comments

def crawl():
    r = reddit.Reddit("acid-trip-bot v.0.1 alpha release")
    r.login("acid-trip-bot","hackny")
         
#   f = open("subreddits.txt")
#   for sub in f.read().split()[240:290]:
    get_threads('4chan', r)
   
def get_threads(sub, r):
    submissions = r.get_subreddit(sub).get_top(limit=40)
    try:
        s = submissions.next()
    except StopIteration:
        return
    while s:
        for i, com in enumerate(s.comments):
            process_comments(com, sub)
        try:
            s = submissions.next()
        except:
            return

def process_comments(com, sub):
    if 'body' in com.__dict__.keys():
        if com.body == "":
            return
        try:
            entries = markovify(sanitize_comment(com.body))
            print entries
            for entry in entries:
                if collection.find({'prefix': entry['prefix'], 'suffix': entry['suffix']}).count() == 0 and len(entry['prefix']) + len(entry['suffix']) < 40:
                    entry['subreddit'] = sub
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

def count():
    search = collection.find()
    print search.count()

def drop_db():
    collection.drop()

# Reddit functions

def confirm(seed, subreddit = None):
    comment = generate.gen(seed, subreddit)
    print comment
    yn = raw_input("Wanna post this shit? Y/N: ")
    if yn.lower() == "y":
        respond(sys.argv[1], comment)
    else:
        new_seed = raw_input("New seed? (blank=same) ")
        if len(new_seed.split()) == 2:
            confirm(new_seed)
        else:
            confirm(seed)

def respond(permalink, text):
    br = Browser()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1'
    br.addheaders = [('User-agent', user_agent)]

    soup = BeautifulSoup(br.open(permalink).read())

    urlopen = urllib2.urlopen
    Request = urllib2.Request
    encode = urllib.urlencode
    cj = cookielib.LWPCookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    root_comment = soup.find('form', attrs={'class': 'usertext border'})
    thing_id = root_comment.find('input', attrs={'name': 'thing_id'})['value']
    print 'thing_id', thing_id

    # LOG THE FUCK IN
    req = Request('http://www.reddit.com/api/login/username', encode({'user': 'acid-trip-bot', 'passwd': 'hackny', 'api_type': 'json'}), {'User-Agent': user_agent})
    req_open = urlopen(req)
    read = json.loads(req_open.read())

    modhash = read['json']['data']['modhash']

    # POST THE FUCKING COMMENT
    req = Request('http://www.reddit.com/api/comment', encode({'thing_id': thing_id, 'text': text + '\n\n*This is an automated response.*', 'uh': modhash}), {'User-Agent': user_agent})
    req_open = urlopen(req)
    read = json.dumps(req_open.read())

if __name__ == "__main__":
    test = collection.find({'subreddit': '4chan'})
    for x in test:
        print x
else:
    print '''
                                                                                
                                                                                
          MMMMMMM7              .MMMMMM.      NMMMMMM     ZMMMMMMMN             
       .MMMMMMMMMMM.          .MMMMMMMMMMMM  MMMMMMMMM   MMMMMMMMMMMMMM..       
         MMMMMMMMMMM.        8MMMMMMMMMMMMM.  MMMMMMM   . MMMMMMM. MMMMMM.      
         MMMMMMMMMMM.      .MMMMMMMM.  MMMM    MMMMMM      MMMMMM   MMMMMM      
         MMM,..MMMMMM       MMMMMM,    .MM8.  .MMMMM=      MMMMMM   .MMMMMM     
         MMM   MMMMMM.     MMMMMMM            .MMMMM.      MMMMMM   .MMMMMM     
        .MMMMMMMMMMMM.     MMMMMMM            ,MMMMMM      MMMMMM   .MMMMMM .   
       .MMMMMMMMMMMMMM     MMMMMMM.     MM    MMMMMMM.    .MMMMMM    MMMMMM7.   
        MMM=    MMMMMMO    MMMMMMMMMMMMMMMM. .MMMMMMM.     MMMMMM   MMMMMMM+    
       MMMM     MMMMMMM .  MMMMMMMMMMMMMMMM. .MMMMMMM$    ~MMMMMMMMMMMMMMMM     
     .MMMMM.    MMMMMMMM.. 8MMMMMMMMMMMMMMM  :MMMMMMMM    MMMMMMMMMMMMMMMMM     
   .~MMMMMMM   MMMMMMMMMM.  MMMMMMMMMMMMMMM  MMMMMMMMMM.. MMMMMMMMMMMMMMMM      
   MMMMMMMMMM  MMMMMMMMMMM   ZMMMMMMMMMMMM: MMMMMMMMMMM7?MMMMMMMMMMMMMMMM       
  .MMMMMMMMMM  MMMMMMMMMM     .MMMMMMMMMM   MMMMMMMMMMM MMMMMMMMMMMMMMMM .      
      I87~      ..7OI. .          .  .       .~DMMMM7 .    IMMMMMMMZ.           
                                                                                
                                                                                
    '''
    if len(sys.argv) == 5:
        #crawl()
        seed = sys.argv[2]+" "+sys.argv[3]
        if sys.argv[4] == '4chan':
            print '''
                                                                                         
                                                  ....                          
                                                ,88OO8O=.                       
                .+ZOOOOZ?..                   .=8Z,,,,=88,.  ...                
            ..$88?::,,,:+88Z,                .~8$,~~~~:,O8~.O88888+.            
           .:88~:~======~:,7OO,.            ..OO:~=====~,7888,,:,+8O,.          
           .O8.:===========::88~.            ~O7:========~7O+~===::88.          
           .:88I~~=+++++++++=:7OI..          =8I:++++++++++=++++++:+8?..        
            ..+8OO?+?????????+~?8$.         .=8I~+????????????????~=O$..        
          .=88Z?==?IIIIIIIIIII?=?87.        .=87~?IIIIIIIIIIIIIII?~I8=          
        .$8O+~?I777777777777777I~$8=        .~O$=I7777777777777I?~I8I.          
       .$O?7OOOOOOO8OOOOOOOOOOOOO?O8.       ..OZIOOOOOOOOO8OOOO$?O8?.           
      ..ZO+IZOOOOOOOOOOOOOOOOOOOO$+8O.      . O8?ZOOOOOOOOOOZ?IO87..            
        .O8O?+I$ZZZZOOOOZZZZZ$7I?+~$O~        =87IZOOOOOZ$??Z887..              
         ..:Z88OOZZIIIIIIZZOOO888OZ7,.        .88~7$7?+=$O8O?...                
            .....,:+++++=:,.......            .=87=ZO88O~...                    
                                              ..+8?:....                        
                                                 .                              
                                                                                
                                                                                
                            . .~~.                                              
                        ..,I88O78I.         .. ....,,::~~~~::,,....             
                    ...=88OI.,,,?8=.      .=88888OOZZ$$7III$$ZZO888+.. .        
                   .=O8Z:,:~~~~~,ZO,     ..$O:.,:::~~~~~~~~~~~::,,:I88I..       
                ..788=,~========:=8I.      ~8I,====================~,:O8.       
               .=88=:===+++=+====,O8..     .O8:~===+++++====++==+===~,$8.       
              .Z8I:=+++++++++++++~~8Z       .8O,=+++++++++++++++++~:I88:.       
            ..O8~=???????????????+~ZO.      .=O7~+????????????+~~7O88, .        
            .?8I7OOOOOOOOOOOOOOOOO7$O~      ..I877OOOOOOOOOOOZO8O+..            
            .I8I$OOOOOOOOOOOOOOOOO$7O?        .?8$IOOOOOOOOOOOZ$O8O.            
            .=87IOOOOOOOOOOOOOOOOO$7O?          =8O+ZOOOOOOOOOOO?+OI            
            ..$8I7OOOO$OOZ$OOOOOOO7$8+           .O8Z?$OOOOOOOO7+O8.            
              .$OZ?7$+$8I8O?ZOOOOZ?Z8.             :O8OI??????788$.             
                .$88888:.,887IZOO?78~.              ..:7Z888OZI,                
                   ..      :O8OIIO8=                                            
                             .,++:.                                             
                                                                                
                                                                                
    '''
        confirm(seed, sys.argv[4])
    else:
        print "Usage: python hackny_bot.py <url> <seed1> <seed2>"

