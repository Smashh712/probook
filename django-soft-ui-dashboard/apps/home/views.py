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
import sqlite3
from .models import Hit, User
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


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

    keyword = request.GET.get("key", "?????????")  # ?????????
    new_book = []
    recommned_list = []
    if keyword:
        recommend_list = recommend(request.user.id)
    j = 1
    while j < 3:
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
                date = f"{date.year}??? {date.month}??? {date.day}???"
                book_id = xml["object"]["item"][i]["@itemId"]

                new_book.append(
                    [title, cover, author, descript, publisher, date, book_id]
                )
                i += 1
    # ?????? ????????????
    rec_idx = recommend_list.index
    temp = []
    temp2 = []
    for i in range(len(recommend_list)):
        if recommend_list.iloc[i] <= 0:
            break
        for j in range(len(new_book)):
            if str(rec_idx[i]) == new_book[j][6]:
                temp2.append(new_book[j])
                break

    for j in range(len(new_book)):
        if new_book[j] not in temp2:
            temp.append(new_book[j])

    new_book = temp2[::-1] + temp
    print(temp2)
    # print(new_book)
    # print(new_book)
    page = request.GET.get("page", "1")  # ?????????
    # ???????????????
    paginator = Paginator(new_book, 10)  # ???????????? 10?????? ????????????
    page_obj = paginator.get_page(page)

    context = {"book_list": page_obj}

    load_template = request.path.split("/")[-1]
    context["segment"] = load_template
    context["key"] = keyword
    return render(request, "home/tables.html", context)


@login_required(login_url="/login/")
def book(request):
    book_id = request.GET.get("id", "1")  # ?????????

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
    date = f"{date.year}??? {date.month}??? {date.day}???"

    new_book.append(date)
    new_book.append(xml["object"]["item"]["priceStandard"])
    new_book.append(xml["object"]["item"]["categoryName"])

    context = dict()
    context["book_feature"] = new_book
    context["segment"] = "search"
    context["book_id"] = book_id
    like = 0
    try:
        existUser = User.objects.get(user_id=request.user.id, book_id=book_id)
        if existUser:
            like = existUser.like
    except:
        pass
    context["like"] = like
    return render(request, "home/book.html", context)


def recommend(rec_user):
    data = User.objects.all()
    user = []
    book = []
    like = []
    # score_df = pd.read_csv(
    #     "C:/hs/probook/django-soft-ui-dashboard/apps/home/data/user-bookscore.csv",
    #     sep=",",
    # )
    # for i in range(len(score_df)):
    #     a = score_df.iloc[i, 0]
    #     b = score_df.iloc[i, 1]
    #     c = score_df.iloc[i, 2]
    #     q = User(user_id=a, book_id=b, like=c)
    #     q.save()

    for row in data:
        user.append(row.user_id)
        book.append(row.book_id)
        like.append(row.like)
    score_df = pd.DataFrame({"user_id": user, "book_id": book, "score": like})

    score_tb = pd.pivot_table(
        score_df, values="score", index=["book_id"], columns=["user_id"], aggfunc=np.sum
    )
    score_tb = score_tb.fillna(0)

    with open("../data/booklist_id.csv", "r", encoding="UTF-8") as f:
        line = f.read()

    booklist_id = line.split(",")

    book_df = pd.DataFrame(index=booklist_id)
    book_df.index.name = "book_id"
    book_df.columns.name = "user_id"

    ub_score_df = book_df.join(score_tb)  # ?????? ?????? ???????????? ????????? ???
    ub_score_df = ub_score_df.fillna(0)

    score_tb_T = score_tb.transpose()

    user_sim = cosine_similarity(score_tb_T, score_tb_T)

    # cosine_similarity()??? ????????? Numpy ????????? ??????????????? ????????? DataFrame?????? ??????
    user_sim_df = pd.DataFrame(
        data=user_sim, index=score_tb.columns, columns=score_tb.columns
    )

    rec_list = pd.DataFrame(index=score_tb.index)

    for j in score_tb.index:
        sum = 0.0
        count = 0
        for i in user_sim_df.index:
            u = user_sim_df.loc[i, rec_user]
            b = score_tb.loc[j, i]
            if b != 0:
                result = u * b
                sum += result
                count += 1
        rec_list.loc[j, rec_user] = sum / count

    unread_filter = score_tb[rec_user] == 0
    rec_list = rec_list.loc[unread_filter]

    return rec_list[rec_user].sort_values(ascending=False)  # ?????? ??????(?????? ?????????)


@login_required(login_url="/login/")
def like(request):
    try:
        existUser = User.objects.get(
            user_id=request.user.id, book_id=request.POST["book_id"]
        )
        if existUser:
            existUser.like = request.POST["like"]
            existUser.save()
    except:
        user = User()
        user.user_id = request.user.id
        user.book_id = request.POST["book_id"]
        user.like = request.POST["like"]
        user.save()

    return HttpResponseRedirect(request.POST["path"] + "?id=" + request.POST["book_id"])
