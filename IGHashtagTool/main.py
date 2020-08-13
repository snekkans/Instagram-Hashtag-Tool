# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from itertools import takewhile
import instaloader
import hashtagObject
from collections import Counter
from datetime import datetime, timedelta
from instaloader import Hashtag
from tkinter import *

# MIN_POSTS = 14999
# MAX_POSTS = 60001

L = instaloader.Instaloader()
# hashtag = Hashtag.from_name(L.context, "rafmminiatures")

rawHashtagList = []
masterHashtagList = []
countedHashtags = []
tempFiltered = []


# get all posts given a hashtag

# last = datetime.utcnow() - timedelta(days=30)
# recent = datetime.utcnow() - timedelta(days=2)

# posts = L.get_hashtag_posts(hashtag.name)


def generate_hashtags(min_posts, max_posts, last, recent, hashtag, posts):
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
    for i in hashtags:
        try:
            h = Hashtag.from_name(L.context, i)
            count = h.mediacount
            # if the count's not in the range
            if max_posts <= count or min_posts >= count:
                print(i + " NOT in range", count)
            else:
                print(i + " IS in range", count)
                tempFiltered.append(h)
                newTag = hashtagObject.HashtagObj(h.name, count, 0)
                countedHashtags.append(newTag)
        except:
            print("Can't find hashtag", i)
    print("\nFinished filtering hashtags by post count with", len(countedHashtags), "results\n")
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
            print("Can't find Counted Hashtag", i)
    for i in countedHashtags:
        print(i.getName(), i.getPostCount(), i.getRecentPosts())


def test():
    print("pressed button")
    # set values
    min_posts = int(entry_min.get())
    max_posts = int(entry_max.get())
    timeframe = int(entry_days.get())
    last = datetime.utcnow() - timedelta(days=int(timeframe))
    recent_timeframe = int(entry_recent_days.get())
    recent = datetime.utcnow() - timedelta(days=int(recent_timeframe))
    hashtag = Hashtag.from_name(L.context, str(entry_hashtag.get()))
    posts = L.get_hashtag_posts(hashtag.name)

    print(min_posts, max_posts, last, recent, hashtag)

    # run code
    #generate_hashtags(min_posts, max_posts, last, recent, hashtag, posts)


root = Tk()
root.geometry("640x480")
frame = Frame(root)
frame.pack()

label_min = Label(frame, text="Minimum Posts")
label_min.pack()

entry_min = Entry(frame, width=20)
entry_min.insert(0, '50000')
entry_min.pack(padx=5, pady=5)

label_max = Label(frame, text="Maximum Posts")
label_max.pack()

entry_max = Entry(frame, width=20)
entry_max.insert(0, '100000')
entry_max.pack(padx=5, pady=5)

label_days = Label(frame, text="Days before today")
label_days.pack()

entry_days = Entry(frame, width=20)
entry_days.insert(0, '30')
entry_days.pack(padx=5, pady=5)

label_recent_post_days = Label(frame, text="Days of Active Posts")
label_recent_post_days.pack()

entry_recent_days = Entry(frame, width=20)
entry_recent_days.insert(0, '2')
entry_recent_days.pack(padx=5, pady=5)

label_hashtag = Label(frame, text="Hashtag to Use")
label_hashtag.pack()

entry_hashtag = Entry(frame, width=20)
entry_hashtag.insert(0, 'rafmminiatures')
entry_hashtag.pack(padx=5, pady=5)

button_start = Button(frame, text="Get Hashtags", command=test)
button_start.pack()

root.title("Hashtagger")
root.mainloop()
