__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from django.contrib import admin
from django.urls import path, re_path
from django.urls import path, include
from django.views.generic.base import RedirectView

from django.urls import re_path, path, include
from rest_framework import routers
from .update_rest import update_rest


from .my_rest_api import my_rest_viewsetB
import json
router = routers.DefaultRouter()

def default_list(request):
    return ''

urlpatterns = [
    path('api/', include(router.urls), name='django_rest_admin_api'),
    path('default_list/', default_list, name='django_rest_admin_self_default_list'),
]

