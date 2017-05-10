from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.request import urlopen
import xmltodict
import json
from .models import TaskCompletion, Task, TaskCollection, Actor
from isogen4.views import error
from isogen4.util import send_file, stream_resource
import apps.api.modules.sc as soundcloud
import mutagen
from apps.api.modules.dhook import DiscordWebhook

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

# def sc_download(request):
#     if request.GET:
#         url = request.GET.get('url')
#         if url:
#             track = soundcloud.resolve(url)
#             stream = soundcloud.get_stream_as_resource(track)
#             filename = track['title'] + ".mp3"
#
#             return stream_resource(stream, filename)
#
#     return JsonResponse({'error'}, json_dumps_params={'indent':2})




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

def discord_webhook(request):
    got_params = False
    response = {}


    if request.POST:
        webhook_id = request.POST.get("id")
        webhook_token = request.POST.get("token")
        content = request.POST.get("content")
        name = request.POST.get("name")
        if content and webhook_url:
            got_params = True

    if content:
        try:
            url = "https://discordapp.com/api/webhooks/" + webhook_id + "/" + webhook_token
            print("url")
            print("url")
            webhook = DiscordWebhook(url)
            webhook.send(content)
            response = {
                "success":True
            }
        except Exception as e:
            print(e)
            response = {
                "error":"Invalid Webhook URI"
            }

    return JsonResponse(response, json_dumps_params={"indent":2})