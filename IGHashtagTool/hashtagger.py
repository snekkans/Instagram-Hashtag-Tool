# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from itertools import takewhile
from tkinter.messagebox import showinfo

import instaloader
import hashtagObject
from collections import Counter
from datetime import datetime, timedelta
from instaloader import Hashtag
from tkinter import *

L = instaloader.Instaloader()
# hashtag = Hashtag.from_name(L.context, "rafmminiatures")

rawHashtagList = []
masterHashtagList = []
countedHashtags = []

lastMonth = datetime.utcnow() - timedelta(days=30)
last48 = datetime.utcnow() - timedelta(days=2)
last24 = datetime.utcnow() - timedelta(days=1)


def generate_hashtags(min_posts, max_posts, hashtag, posts):
    global lastMonth, last48, last24
    print(hashtag.mediacount, "total posts for hashtag", hashtag.name, "\n")  # counts all posts in hashtag
    print("Begin finding relevant posts\n")
    # get posts in timeframe
    for post in takewhile(lambda p: p.date_utc > lastMonth, posts):
        # L.download_post(post, target='#' + hashtag.name)
        print(post.date_utc, lastMonth, lastMonth < post.date_utc)
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
            new_tag = hashtagObject.HashtagObj(h.name, count, 0, 0, 0)
            nposts = L.get_hashtag_posts(new_tag.getName())
            # if the count's not in the range
            if max_posts <= count or min_posts >= count:
                print(i + " NOT in range", count)
            else:
                print(i + " IS in range", count)
                try:
                    print("Begin getting posts from last 48 hours for", new_tag.getName())
                    temp = 0
                    for post in takewhile(lambda p: p.date_utc > last48, nposts):
                        print(post.date_utc, last48, last48 < post.date_utc)
                        temp += 1
                    print("Found", temp, "posts for", new_tag.getName(), 'over 48 hours ')
                    new_tag.setLast2DaysPosts(temp)
                except:
                    print("Error getting posts over last 48 hours for", new_tag.getName())

                countedHashtags.append(new_tag)
        except:
            print("Can't find hashtag", i)
    print("\nFinished filtering hashtags by post count with", len(countedHashtags), "results\n")

    for i in countedHashtags:
        print(i.getName(), i.getPostCount(), i.getRecentPosts())


def test():
    global countedHashtags
    min_posts = int(entry_min.get())
    max_posts = int(entry_max.get())
    hashtag = Hashtag.from_name(L.context, str(entry_hashtag.get()))
    posts = L.get_hashtag_posts(hashtag.name)

    # run code
    generate_hashtags(min_posts, max_posts, hashtag, posts)
    popup_showinfo(countedHashtags)


def popup_showinfo(items):
    log = "Hashtag | Total Posts | 48 Hours Posts\n"
    for i in items:
        log += str(i.getName()) + " | " + str(i.getPostCount()) + " | " + str(i.get2DaysPosts()) + "\n"
    showinfo("Hashtagger", log)


root = Tk()
root.geometry("320x240")
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

label_hashtag = Label(frame, text="Hashtag to Use")
label_hashtag.pack()

entry_hashtag = Entry(frame, width=20)
entry_hashtag.insert(0, 'rafmminiatures')
entry_hashtag.pack(padx=5, pady=5)

button_start = Button(frame, text="Get Hashtags", command=test)
button_start.pack()

label_log = Label(frame, text="Enter your values and press the start button!")
label_log.pack()

root.title("Hashtagger")
root.mainloop()
