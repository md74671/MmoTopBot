﻿import praw
import string
import OAuth2Util


subreddits = list()
r = praw.Reddit('Top MMORPG post aggregator by /u/SadDragon')

# Setup Authentication
o = OAuth2Util.OAuth2Util(r)
o.refresh(force=True)


# Get MMORPG sidebar info
sidebar =  r.get_subreddit('mmorpg').description.split('\n')

# Grab popular MMO list
index = 0
start = False
for line in sidebar:
    if line == '###**Popular MMO Subreddits**':
        start = True
        continue
    if start and line != '':
        loc = line.index('/r/') + 3
        subreddits.append(line[loc:-1])
        index += 1 
    if start and line == '' and len(subreddits) > 0:
        start = False
        break

print('Creating output...');

output = 'Greetings adventurers!\n\nI have compiled a list of all the top posts from last week for all of the popular MMO subreddits in the sidebar. It may be news or it may be fluff but its all here in one place!\n\n'
output += 'Subreddit | Top Post Last Week | Points\n---|---|---\n'
# Loop through subreddits and get top week
for sub in subreddits:
    submissions = r.get_subreddit(sub).get_top_from_week(limit=1)
    for post in submissions:
        output += '/r/{0} | [{1}]({2}) | {3}\n'.format(sub, post.title, post.url, post.score)
    
output += '\n\n---\n\n I am a bot and this is an automated post. Please direct any questions to the mods via modmail.\n\n*beep boop*'

print('Making post...');
r.submit('mmorpg','Top MMO posts last week, tonight!',output)
