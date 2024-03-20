from django import template

from gamefolio_app.models import Game

register = template.Library()

@register.simple_tag
def get_image(game, image_type):
    return game.get_image(image_type)

@register.inclusion_tag('gamefolio_app/games.html')
def get_games_list(current_games=None):
    return {'games': Game.objects.all(),
            'current_games': current_games}