import argparse
import yaml
import random
import os
import sys

from mastodon import Mastodon

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Super-hyper-awesome mastodon image posting bot")
    parser.add_argument('--config', dest='configpath', action='store', default='config.yaml', help="Path to config file")
    parser.add_argument('--message', dest='message', action='store', default=False, help="Send a message to the bot's followers")
    parser.add_argument('--create', dest='create', action='store_const', const=True, default=False, help="RUN ONLY ONCE, get the credentials file from the server")
    
    args = parser.parse_args()
    
    try:
        configfile = open(args.configpath, 'r')
    except IOError, e:
        print("Config file not found, exiting!")
        sys.exit(1)
    config = yaml.load(configfile.read())
    
    if not os.path.exists(config['clientcred']):
        if(args.create == True):
            Mastodon.create_app(
                config['botname'],
                to_file=config['clientcred'])
        else:
            print "Credential file not found, exiting!"
            sys.exit(1)
    
    mastodon = Mastodon(client_id=config['clientcred'])
    mastodon.log_in(config['username'],
                    config['password'],
                    to_file=config['usercred'])
    
    m = Mastodon(client_id=config['clientcred'],
                 access_token=config['usercred'])
    
    if(args.message != False):
        # Sending a message
        m.status_post(args.message)
    else:
        # Normal behavior
        try:
            imglist = os.listdir(config['images'])
            choice = random.choice(imglist)
            posttext = random.choice(config['posttext'])
            media_dict = m.media_post(os.path.join('catboys/', choice))
            m.status_post(posttext, media_ids=[media_dict,], sensitive=False)
        except IOError, e:
            print("Could not open image directory, exiting!")
            sys.exit(1)
