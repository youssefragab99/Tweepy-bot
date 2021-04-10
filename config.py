import tweepy
from secrets import *
import logging


logger = logging.getLogger()

def create_api():
    api_key = keys[0]
    api_secret_key = keys[1]
    access_token = keys[2]
    access_token_secret = keys[3]

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
                        wait_on_rate_limit_notify=True)
    try: 
        api.verify_credentials()
    except Exception as e: 
        logger.error('Error creating API', exc_info= True)
        raise e
    logger.info('API created')
    return api

