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
    return comment[0].capitalize() + comment[1:].lower()

def punctuate(comment):
    words = comment.split()
    comment = ''
    for x in words:
        if random.choice([True, False, False, False, False, False]):
            comment += ' %s ' % (random.choice(['!!!', '.', '...', '??']) + x)
        else:
            comment += ' %s' % x
    return comment
            

def exasperation(): # some weird bullshit
    no_vowels = random.choice(range(1, 3))
    no_consonants = random.choice(range(3, 10))
    vow = 'aeiou'
    cons = 'bcdfghjklmnpqrtvwxz'
    chosen_cons = random.choice([x for x in cons])
    chosen_vow = random.choice([x for x in vow])
    exasp = chosen_vow*no_vowels + chosen_cons*no_consonants
    return exasp




