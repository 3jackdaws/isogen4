from django.db.models import Model
from django.db import models
import datetime
from urllib.request import Request, urlopen
from urllib.parse import urlencode

TASK_TYPES = (
        (0, "Rotating"),
        (1, 'Periodic'),
    )


class Actor(Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TaskCompletion(Model):
    time = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(Actor, blank=False)

    def __str__(self):
        return self.actor.name + " on " + str(self.time)

    def nicedatetime(self):
        return self.time.strftime("%A, %b %d at %-H:%M%p")


class Task(Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    completions = models.ManyToManyField(TaskCompletion)
    members = models.ManyToManyField(Actor, blank=True)
    type = models.IntegerField(choices=TASK_TYPES)

    def get_type_name(self):
        return TASK_TYPES[self.type][1]

    def last_ten_completions(self):
        return self.completions.order_by('-time')[:10]

    def __str__(self):
        return self.name + " - " + TASK_TYPES[self.type][1]


class TaskCollection(Model):
    name = models.CharField(max_length=50)
    identifier = models.CharField(max_length=8)
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return self.name

DISCORD_BASE_API = "https://discordapp.com/api/webhooks/{}/{}"
class DiscordWebhook(Model):
    name = models.CharField(max_length=100)
    avatar = models.URLField()
    id = models.BigIntegerField(primary_key=True)
    token = models.CharField(max_length=68)

    def send(self, content):
        params = {
            "content": content,
            "username": self.name
        }
        if self.avatar:
            params['avatar_url'] = self.avatar
        url = DISCORD_BASE_API.format(self.id, self.token)
        request = Request(url, urlencode(params).encode('utf-8') if params else None)
        request.add_header("User-Agent", "WebhookExecutor (http://isogen.net/, 1.0)")
        site = urlopen(request)
        return site.read().decode('utf-8')

