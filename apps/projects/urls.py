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
from apps.projects import views
from apps.api.views import task_collection

urlpatterns = [
    url(r'^$', views.index),
    url(r'^terminal/?$', views.terminal),
    url(r'^physics/?$', views.physics),
    url(r'^snippets/?$', views.bad_design),
    url(r'^soundcloud/?$', views.soundcloud),
    url(r'^tasks/([a-z0-9]+)?', task_collection),
    url(r'^projects/([a-z]+)/?$', views.projects),
    url(r'^share$', views.share),
]
