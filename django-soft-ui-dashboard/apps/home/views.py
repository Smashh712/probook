# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
import requests
import xmltodict
import random


@login_required(login_url="/login/")
def index(request):

    test = requests.get(
        "http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbmlboy101516001&QueryType=ItemNewAll&MaxResults=50&start=1&SearchTarget=Book&CategoryId=437&output=xml&Version=20131101"
    )
    xml = xmltodict.parse(test.text)

    new_book = []
    idx = random.randint(0, len(xml["object"]))
    title = xml["object"]["item"][idx]["title"]
    cover = xml["object"]["item"][idx]["cover"]
    author = xml["object"]["item"][idx]["author"]
    descript = xml["object"]["item"][idx]["description"]

    new_book.append([title, cover, author, descript])

    idx2 = idx
    while idx2 == idx:
        idx2 = random.randint(0, len(xml["object"]))

    title = xml["object"]["item"][idx2]["title"]
    cover = xml["object"]["item"][idx2]["cover"]
    author = xml["object"]["item"][idx2]["author"]
    descript = xml["object"]["item"][idx2]["description"]

    new_book.append([title, cover, author, descript])

    context = {"new_book": new_book}

    print(context)
    return render(request, "home/index.html", context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))
