# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Hit(models.Model):
    hit = models.IntegerField()


class User(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    like = models.IntegerField()
