from sys import exit
from configparser import ConfigParser
from huepy import *

def error(config_complete_path, msg):
    config = ConfigParser()
    config.read(config_complete_path)
    config['Error'] = {'LastRun':True, 'LastMessage':msg}
    with open(config_complete_path, 'w') as configfile:
        config.write(configfile)
    print(red('Error! ' + msg))
    exit()

def clear_errors(config_complete_path):
    config = ConfigParser()
    config.read(config_complete_path)
    config['Error'] = {'LastRun':'', 'LastMessage':''}
    with open(config_complete_path, 'w') as configfile:
        config.write(configfile)