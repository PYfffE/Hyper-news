from django.shortcuts import render
from django.http.response import HttpResponse
from django.http.response import Http404

# Create your views here.
from django.views import View


class MainView(View):
    def get(self, request):
        return HttpResponse('Coming soon')
