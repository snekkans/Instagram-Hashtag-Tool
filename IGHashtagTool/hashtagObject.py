class HashtagObj:
    def __init__(self, name, post_count, last_two_days_posts, last_day_posts, last_month_posts):
        self.name = name
        self.postCount = post_count
        self.last2DaysPosts = last_two_days_posts
        self.lastDayPosts = last_day_posts
        self.lastMonthPosts = last_month_posts

    def getName(self):
        return self.name

    def getPostCount(self):
        return self.postCount

    def get2DaysPosts(self):
        return self.last2DaysPosts

    def setLast2DaysPosts(self, newNum):
        self.last2DaysPosts = newNum

    def getDayPosts(self):
        return self.lastDayPosts

    def setDayPosts(self, newNum):
        self.lastDayPosts = newNum

    def getMonthPosts(self):
        return self.lastMonthPosts

    def setMonthPosts(self, newNum):
        self.lastMonthPosts = newNum
