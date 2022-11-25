from django.db import models


class Post(models.Model):
    author = models.ForeignKey('users.SNUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    created_at = models.DateField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)

    def likes_count(self):
        return PostStatistic.objects.filter(post_id=self.id, like__isnull=False).count()

    def dislikes_count(self):
        return PostStatistic.objects.filter(post_id=self.id, dislike__isnull=False).count()


class PostStatistic(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    user = models.ForeignKey('users.SNUser', on_delete=models.CASCADE, default=None, null=True, blank=True,
                                 related_name='user')
    created_at = models.DateTimeField(auto_now_add=True)
    created_at_date = models.DateField(auto_now_add=True)



class PostAnalytics(object):
    def __init__(self,date,likes,dislikes):
        self.date = date
        self.likes = likes
        self.dislikes = dislikes
