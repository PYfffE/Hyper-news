from django.shortcuts import render, redirect
from django.http.response import HttpResponse, Http404
import json

# Create your views here.
from django.views import View

from hypernews.settings import NEWS_JSON_PATH
from django.conf import settings

with open(settings.NEWS_JSON_PATH, 'r') as json_file:
    json_db = json.loads(json_file.read())

dates = sorted({i['created'][0:10] for i in json_db})
list.reverse(dates)

parsed_news = [[i['created'][0:10], i['link'], i['title']] for i in json_db]


class NewsView(View):

    def get(self, request):
        return render(request, 'news/news.html', {
            'dates': dates,
            'news': parsed_news,
        })


class LinkView(View):
    def get(self, request, link, *args, **kwargs):
        news = None
        for i in json_db:
            if str(i['link']) == link:
                news = i
        if news is None:
            raise Http404

        title = news['title']
        created = news['created']
        text = news['text']

        return render(request, 'news/link.html', {
            'title': title,
            'created': created,
            'text': text,
        })


class MainView(View):
    def get(self, request):
        return render(request, 'news/index.html')
