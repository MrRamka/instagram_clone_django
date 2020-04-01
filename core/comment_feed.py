class FeedComment:
    def __init__(self, post, comment_list, has_more=False):
        self.post = post
        self.comment_list = comment_list
        self.has_more = has_more

    def __str__(self):
        return f'{self.post} {self.comment_list} {self.has_more}'
