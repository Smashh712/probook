# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Hit(models.Model):
    hit = models.IntegerField()
<<<<<<< HEAD


class User(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    like = models.IntegerField()
=======
>>>>>>> 003c9ed34f374ba7d87d4a60463da114f5c41ad9
