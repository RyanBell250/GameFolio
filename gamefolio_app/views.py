from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from gamefolio_app.models import Game, Review

class IndexView(View):
    def get(self, request):
        #game_list = Game.objects.order_by('-views')[:5]
        game_list = sorted(Game.objects.all(), key = lambda p : p.average_rating())[:5]
        reviews_list = Review.objects.order_by('-likes')[:6]
        
        context_dict = {}
        context_dict['games'] = game_list
        context_dict['reviews'] = reviews_list
        
        return render(request, 'gamefolio_app/index.html', context=context_dict)