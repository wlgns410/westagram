from django.db import models
# from django.db.models.deletion import SET_NULL

class Account(models.Model):
    name            = models.CharField(max_length=50)
    nickname        = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=50, unique=True)
    password        = models.CharField(max_length=200)
    email           = models.EmailField(max_length=200, unique=True)

    class Meta:
        db_table = "accounts"

class Follow(models.Model):
    following   = models.ForeignKey(Account, max_length=7000, on_delete=models.CASCADE, related_name="following")
    follower    = models.ForeignKey(Account, max_length=7000, on_delete=models.CASCADE, related_name="follower")

    class Meta:
        db_table = "follows"