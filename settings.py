from os.path import expanduser, join as pathjoin
import pyperclip
from configparser import ConfigParser
from huepy import *

config_path = expanduser('~')
config_file = '.botblocker'
config_complete_path = pathjoin(config_path, config_file)

def initial_config(config_complete_path):
    config = ConfigParser() 
    consumer_key = input('Paste your Twitter API Consumer Key: ')
    consumer_secret = input('Paste your Twitter API Consumer Secret Key: ')
    mashape_key = input('Paste your Mashape API Key: ')
    config['API'] = {'ConsumerKey':consumer_key, 'ConsumerSecret':consumer_secret, 'MashapeKey':mashape_key}
    
    with open(config_complete_path, 'w') as configfile:
        config.write(configfile)

def user_config(config_complete_path, auth):
    config = ConfigParser()
    config.read(config_complete_path)
    username = input('Type in your Twitter username: ')

    try:
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        error('Failed to get request token.')

    print('Access this link to authorize usage of your Twitter account: ' + bold(lightpurple(auth_url)) + ' (URL automatically copied to clipboard)')
    pyperclip.copy(auth_url)
    verifier = input('Type in the verifier code available on the authorization link: ')

    try:
        access_token, access_secret = auth.get_access_token(verifier)
    except tweepy.TweepError:
        error('Failed to get access token.')

    config[username] = {'AccessToken':access_token, 'AccessSecret':access_secret}
    with open(config_complete_path, 'w') as configfile:
        config.write(configfile)
    return access_token, access_secret