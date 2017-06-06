from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from urllib.request import urlopen, Request
import xmltodict
import json
import re
from .models import TaskCompletion, Task, TaskCollection, Actor
from isogen4.views import error
from isogen4.util import send_file, stream_resource
import apps.api.modules.sc as soundcloud
import mutagen
from apps.api.modules.dhook import DiscordWebhook
from apps.projects.models import Project, Experiment
from apps.api import utils as api_utils

def index(request:HttpRequest):
    context = {}
    return HttpResponse(":^)")

def feed(request:HttpRequest, num):
    feed_dict = {}
    if request.GET:
        url = request.GET.get("url")
        if url:
            atom_feed = urlopen(url + "/commits/master.atom")
            feed_dict = xmltodict.parse(atom_feed)
    return JsonResponse(feed_dict, json_dumps_params={"indent":2})

def search(request:HttpRequest, query):
    query=query.lower()
    results = {
        "results": {
            "projects": {
                "name": "Projects",
                "results": []
            },
            "experiments": {
                "name": "Experiments",
                "results": []
            }
        }
    }
    for project in Project.objects.all():
        tags = [str(x) for x in project.technologies.all()]
        if query in project.name.lower() or query in project.short_description.lower() or query in " ".join(tags):
            results['results']['projects']['results'].append({
                "title":project.name,
                "description":project.short_description,
                "url":"/projects/" + project.short_name,
                "tags":tags
            })

    for experiment in Experiment.objects.all():
        tags = [str(x) for x in experiment.technologies.all()]
        if query in experiment.name.lower() or query in experiment.short_description.lower() or query in " ".join(tags):
            results['results']['experiments']['results'].append({
                "title":experiment.name,
                "description":experiment.short_description,
                "url":"/experiments/" + experiment.short_name,
                "tags":tags
            })

    return JsonResponse(results, json_dumps_params={"indent":2})

@csrf_exempt
def task_collection(request, identifier):
    completion = None
    collection = None
    if request.GET:
        task_id = request.GET.get('task-id')
        actor = request.GET.get('actor')
        if task_id and actor:
            actor = Actor.objects.get(name=actor)
            task = Task.objects.get(id=task_id)
            if task and actor:
                task_completion = TaskCompletion(actor=actor)
                task_completion.save()
                task.completions.add(task_completion)
                task.save()

    if identifier:
        try:
            collection = TaskCollection.objects.get(identifier=identifier)
        except Exception as e:
            print(e)
            return error(404, "Task collection not found.")(request)

    return render(request, 'apps/task/task_collection.html', {"collection": collection})


def api_task(request, collection):
    if request.GET:
        task_id = request.GET.get('task-id')
        actor = request.GET.get('actor')
        if task_id and actor:
            actor = Actor.objects.get(name=actor)
            task = Task.objects.get(id=task_id)
            if task and actor:
                task_completion = TaskCompletion(actor=actor)
                task_completion.save()
                task.completions.add(task_completion)
                task.save()


def sc_info(request):
    if request.GET:
        url = request.GET.get('url')
        if url and "soundcloud.com" in url:
            track = soundcloud.resolve(url)
            response = {}
            response['title'] = track['title']
            response['artwork'] = track['artwork_url']
            response['description'] = track['description']
            return JsonResponse(track)

    return JsonResponse({'error'}, json_dumps_params={'indent':2})

def sc_download(request):
    if request.GET:
        url = request.GET.get('url')
        if url:
            track = soundcloud.resolve(url)
            filename = soundcloud.file_from_track(track)
            track = soundcloud.resolve(url)
            stream = soundcloud.get_stream_as_resource(track)
            filename = "/tmp/" + track['title'] + ".mp3"
            with open(filename, "wb+") as file:
                file.write(stream.read())
                file.close()

            audio = mutagen.File(filename)
            audio.add_tags()
            audio = soundcloud.set_artist_title(audio, track['user']['username'], track['title'])
            audio = soundcloud.embed_artwork(audio, soundcloud.get_300px_album_art(track))
            audio.save(filename, v1=2)
            return send_file(request, filename)

    return JsonResponse({'error'}, json_dumps_params={'indent':2})

def user_repos(request, user):
    repo = api_utils.get_repo_json("https://api.github.com/users/" + user + "/repos?sort=pushed")
    return JsonResponse(repo, json_dumps_params={"indent": 2}, safe=False)

def github_repo(request, user, repo):
    repo = api_utils.github_request("https://api.github.com/repos/" + user + "/" + repo)
    return HttpResponse(repo, content_type='application/json')

def cache(request):
    response = "{}"
    content_type = 'application/json'
    if request.GET:
        url = request.GET['url']
        if url:
            req = Request(url)
            response = api_utils.api_cache(req)
            try:
                json.loads(response)
            except:
                content_type = "text/plain"
    return HttpResponse(response, content_type=content_type)