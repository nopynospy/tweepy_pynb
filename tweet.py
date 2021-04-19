import tweepy
from textblob import TextBlob
from datetime import datetime
import csv
import os.path
from dotenv import load_dotenv

def tweet_func(csvname="tweet.csv", query="Malaysia"):
    load_dotenv()
    auth = tweepy.OAuthHandler(os.getenv('OAUTH_KEY'),os.getenv('OAUTH_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_KEY'),os.getenv('ACCESS_SECRET'))
    api = tweepy.API(auth)
    public_tweets = api.search(query)
    total_polarity = 0
    total_subjectivity = 0
    tweet_dict = {
    "query": query,
    "time": datetime.now()
    }
    analysis_number = 0
    for tweet in public_tweets:
        analysis=TextBlob(tweet.text)
        total_polarity += analysis.sentiment.polarity
        total_subjectivity += analysis.sentiment.subjectivity
        analysis_number+=1
    tweet_dict["total_polarity"] = total_polarity/analysis_number
    tweet_dict["total_subjectivity"] = total_subjectivity/analysis_number
    print("Added to " + 'tweet.csv')
    file_exists = os.path.isfile(csvname)

    with open (csvname, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=list(tweet_dict.keys()))

        if not file_exists or os.stat(csvname).st_size == 0:
            writer.writeheader()

        writer.writerow(tweet_dict)

if __name__ == "__main__": 
    tweet_func() 
