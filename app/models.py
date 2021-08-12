from django.db import models

# Create your models here.


class Event(models.Model):
    type = models.CharField(max_length=100)
    public = models.BooleanField(default=True)
    repo_id = models.IntegerField()
    actor_id = models.IntegerField()
