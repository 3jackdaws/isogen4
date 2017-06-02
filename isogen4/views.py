from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from wsgiref.util import FileWrapper
from isogen4.settings import STATIC_ROOT
from apps.api.utils import file_cache

def index(request:HttpRequest):
    context = {}
    return render(request, "isogen/homepage.html", context)


def portfolio(request:HttpRequest):
    return render(request, "isogen/profile.html", {})


def error(errornum, message):
    def error(request):
        return render(request, 'isogen/error.html', {"status":errornum, "message":message})
    return error


def static(request, path):
    content_type = "text/html"
    if ".css" in path:
        content_type = "text/css"
    filename = STATIC_ROOT + path
    text = file_cache(filename)
    response = HttpResponse(text, content_type=content_type)
    return response