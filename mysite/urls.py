# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include # 追記7

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')), # 追記6
]

