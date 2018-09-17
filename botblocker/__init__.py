import tweepy
from huepy import *
from os.path import join as pathjoin
from botometer import Botometer
from configparser import ConfigParser
from .settings import config_path, config_complete_path
from .settings import initial_config, user_config, confirm
from .errors import error, clear_errors
from .botblocker import get_followers, create_botometer, add_to_allowlist
from .botblocker import identify_bots, Block, block_bot, block_bots

def check_settings():
    config = ConfigParser()
    config.read(config_complete_path)
    if 'Error' in config and config['Error']['LastRun']:
        print('My last run exited with an error. Do you wish to reconfigure API settings?')
        if confirm():
            initial_config(config_complete_path)
        clear_errors()
    if 'API' not in config:
        print('It seems this is the first time you\'re running botblocker! First of all, let\'s set things up.')
        initial_config(config_complete_path)
        
def get_block_settings(msg):
    soft_block = False
    report_spam = False
    print(msg)
    block_now = confirm()
    if block_now:
        print('Should I only soft block accounts identified as bots?')
        soft_block = confirm()
        print('Should I report accounts identified as bots to Twitter?')
        report_spam = confirm()
    return Block(block_now, soft_block, report_spam)

def main():
    check_settings()
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
    twitter_api_auth = {
    'consumer_key': auth.consumer_key,
    'consumer_secret': auth.consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_secret,
    }
    bom = create_botometer(config['API'].get('MashapeKey', None), twitter_api_auth)
    followers = get_followers(api, username)

    print('What level of rigorosity should I use to identify bots?')
    try:
        level = int(input('1/2 - {}/3: '.format(green('Recommended'))))
    except ValueError:
        print(red('Invalid value for rigorosity level. Changing it to 2...'))
        level = 2

    while_block = get_block_settings('Do you want me to block the account as soon as I identify it as a bot? ' + green('(Recommended)'))
    bots, non_bots = identify_bots(api, bom, followers, level, while_block)
    if not while_block.block_now:
        post_block = get_block_settings('Do you want me to block all accounts identifieds as bots? ' + green('(Recommended)'))
        block_bots(api, bots, post_block)
    if while_block.block_now or post_block.block_now:
        print(bad('{} bot accounts blocked!'.format(len(bots))))
    print('Do you want to add the accounts identified as non-bots in an allowlist?')
    if confirm():
        allowlist_path = config[username].get('AllowListPath', pathjoin(config_path, 'AllowList.pickle'))
        add_to_allowlist(allowlist_path, non_bots)
        print(good('{} non-bot accounts added to the allowlist!'.format(len(non_bots))))