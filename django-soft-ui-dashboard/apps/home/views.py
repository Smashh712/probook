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
from django.core.paginator import Paginator
import datetime as dt
import requests
import xmltodict
import random
import time
from .models import Hit


@login_required(login_url="/login/")
def index(request):
    q = Hit.objects.get(id=1)
    q.hit += 1
    q.save()

    test = requests.get(
        "http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbmlboy101516001&QueryType=ItemNewAll&MaxResults=50&start=1&SearchTarget=Book&CategoryId=437&output=xml&Version=20131101"
    )
    xml = xmltodict.parse(test.text)

    new_book = []
    idx = random.randint(0, len(xml["object"]))
    title = xml["object"]["item"][idx]["title"]
    cover = xml["object"]["item"][idx]["cover"]
    author = xml["object"]["item"][idx]["author"]
    book_id = xml["object"]["item"][idx]["@itemId"]

    new_book.append([title, cover, author, book_id])

    idx2 = idx
    while idx2 == idx:
        idx2 = random.randint(0, len(xml["object"]))

    title = xml["object"]["item"][idx2]["title"]
    cover = xml["object"]["item"][idx2]["cover"]
    author = xml["object"]["item"][idx2]["author"]
    book_id = xml["object"]["item"][idx2]["@itemId"]

    new_book.append([title, cover, author, book_id])

    context = {"new_book": new_book}
    context["num_new"] = len(xml["object"]["item"])
    context["hit"] = q.hit
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


@login_required(login_url="/login/")
def search(request):
    keyword = request.GET.get("key", "파이썬")  # 페이지
    new_book = []
    print(keyword)
    j = 0
    while j < 2:
        test = requests.get(
            f"https://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query={keyword}&QueryType=Title&MaxResults=50&start={j}&SearchTarget=Book&output=xml&Version=20070901&Sort=Accuracy"
        )
        xml = xmltodict.parse(test.text)
        j += 1
        if "item" in xml["object"]:
            i = 0
            while i < len(xml["object"]["item"]):
                title = xml["object"]["item"][i]["title"]
                if len(title) > 40:
                    title = title[:40] + " ..."
                cover = xml["object"]["item"][i]["cover"]
                author = xml["object"]["item"][i]["author"]
                descript = xml["object"]["item"][i]["description"]
                publisher = xml["object"]["item"][i]["publisher"]
                date = xml["object"]["item"][i]["pubDate"]
                date = dt.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")
                date = f"{date.year}년 {date.month}월 {date.day}일"
                book_id = xml["object"]["item"][i]["@itemId"]

                new_book.append(
                    [title, cover, author, descript, publisher, date, book_id]
                )
                i += 1
    # 입력 파라미터
    page = request.GET.get("page", "1")  # 페이지
    print(page)
    # 페이징처리
    paginator = Paginator(new_book, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {"book_list": page_obj}

    load_template = request.path.split("/")[-1]
    context["segment"] = load_template
    context["key"] = keyword
    return render(request, "home/tables.html", context)


@login_required(login_url="/login/")
def book(request):
    book_id = request.GET.get("id", "1")  # 페이지

    test = requests.get(
        f"http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey=ttbmlboy101516001&itemIdType=ItemId&ItemId={book_id}&output=xml&Cover=Big"
    )
    xml = xmltodict.parse(test.text)
    new_book = []
    new_book.append(xml["object"]["item"]["title"])
    new_book.append(xml["object"]["item"]["author"])
    new_book.append(xml["object"]["item"]["publisher"])
    new_book.append(xml["object"]["item"]["cover"])
    description = xml["object"]["item"]["description"]
    new_book.append(description[description.find("br") + 4 :])
    date = xml["object"]["item"]["pubDate"]
    date = dt.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")
    date = f"{date.year}년 {date.month}월 {date.day}일"

    new_book.append(date)
    new_book.append(xml["object"]["item"]["priceStandard"])
    new_book.append(xml["object"]["item"]["categoryName"])

    context = dict()
    context["book_feature"] = new_book
    context["segment"] = "search"
    return render(request, "home/book.html", context)
