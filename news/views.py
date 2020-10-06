from django.shortcuts import render, redirect
from django.http.response import HttpResponse, Http404
import json

# Create your views here.
from django.views import View

from hypernews.settings import NEWS_JSON_PATH
from django.conf import settings

with open(settings.NEWS_JSON_PATH, 'r') as json_file:
    json_db = json.loads(json_file.read())


class NewsView(View):
    def get(self, request):
        return HttpResponse("Hyper News")


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
        return HttpResponse("Coming soon")
