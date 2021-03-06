"""isogen4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from apps.api import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^search/([a-zA-Z0-9 -]+)', views.search),
    url(r'^feed/([0-9]+)', views.feed),
    url(r'^tasks/([a-z0-9]+)?', views.task_collection),
    url(r'^soundcloud/info/?', views.sc_info),
    url(r'^soundcloud/?', views.sc_download),
    url(r'^users/([a-z0-9A-Z]+)/repos', views.user_repos),
    url(r'^repos/(.+)/(.+)', views.github_repo),
    url(r'^cache', views.cache),



]
