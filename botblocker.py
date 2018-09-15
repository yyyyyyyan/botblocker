import tweepy
from huepy import *
from botometer import Botometer
from configparser import ConfigParser
from collections import namedtuple
from math import floor
from settings import config_complete_path
from settings import initial_config, user_config
from errors import error, clear_errors

def initialize():
    config = ConfigParser()
    config.read(config_complete_path)
    if 'Error' in config and config['Error']['LastRun']:
        print('My last run exited with an error. Do you wish to reconfigure API settings?')
        reconfigure = input(green('(Y)es') + '/' + red('(N)o') + ': ')
        if reconfigure.upper().startswith('Y'):
            initial_config(config_complete_path)
        clear_errors()
    if 'API' not in config:
        print('It seems this is the first time you\'re running botblocker! First of all, let\'s set things up.')
        initial_config(config_complete_path)

def get_followers(api, username):
    followers = []
    try:
        for ids in tweepy.Cursor(api.followers_ids, screen_name=username).items():
            followers.extend(ids)
    except tweepy.TweepError:
        error('Failed to retrieve your Twitter followers.')
    return followers

def create_botometer(access_token, access_secret, mashape_key)
    try:
        bom = Botometer(wait_on_rate_limit=True, mashape_key=mashape_key, access_token=access_token, access_token_secret=access_secret)
    except tweepy.TweepError:
        error('Failed to connect to Botometer API')
    return bom

def get_block_settings(msg):
    print(msg)
    block_while = input(green('(Y)es') + '/' + red('(N)o') + ': ').upper().startswith('Y')
    soft_block = False
    if block_while:
        print('Should I only soft block accounts identified as bots?')
        soft_block = input(green('(Y)es') + '/' + red('(N)o') + ': ').upper().startswith('Y')

def identify_bots(api, bom, followers, block=False)
    block_levels = {3:2.5, 2:3, 1:4}
    colors = {0:lightblue, 1:lightgreen, 2:yellow, 3:orange, 4:red}
    bots = {}
    for id_number, result in bom.check_accounts_in(followers):
        score = result['display_scores']['universal']
        color = colors[floor(score - 0.0001)]
        if score > block_levels.get(block.level, 5):
            bots[result['user']['screen_name']] = score
            if block.block_while:
                block_bot(api, id_number, block.soft_block, block.report_spam)

def block_bot(api, bot_id, soft_block=False, report_spam=False):
    api.report_spam(user_id=bot_id) if report_spam else api.create_block(user_id=bot_id)
    if soft_block:
        api.destroy_block(user_id=bot_id)

def main():
    initialize()
    config = ConfigParser()
    config.read(config_complete_path)
    auth = tweepy.OAuthHandler(config['API'].get('ConsumerKey', None), config['API'].get('ConsumerSecret', None))
    username = input('Type in the username you want botblocker to use: ')
    if username in config:
        access_token = config[username].get('AccessToken', None)
        access_secret = config[username].get('AccessSecret', None)
    else:
        print('The username inputted was not found in my registry. Let\'s configure it!')
        access_token, access_secret = user_config(config_complete_path, auth)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    followers = get_followers(api, username)
    
    bom = create_botometer(access_token, access_secret, config['API'].get('MashapeKey', None))
    get_block_settings('Do you want me to block the account as soon as I identify it as a bot? ' + green('(Recommended)'))
    
    Block = namedtuple('Block', ['block_now', 'soft_block', 'report_spam'])
    block
