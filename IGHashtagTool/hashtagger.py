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
L.login("","")
# hashtag = Hashtag.from_name(L.context, "rafmminiatures")

rawHashtagList = []
masterHashtagList = []
countedHashtags = []

lastUsedHashtag = ""

lastMonth = datetime.utcnow() - timedelta(days=30)
last48 = datetime.utcnow() - timedelta(days=2)
last24 = datetime.utcnow() - timedelta(days=1)
retrieved_data = False

def generate_hashtags(min_posts, max_posts, hashtag, posts):
    global lastMonth, last48, last24, retrieved_data, button_start, lastUsedHashtag
    lastUsedHashtag = hashtag.name
    retrieved_data = False
    print(hashtag.mediacount, "total posts for hashtag", hashtag.name, "\n")  # counts all posts in hashtag
    print("Begin finding relevant posts\n")
    # get hashtags for all posts in the last month
    for post in takewhile(lambda p: p.date_utc > lastMonth, posts):
        # L.download_post(post, target='#' + hashtag.name)
        print(post.date_utc, lastMonth, lastMonth < post.date_utc)
        rawHashtagList.append(post.caption_hashtags)
    print("Finished finding relevant posts!\n")
    print("Begin generating hashtag list\n")
    # filter out repeated hashtags and get a proper list out of it
    for i in rawHashtagList:
        for j in i:
            masterHashtagList.append(j)

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

            new_tag = hashtagObject.HashtagObj(h.name, count, 0, 0, 0)
            # post counting hypothetically goes here
            countedHashtags.append(new_tag)

            if max_posts <= count or min_posts >= count:
                print(i + " NOT in range", count)
            else:
                print(i + " IS in range", count)

                #check all top posts here before adding to counted hashtags

                new_tag = hashtagObject.HashtagObj(h.name, count, 0, 0, 0)
                countedHashtags.append(new_tag)
        except:
            print("Can't find hashtag", i)
    print("\nFinished filtering hashtags by post count with", len(countedHashtags), "results\n")

    #in this for loop, don't count the number of posts per set of hours
    #instead, do this:
    #for each hashtag in the counted hashtags
    #go through top posts in that hashtag
        #for each of those posts, check if it was made in the last n hours
        #if it was, add it to the new list, otherwise discard it
    #TODO: see above on how to restructure this for loop

    # actual post counting starts here
    for i in countedHashtags:
        try:
            # print("Begin getting posts from last 24 hours for", i.getName())
            temp = 0
            nposts = L.get_hashtag_posts(i.getName())
            for post in takewhile(lambda p: p.date_utc > last24, nposts):
                # print(post.date_utc, last24, last24 < post.date_utc)
                temp += 1
            print("Found", temp, "posts for", i.getName(), 'over 24 hours ')
            i.setDayPosts(temp)
        except:
            print("Error getting posts over last 24 hours for", i.getName())

        try:
            # print("Begin getting posts from last 48 hours for", i.getName())
            temp = 0
            nposts = L.get_hashtag_posts(i.getName())
            for post in takewhile(lambda p: p.date_utc > last48, nposts):
                # print(post.date_utc, last48, last48 < post.date_utc)
                temp += 1
            print("Found", temp, "posts for", i.getName(), 'over 48 hours ')
            i.setLast2DaysPosts(temp)
        except:
            print("Error getting posts over last 48 hours for", i.getName())

        try:
            # print("Begin getting posts from last month for", i.getName())
            temp = 0
            nposts = L.get_hashtag_posts(i.getName())
            for post in takewhile(lambda p: p.date_utc > lastMonth, nposts):
                # print(post.date_utc, last48, last48 < post.date_utc)
                temp += 1
            print("Found", temp, "posts for", i.getName(), 'over last month')
            i.setMonthPosts(temp)
        except:
            print("Error getting posts over last month for", i.getName())
    retrieved_data = True


def get_hashtags_in_range(min_posts, max_posts):
    temp_array = []
    for i in countedHashtags:
        if max_posts >= i.getPostCount() >= min_posts:
            temp_array.append(i)
            print(i.getName(), i.getPostCount(), i.getDayPosts(), i.get2DaysPosts(), i.getMonthPosts())
    return temp_array


def main():
    global countedHashtags
    try:
        min_posts = int(entry_min.get())
    except:
        showinfo("Error", "Enter a number for Minimum Posts")
    try:
        max_posts = int(entry_max.get())
    except:
        showinfo("Error", "Enter a number for Maximum Posts")
    if str(entry_hashtag.get()) == "" or not str(entry_hashtag.get()).isalnum():
        showinfo("Error", "Enter a valid Hashtag")
    elif max_posts<min_posts:
        showinfo("Error", "Minimum Posts must be less than Maximum Posts")
    else:
        hashtag = Hashtag.from_name(L.context, str(entry_hashtag.get()))
        posts = L.get_hashtag_posts(hashtag.name)
        # run code
        if not retrieved_data or lastUsedHashtag != str(entry_hashtag.get()):
            generate_hashtags(min_posts, max_posts, hashtag, posts)
        popup_showinfo(get_hashtags_in_range(min_posts, max_posts))


def popup_showinfo(items):
    log = "Hashtag | Total Posts | 24 Hours | 48 Hours | 30 Days\n"
    for i in items:
        log += str(i.getName()) + " | " + str(i.getPostCount()) + " | " + str(i.getDayPosts()) + " | " + str(
            i.get2DaysPosts()) + " | " + str(i.getMonthPosts()) + "\n"
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

button_start = Button(frame, text="Get Hashtags", command=main)
button_start.pack()

label_log = Label(frame, text="Enter your values and press the start button!")
label_log.pack()

root.title("Hashtagger")
root.mainloop()
