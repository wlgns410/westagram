from user.models import Account
from django.db import models

from user.models import Account

class Posting(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    img_url = models.URLField(max_length=200)

    class Meta:
        db_table = "postings"

class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Posting, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    re_comment = models.ForeignKey("self", on_delete=models.CASCADE, related_name="Comment",null=True)

    class Meta:
        db_table = "comments"

class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Posting, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'