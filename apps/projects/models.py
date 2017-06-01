from django.db.models import Model
from django.db import models
from isogen4.util import markdown_to_html


class Technology(Model):
    name = models.CharField(max_length=32)
    short_description = models.CharField(max_length=400)
    external_url = models.URLField()
    is_language = models.BooleanField()
    color = models.CharField(max_length=16, choices=(
        ("red", "red"),
        ("yellow", "yellow"),
        ("orange", "orange"),
        ("blue", "blue"),
        ("black", "black"),
        ("grey", "grey"),
        ("teal", "teal"),
        ("purple", "purple"),
        ("violet", "violet"),
        ("olive", "olive"),
        ("pink", "pink"),
        ("brown","brown")
    ))

    def __str__(self):
        return self.name


PROJECT_STATUS = [
    "Active",
    "In Progress",
    "Postponed",
    "Deferred",
    "Hope to Revisit",
    "Abandoned"
]


class Project(Model):
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=32)
    short_description = models.CharField(max_length=400)
    short_name = models.CharField(max_length=32, unique=True)
    picture = models.ImageField()
    start_date = models.DateTimeField()
    status = models.IntegerField(choices=(
        (0, "Active"),
        (1, "In Progress"),
        (2, "Postponed"),
        (3, "Deferred"),
        (4, "Hope to Revisit"),
        (5, "Abandoned"),
    ))
    text = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True)
    external_url = models.URLField()

    def __str__(self):
        return self.name

    def get_status(self):
        return PROJECT_STATUS[self.status]

    def get_html(self):
        return markdown_to_html(self.text)

    def language(self):
        lang = [x for x in self.technologies.all() if x.is_language]
        return lang if len(lang) > 0 else None


class Experiment(Model):
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=32)
    short_description = models.CharField(max_length=400)
    short_name = models.CharField(max_length=32, unique=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    def __str__(self):
        return self.name
