""" base URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), {"TITLE": settings.TITLE}),
    path('', include('apps.users.urls', namespace="users")),
    path('', include('apps.things.urls', namespace="things")),
    path('admin/', admin.site.urls),
]
