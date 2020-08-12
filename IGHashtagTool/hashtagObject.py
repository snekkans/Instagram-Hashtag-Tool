class HashtagObj:
    def __init__(self, name, postCount,recentPosts):
        self.name = name
        self.postCount = postCount
        self.recentPosts=recentPosts

    def getName(self):
        return self.name

    def getPostCount(self):
        return self.postCount

    def getRecentPosts(self):
        return self.recentPosts

    def setRecentPosts(self,newNum):
        self.recentPosts=newNum
