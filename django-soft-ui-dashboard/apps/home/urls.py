# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("search", views.search, name="search"),
<<<<<<< HEAD
    path("book", views.book, name="book"),
=======
>>>>>>> 003c9ed34f374ba7d87d4a60463da114f5c41ad9
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
