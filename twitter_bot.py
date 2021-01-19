import tweepy 
import datetime 
from  pandas import DataFrame
import logging 
import time
from config import create_api

api = create_api()

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()

user = api.me()

def publictweet(): 
    if datetime.date.today().weekday() == 0:
        tweettopublish = 'Hi everyone, today is Monday. Have an amazing week.'
    if datetime.date.today().weekday() == 1:
        tweettopublish = 'Today is Tuesday, also known as Champions league day'
    if datetime.date.today().weekday() == 2: 
        tweettopublish = 'Happy hump day'
    if datetime.date.today().weekday() == 3: 
        tweettopublish = 'Reminder, the weekend is coming'
    if datetime.date.today().weekday() == 4: 
        tweettopublish = 'TGIF'
    if datetime.date.today().weekday() == 5: 
        tweettopublish = 'Happy weekend everyone!'
    if datetime.date.today().weekday() == 6: 
        tweettopublish = 'Happy Grand Prix day! This will be right at least for some weeks'
    api.update_status(tweettopublish)
    

timeline = api.home_timeline()
def print_tweets_from_timeline():
    for tweet in timeline: 
        print(f'{tweet.user.name} said "{tweet.text}"\n')

print_tweets_from_timeline()

def get_user_info(x):
    user = api.get_user(x)
    print('User details:')
    print(user.name)
    print(user.description)
    print(user.location '\n')

    print('Last 20 followers:')
    for follower in user.followers():
        print(follower.name)

get_user_info('yragab99')


def get_followers_info(y):
    user_followers = api.get_user(y).followers()
    print(user_followers)


def extract_tweets(userid):
    all_tweets = []
    tweets = tweepy.Cursor(api.user_timeline,screen_name = userid, 
                            count = 200, 
                            tweet_mode = 'extended').items()
    all_tweets.extend(tweets)
    outtweets = [[tweet.id_str,
                  tweet.created_at,
                  tweet.favorite_count,
                  tweet.retweet_count,
                  tweet.full_text.encode('utf-8').decode('utf-8')]
                for idx, tweet in enumerate(all_tweets)]
    df = DataFrame(outtweets, columns =['id', 'created_at', 'favorite_count', 'retweet_count', 'text'])
    df.to_csv('%s_tweets.csv' % userid, index = False)


def retweeet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list: 
        search_query = f'{need_hashtags} -filter:retweets'
        tweets = api.search(q=search_query, lang = 'en', tweet_mode ='extended')
        for tweet in tweets: 
            hashtags = [i['text'].lower() for i in tweet.__dict__['entities']['hashtags']]
            try: 
                need_hashtags = [hashtag.strip('#') for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                for hashtag in set(hashtags):
                    if tweet.user.id != api.me().id:
                        status = api.get_status(tweet.id)
                        print(status)
                        #if api.retweeted():
                            #pass
                        #else:
                        api.retweet(tweet.id)
                        logger.info(f'Retweeted tweet from {tweet.user.name} saying: {tweet.full_text}')
                        time.sleep(5)
            except tweepy.TweepError as e:
                logger.error('Error on retweet', exc_info = True)
                print(e.reason)
    else:
        logger.error('Hashtag search terms need to be of type list', exc_info = True)
        return

