from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from isogen4.util import send_file

try:
    import soundscrape.soundscrape as soundscrape
except:
    pass

def index(request:HttpRequest):
    context = {}
    return HttpResponse(":^)")



def terminal(request:HttpRequest):
    context = {}
    return render(request, "apps/projects/terminal2.html", context)



def physics(request: HttpRequest):
    return render(request, 'apps/projects/physics.html')

def bad_design(request: HttpRequest):
    return render(request, 'apps/projects/bad_design.html')


def soundcloud(request):


    return render(request, 'apps/projects/soundcloud.html')

def soundcloud_get(request, artist, song):
    response = {}
    if request.GET:
        if soundscrape:
            artist = request.GET.get('artist')
            song = request.GET.get('song')
            soundscrape.download_file()
        else:
            response['error'] = "this endpoint is not yet available."

