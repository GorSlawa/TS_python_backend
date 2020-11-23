from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)


class Message(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(null=False)
    reply = models.IntegerField(null=True)
