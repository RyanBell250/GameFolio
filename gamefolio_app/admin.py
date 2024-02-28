from django.contrib import admin
from gamefolio_app.models import Author, Game, Review, List
# Register your models here.
admin.site.register(Author)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(List)