from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest

def index(request:HttpRequest):
    context = {}
    return HttpResponse(":^)")



def terminal(request:HttpRequest):
    context = {}
    return render(request, "apps/projects/terminal.html", context)