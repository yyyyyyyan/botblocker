import argparse
import tweepy
from huepy import bad, good
from os.path import join as pathjoin
from platform import system
from configparser import ConfigParser
from .settings import config_path, config_complete_path
from .settings import initial_config, user_config, confirm
from .errors import clear_errors
from .botblocker import get_followers, filter_followers, create_botometer
from .botblocker import identify_bots, Block, block_bots, add_to_allowlist

parser = argparse.ArgumentParser(description='Python program to identify and block your bot followers on Twitter')
parser.add_argument('-c', '--config', action='store_true', help='(Re)configure usage settings')
parser.add_argument('--noblock', action='store_false', help='Don\'t block anyone')
parser.add_argument('--saveallowlist', action='store_true', help='Save users identified as non-bots to an allowlist')
parser.add_argument('--softblock', action='store_true', help='Do soft block (block and unblock right after)')
parser.add_argument('-r', '--report', action='store_true', help='Report users identified as bots to Twitter')
parser.add_argument('-l', '--level', action='store', type=int, choices=range(1,4), default=2, help='Level of rigorosity to use to identify bots (2 is recommended)')
parser.add_argument('-u', '--user', action='store', required=True, help='The Twitter username you want to run botblocker for')
parser.add_argument('-v', '--version', action='version', help='Version', version='1.1.3')
args = parser.parse_args()

if system() == 'Windows':
    import colorama
    colorama.init()

def check_settings():
    config = ConfigParser()
    config.read(config_complete_path)
    if 'Error' in config and config['Error']['LastRun']:
        print('My last run exited with an error. Do you wish to reconfigure API settings?')
        if confirm():
            initial_config(config_complete_path)
        clear_errors(config_complete_path)
    if 'API' not in config:
        print('It seems this is the first time you\'re running botblocker! First of all, let\'s set things up.')
        initial_config(config_complete_path)
        
def main():
    if args.config:
        initial_config(config_complete_path)
    check_settings()

    config = ConfigParser()
    config.read(config_complete_path)

    auth = tweepy.OAuthHandler(config['API'].get('ConsumerKey', None), config['API'].get('ConsumerSecret', None))
    username = args.user
    if username in config:
        access_token = config[username].get('AccessToken', None)
        access_secret = config[username].get('AccessSecret', None)
    else:
        print('The username inputted was not found in my registry. Let\'s configure it!')
        access_token, access_secret = user_config(config_complete_path, auth)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    twitter_api_auth = {
    'consumer_key': auth.consumer_key,
    'consumer_secret': auth.consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_secret,
    }
    bom = create_botometer(config['API'].get('MashapeKey', None), twitter_api_auth)
    
    allowlist_path = config['Global'].get('AllowListPath', pathjoin(config_path, 'AllowList.pickle'))
    followers = filter_followers(allowlist_path, get_followers(api, username))

    level = args.level
    while_block = Block(args.noblock, args.softblock, args.report)
    bots, non_bots = identify_bots(api, bom, followers, level, while_block)
    if not while_block.block_now:
        print('Should I block accounts identified as bots now?')
        post_block = Block(confirm(), args.softblock, args.report)
        block_bots(api, bots, post_block)

    if while_block.block_now or post_block.block_now:
        print(bad('{} bot accounts blocked!'.format(len(bots))))
    
    if args.saveallowlist:
        add_to_allowlist(allowlist_path, non_bots)
        print(good('{} non-bot accounts added to the allowlist!'.format(len(non_bots))))

if __name__ == '__main__':
    main()