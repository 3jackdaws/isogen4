from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from urllib.request import urlopen
import xmltodict
import json
from .models import TaskCompletion, Task, TaskCollection, Actor
from isogen4.views import error

def index(request:HttpRequest):
    context = {}
    return HttpResponse(":^)")



def feed(request:HttpRequest, num):
    atom_feed = urlopen("https://github.com/3jackdaws/isogen4/commits/master.atom")
    feed_dict = xmltodict.parse(atom_feed)
    return JsonResponse(feed_dict, json_dumps_params={"indent":2})


def task_collection(request, identifier):
    print(identifier)
    completion = None
    collection = None
    if request.GET:
        print("get was set")
        task_id = request.GET.get('task-id')
        actor = request.GET.get('actor')
        actor = Actor.objects.get(name=actor)
        task = Task.objects.get(id=task_id)
        if task and actor:
            task_completion = TaskCompletion(actor=actor)
            task_completion.save()
            task.completions.add(task_completion)
            task.save()

            print("added completion")
    if identifier:
        try:
            collection = TaskCollection.objects.get(identifier=identifier)
        except Exception as e:
            print(e)
            return error(404, "Task collection not found.")(request)

    return render(request, 'apps/projects/task_collection.html', {"collection": collection})
