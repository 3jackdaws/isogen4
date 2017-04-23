from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from urllib.request import urlopen
import xmltodict
import json
from .models import TaskCompletion, Task, TaskCollection, Actor
from isogen4.views import error
from isogen4.util import send_file
import apps.api.modules.sc as soundcloud

def index(request:HttpRequest):
    context = {}
    return HttpResponse(":^)")



def feed(request:HttpRequest, num):
    atom_feed = urlopen("https://github.com/3jackdaws/isogen4/commits/master.atom")
    feed_dict = xmltodict.parse(atom_feed)
    return JsonResponse(feed_dict, json_dumps_params={"indent":2})


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


def sc_info(request):
    if request.GET:
        url = request.GET.get('url')
        if url:
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
            stream = soundcloud.get_stream_as_resource(track)
            filename = "/tmp/" + track['title'] + ".mp3"
            file = open(filename, "wb+")
            file.write(stream.read())
            return send_file(request, filename)

    return JsonResponse({'error'}, json_dumps_params={'indent':2})