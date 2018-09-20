import tweepy
import pickle
from huepy import *
from datetime import datetime
from collections import namedtuple
from math import floor
from botometer import Botometer
from .settings import config_complete_path
from .errors import error

def get_followers(api, username):
    followers = []
    try:
        for ids in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
            followers.extend(ids)
    except tweepy.TweepError:
        error(config_complete_path, 'Failed to retrieve your Twitter followers.')
    return followers

def filter_followers(location, followers):
    try:
        with open(location, 'rb') as allowlist:
            allowed_ids = pickle.load(allowlist)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        allowed_ids = []

    filtered_followers = [f for f in followers if f not in allowed_ids]
    return filtered_followers

def create_botometer(mashape_key, twitter_api_auth):
    try:
        bom = Botometer(wait_on_rate_limit=True, mashape_key=mashape_key, **twitter_api_auth)
    except tweepy.TweepError:
        error(config_complete_path, 'Failed to connect to Botometer API')
    return bom

def calculate_bot_score(api, id_number):
    parameters = {
    'followers_count': lambda user: user.followers_count <= 25,
    'created_at': lambda user: (datetime.now() - user_info.created_at).days < 31,
    'default_profile': lambda user: user.default_profile,
    'default_profile_image': lambda user: user.default_profile_image,
    'screen_name': lambda user: sum(c.isdigit() for c in user.screen_name) > 5
    }
    score = 0
    try:
        user_info = api.get_user(user_id=id_number)
    except tweepy.TweepError:
        return id_number, -1
    return user_info.screen_name, sum(parameters[p](user_info) for p in parameters)

Block = namedtuple('Block', ['block_now', 'soft_block', 'report_spam'])
def identify_bots(api, bom, followers, level, block=Block(False, False, False)):
    print(lightcyan('\nAnalizing followers...'))
    block_levels = {3:2.5, 2:3, 1:4}
    colors = {0:lightblue, 1:lightgreen, 2:yellow, 3:orange, 4:red, 5:red}
    bots = []
    non_bots = []
    try:
        for i, account in enumerate(bom.check_accounts_in(followers), 1):
            id_number, result = account
            if result.get('error'):
                screen_name, score = calculate_bot_score(api, id_number)
            else:
                screen_name = result['user']['screen_name']
                score = result['display_scores']['universal']
            color = colors.get(floor(score), white)
            print(str(i) + color(' {} - {}'.format(screen_name, score)))
            if score >= block_levels.get(level, 3):
                bots.append(screen_name)
                if block.block_now:
                    block_bot(api, id_number, block.soft_block, block.report_spam)
                    print(bad('Blocked'))
            elif score < 2.5:
                non_bots.append(id_number)
    except KeyboardInterrupt:
        print(red('\nInterrupted\n'))
    return bots, non_bots

def block_bot(api, bot_id, soft_block=False, report_spam=False):
    api.report_spam(user_id=bot_id) if report_spam else api.create_block(user_id=bot_id)
    if soft_block:
        api.destroy_block(user_id=bot_id)

def block_bots(api, bots, block=Block(False, False, False)):
    if block.block_now:
        for user_id in bots:
                block_bot(api, user_id, block.soft_block, block.report_spam)

def add_to_allowlist(location, user_ids):
    allowlist = open(location, 'w+b')
    try:
        allowed_ids = pickle.load(allowlist)
        allowed_ids.update(user_ids)
    except (EOFError, pickle.UnpicklingError):
        allowed_ids = set(user_ids)
    pickle.dump(allowed_ids, allowlist, pickle.HIGHEST_PROTOCOL)
    allowlist.close()