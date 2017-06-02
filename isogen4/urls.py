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
from django.conf.urls import url, include
from django.contrib import admin
from isogen4 import views
from apps.projects.views import projects

urlpatterns = [
    url(r'^$', views.index),
    url(r'^ian/?$', views.portfolio),
    url(r'^experiments/', include("apps.projects.urls")),
    url(r'^projects/([a-z]+)/?', projects),
    url(r'^api/', include("apps.api.urls")),
    url(r'^admin/', admin.site.urls),
    url(r'^static/([\s\S]+)', views.static),
    url(r'.', views.error(404, "That page was not found")),
]

