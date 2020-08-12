# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from itertools import takewhile

import instaloader
import hashtagObject

from collections import Counter
from datetime import datetime, timedelta
from instaloader import Hashtag

MIN_POSTS = 14999
MAX_POSTS = 60001

L = instaloader.Instaloader()
hashtag = Hashtag.from_name(L.context, "rafmminiatures")
rawHashtagList = []
masterHashtagList = []
# get all posts given a hashtag

last = datetime.utcnow() - timedelta(days=30)

posts = L.get_hashtag_posts(hashtag.name)
print(hashtag.mediacount, "total posts for hashtag", hashtag.name, "\n")  # counts all posts in hashtag
# for post in instaloader.Hashtag.from_name(L.context, 'legoleaks').get_posts():

print("Begin finding relevant posts\n")

# get posts in timeframe
for post in takewhile(lambda p: p.date_utc > last, posts):
    # L.download_post(post, target='#' + hashtag.name)
    print(post.date_utc, last, last < post.date_utc)
    rawHashtagList.append(post.caption_hashtags)

print("Finished finding relevant posts!\n")

print("Begin generating hashtag list\n")
# put all the items into one big list
for i in rawHashtagList:
    for j in i:
        masterHashtagList.append(j)

# artopportunitiesmonthly

c = Counter(masterHashtagList)
hashtags = list(c)

print("Finished generating hashtag list with", len(hashtags), "unique results\n")

print(hashtags, "\n")

print("Begin filtering hashtags by post count\n")

countedHashtags = []
tempFiltered = []

for i in hashtags:
    try:
        h = Hashtag.from_name(L.context, i)
        count = h.mediacount
        # if the count's not in the range
        if MAX_POSTS < count or MIN_POSTS > count:
            print(i + " NOT in range", count)
        else:
            print(i + " IS in range", count)
            tempFiltered.append(h)
            newTag = hashtagObject.HashtagObj(h.name, count, 0)
            countedHashtags.append(newTag)
    except:
        print("Can't find hashtag", i)

print("\nFinished filtering hashtags by post count with", len(countedHashtags), "results\n")

recent = datetime.utcnow() - timedelta(days=2)
for i in countedHashtags:
    try:
        print("Begin get posts for hashtag", i.getName() + "\n")
        temp = 0
        nposts = L.get_hashtag_posts(i.getName())
        for post in takewhile(lambda p: p.date_utc > recent, nposts):
            # L.download_post(post, target='#' + i.getName())
            print(post.date_utc, recent, recent < post.date_utc)
            temp += 1
        print("Finished getting posts for hashtag", i.getName() + "\n")
        i.setRecentPosts(temp)
    except:
        print("Can't find Counted Hashtag",i)

for i in countedHashtags:
    print(i.getName(), i.getPostCount(), i.getRecentPosts())
