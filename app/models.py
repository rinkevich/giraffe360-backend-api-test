from django.db import models


class Event(models.Model):
    EVENT_CHOICES = (
        ("PushEvent", "Push Event"),
        ("ReleaseEvent", "Release Event"),
        ("WatchEvent", "Watch Event"),
    )

    type = models.CharField(max_length=100, choices=EVENT_CHOICES)
    public = models.BooleanField(default=True)
    repo_id = models.IntegerField()
    actor_id = models.IntegerField()
