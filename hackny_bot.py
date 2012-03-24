import reddit
import pymongo

#419 reddits

SUBS_LIST = ['4chan', 'AbandonedPorn', 'adventuretime', 'AdviceAnimals', 'AlienBlue', 'alternativeart', 'AMA', 'Amateur', 'amiugly', 'Anarchism', 'Android', 'AnimalPorn', 'anime', 'announcements', 'answers', 'Anthropology', 'apple', 'ArcherFX', 'architecture', 'arresteddevelopment', 'Art', 'AsianHotties', 'AskReddit', 'askscience', 'asmr', 'asoiaf', 'ass', 'Astronomy', 'atheism', 'Austin', 'australia', 'Autos', 'aww', 'Bacon', 'Bad_Cop_No_Donut', 'Baking', 'baseball', 'battlestations', 'beer', 'bestof', 'bicycling', 'biology', 'blog', 'Blowjobs', 'boardgames', 'Boobies', 'books', 'boston', 'breakingbad', 'Buddhism', 'buildapc', 'business', 'BuyItForLife', 'calvinandhobbes', 'CampingandHiking', 'canada', 'cannabis', 'carlhprogramming', 'cars', 'catpictures', 'cats', 'Celebs', 'CFB', 'chemistry', 'chicago', 'Christianity', 'chrome', 'circlejerk', 'CityPorn', 'classicalmusic', 'classicrage', 'climbing', 'coding', 'Coffee', 'cogsci', 'collapse', 'comicbooks', 'comics', 'community', 'compsci', 'conspiracy', 'Cooking', 'cordcutters', 'creepy', 'cumsluts', 'cyberlaws', 'DealsReddit', 'Demotivational', 'depression', 'DepthHub', 'Design', 'DesignPorn', 'DestructionPorn', 'Dexter', 'Diablo', 'dirtysmall', 'DIY', 'DnB', 'doctorwho', 'Documentaries', 'DoesAnybodyElse', 'Dogfort', 'dogs', 'DotA2', 'Drugs', 'drunk', 'dubstep', 'dwarffortress', 'EarthPorn', 'Economics', 'economy', 'education', 'electrohouse', 'electronicmusic', 'electronics', 'EmmaWatson', 'energy', 'engineering', 'Enhancement', 'entertainment', 'Entrepreneur', 'environment', 'europe', 'explainlikeimfive', 'facepalm', 'Fantasy', 'fashion', 'Favors', 'feminisms', 'fffffffuuuuuuuuuuuu', 'fffffffuuuuuuuuuuuud', 'fifthworldproblems', 'finance', 'firefly', 'firstworldproblems', 'fitmeals', 'Fitness', 'food', 'Foodforthought', 'FoodPorn', 'ForeverAlone', 'forhire', 'freebies', 'Freethought', 'Frugal', 'frugalmalefashion', 'funny', 'futurama', 'gadgets', 'GameDeals', 'gamedev', 'gameofthrones', 'gamernews', 'Games', 'gaming', 'gardening', 'gaymers', 'geek', 'GeekPorn', 'gentlemanboners', 'GetMotivated', 'gif', 'gifs', 'ginger', 'girlsinyogapants', 'GirlswithGlasses', 'gonewild', 'GoneWildPlus', 'google', 'Graffiti', 'Green', 'Guildwars2', 'Guitar', 'guns', 'happy', 'hardware', 'harrypotter', 'Health', 'HIMYM', 'hiphopheads', 'history', 'HistoryPorn', 'hockey', 'Homebrewing', 'horror', 'Hotchickswithtattoos', 'howto', 'HumanPorn', 'humor', 'IAmA', 'IDAP', 'iiiiiiitttttttttttt', 'IndieGaming', 'investing', 'ipad', 'iphone', 'itookapicture', 'IWantOut', 'IWantToLearn', 'japan', 'javascript', 'Jazz', 'jobs', 'Jokes', 'keto', 'LadyBoners', 'law', 'leagueoflegends', 'learnprogramming', 'lectures', 'LegalTeens', 'lego', 'lgbt', 'Libertarian', 'LifeProTips', 'linguistics', 'linux', 'listentothis', 'lists', 'literature', 'lolcats', 'LosAngeles', 'loseit', 'lost', 'LucidDreaming', 'MachinePorn', 'magicTCG', 'malefashionadvice', 'MapPorn', 'Marijuana', 'mashups', 'masseffect', 'math', 'Meditation', 'meetup', 'MensRights', 'Metal', 'milf', 'Military', 'Minecraft', 'MMA', 'modnews', 'motorcycles', 'moviecritic', 'movies', 'Music', 'mw3', 'mylittlepony', 'nba', 'NetflixBestOf', 'netsec', 'newreddits', 'news', 'nfl', 'nosleep', 'nostalgia', 'nsfw', 'nsfw2', 'nsfw_gifs', 'NSFW_nospam', 'nyc', 'obama', 'occupywallstreet', 'O_Faces', 'offbeat', 'OneY', 'OnOff', 'opendirectories', 'opensource', 'Paleo', 'Paranormal', 'Parenting', 'passionx', 'personalfinance', 'Pets', 'philosophy', 'PhilosophyofScience', 'photography', 'photos', 'PHP', 'Physics', 'pics', 'Pictures', 'pokemon', 'politics', 'pornvids', 'Portal', 'Portland', 'PostCollapse', 'productivity', 'programming', 'progressive', 'ProjectEnrichment', 'ProjectReddit', 'proper', 'PS3', 'psychology', 'Psychonaut', 'Python', 'quotes', 'QuotesPorn', 'ragenovels', 'Random_Acts_Of_Pizza', 'randomsexiness', 'reactiongifs', 'RealGirls', 'recipes', 'reddit.com', 'RedditThroughHistory', 'redheads', 'relationship_advice', 'relationships', 'religion', 'ReverseEngineering', 'ronpaul', 'RoomPorn', 'rpg', 'ruby', 'running', 'science', 'scifi', 'Seattle', 'secretsanta', 'seduction', 'self', 'SelfSufficiency', 'sex', 'Sexy', 'ShitRedditSays', 'shittyadvice', 'shittyaskscience', 'shutupandtakemymoney', 'skeptic', 'skyrim', 'soccer', 'socialism', 'software', 'somethingimade', 'SOPA', 'space', 'spacedicks', 'spaceporn', 'SpideyMeme', 'sports', 'StandUpComedy', 'starcraft', 'startrek', 'startups', 'StarWars', 'SubredditDrama', 'subredditoftheday', 'SuicideWatch', 'swtor', 'sysadmin', 'talesfromtechsupport', 'tattoos', 'technology', 'techsupport', 'teen_girls', 'television', 'Terraria', 'tf2', 'TheoryOfReddit', 'theredditor', 'thewalkingdead', 'thick', 'tipofmytongue', 'tldr', 'todayilearned', 'toosoon', 'TopGear', 'toronto', 'trackers', 'trance', 'travel', 'treecomics', 'trees', 'TrollXChromosomes', 'truegaming', 'TrueReddit', 'TwoXChromosomes', 'Ubuntu', 'unitedkingdom', 'UniversityofReddit', 'vegan', 'vertical', 'video', 'videos', 'VillagePorn', 'vinyl', 'voluptuous', 'wallpaper', 'wallpapers', 'waterporn', 'WeAreTheMusicMakers', 'webcomics', 'web_design', 'webdev', 'WebGames', 'wicked_edge', 'WikiLeaks', 'wikipedia', 'windows', 'windowshots', 'woahdude', 'women', 'worldnews', 'worldpolitics', 'worstof', 'wow', 'writing', 'WTF', 'xbox360', 'xkcd', 'Xsmall', 'YouShouldKnow', 'zelda', 'ZenHabits', 'zombies']

def run():
    r = reddit.Reddit("hackny_bot")
    r.login("bzzzz3","bzzzz")
    for sub in SUBS_LIST:
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
        print com.body
        print
    else:
        print (process_comments(com.comments))

if __name__ == "__main__":
    run()
