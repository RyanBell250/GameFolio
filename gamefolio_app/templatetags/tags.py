from django import template
from gamefolio_app.models import ListEntry

from gamefolio_app.models import Game

register = template.Library()

@register.simple_tag
def get_image(game, image_type):
    return game.get_image(image_type)
  
@register.inclusion_tag("gamefolio_app/list_image.html")
def render_list_images(list):
    entries = ListEntry.objects.filter(list = list)[:4];
    if(len(entries) < 4):
        entries =[entries[0]];
    return {"entries": entries, "list": list}

@register.inclusion_tag("gamefolio_app/game_card.html", takes_context=True)
def render_game_card(context, game, *args, **kwargs):

    context_dict = kwargs
    context_dict["game"] = game;
    context_dict["user"] = context["user"]
    print(kwargs)

    return context_dict

@register.inclusion_tag("gamefolio_app/review.html")
def render_review(review):
    return {"review": review}

@register.inclusion_tag("gamefolio_app/review.html", takes_context=True)
def render_review(context, review):
    user = context["user"]
    return {"review": review, "user": user}
