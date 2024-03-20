from django import template

register = template.Library()

@register.simple_tag
def get_image(game, image_type):
    return game.get_image(image_type)

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