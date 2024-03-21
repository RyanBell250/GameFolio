from django import template

from gamefolio_app.models import Game

register = template.Library()

@register.simple_tag
def get_image(game, image_type):
    return game.get_image(image_type)
