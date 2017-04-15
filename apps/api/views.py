from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from urllib.request import urlopen
import xmltodict
import json

def index(request:HttpRequest):
    context = {}
    return HttpResponse(":^)")



def feed(request:HttpRequest, num):
    atom_feed = urlopen("https://github.com/3jackdaws/isogen4/commits/master.atom")
    feed_dict = xmltodict.parse(atom_feed)
    return JsonResponse(feed_dict, json_dumps_params={"indent":2})