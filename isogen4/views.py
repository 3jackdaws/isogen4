from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest

def index(request:HttpRequest):
    context = {}
    return render(request, "isogen/homepage.html", context)


def portfolio(request:HttpRequest):
    return render(request, "isogen/profile.html", {})


def error(errornum, message):
    def error(request):
        return render(request, 'isogen/error.html', {"status":errornum, "message":message})
    return error