from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from isogen4.util import send_file
from .models import Project, Technology



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

def projects(request:HttpRequest, short_name=None):

    context = {"project": None}
    if short_name:
        try:
            context['project'] = Project.objects.get(short_name=short_name)
        except Exception as e:
            print(e)
    return render(request, 'apps/projects/projects.html', context)
