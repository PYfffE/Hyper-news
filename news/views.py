from datetime import datetime

from django.shortcuts import render, redirect
from django.http.response import HttpResponse, Http404
import json

# Create your views here.
from django.views import View

from hypernews.settings import NEWS_JSON_PATH
from django.conf import settings

# json_db = None
# parsed_news = None
# dates = None


def news_update():
    global json_db
    global parsed_news
    global dates

    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        json_db = json.loads(json_file.read())
    parsed_news = [[i['created'][0:10], i['link'], i['title']] for i in json_db]

    dates = sorted({i['created'][0:10] for i in json_db})

    list.reverse(dates)


news_update()


def search(q):
    global parsed_news
    found = []
    print(parsed_news)
    for i in parsed_news:
        if q in i[2]:
            found.append(i)
    return found


def get_dates(news):
    return sorted({i['created'][0:10] for i in news})


def insert(title, text):
    global json_db

    json_db.append({'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'text': text, 'title': title, 'link': len(json_db) + 1})
    with open(settings.NEWS_JSON_PATH, 'w') as json_file:
        json_file.write(json.dumps(json_db))

    news_update()


class NewsView(View):

    def get(self, request):
        search_news = None
        q = request.GET.get('q')
        print(type(q))
        search_dates = sorted({i['created'][0:10] for i in json_db})
        if q is not None:
            if q == '':
                search_news = []
            else:
                search_news = search(q)
            search_dates = sorted({i[0][0:10] for i in search_news})
        else:
            search_news = parsed_news
        list.reverse(search_dates)
        return render(request, 'news/news.html', {
            'dates': search_dates,
            'news': search_news,
        })


class NewsManipulation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        insert(request.POST.get('title'), request.POST.get('text'))
        return redirect('/news/')


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
        return redirect('/news/')
