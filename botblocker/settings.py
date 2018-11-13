import tweepy
import pyperclip
from os.path import expanduser, join as pathjoin
from configparser import ConfigParser
from huepy import *
from .errors import error

config_path = expanduser('~')
config_file = '.botblocker'
config_complete_path = pathjoin(config_path, config_file)

def initial_config(config_complete_path):
    config = ConfigParser()
    print('Paste your ' + blue('Twitter API Consumer Key') + ': ', end='')
    consumer_key = input()
    print('Paste your ' + blue('Twitter API Consumer Secret Key') + ': ', end='')
    consumer_secret = input()
    print('Paste your ' + blue('Mashape API Key' + ': '), end='')
    mashape_key = input()
    config['API'] = {'ConsumerKey':consumer_key, 'ConsumerSecret':consumer_secret, 'MashapeKey':mashape_key}

    allowlist_path = pathjoin(input('Type in the full path of the folder you want to save your allowlist: '), 'AllowList.pickle')
    config['Global'] = {'AllowListPath':allowlist_path}

    with open(config_complete_path, 'w') as configfile:
        config.write(configfile)

def user_config(config_complete_path, auth):
    config = ConfigParser()
    config.read(config_complete_path)
    username = input('Type in your Twitter username: ')

    try:
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        error(config_complete_path, 'Failed to get request token.')

    msg_auth_link = 'Access this link to authorize usage of your Twitter account: ' + bold(lightpurple(auth_url))
    if(pyperclip.is_available()):
        msg_auth_link += ' (URL automatically copied to clipboard)'
        pyperclip.copy(auth_url)
    print(msg_auth_link)
    verifier = input('Type in the verifier code available on the authorization link: ')

    try:
        access_token, access_secret = auth.get_access_token(verifier)
    except tweepy.TweepError:
        error(config_complete_path, 'Failed to get access token.')

    config[username] = {'AccessToken':access_token, 'AccessSecret':access_secret}
    with open(config_complete_path, 'w') as configfile:
        config.write(configfile)
    return access_token, access_secret

def confirm():
    print(green('(Y)es') + '/' + red('(N)o') + ': ', end='')
    result = input().upper().startswith('Y')
    return result