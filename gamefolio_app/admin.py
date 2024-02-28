from django.contrib import admin
from gamefolio_app.models import Author, Game, Review, List, ListEntry

#Shows list entrys on list page in admin
class ListEntry(admin.TabularInline):
    model = ListEntry
    classes = ['collapse']

class ListAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "List Information",
            {
                "fields": ["title", "description", "slug"],
            }
        ),
    ]
    readonly_fields = ('slug',)
    inlines = (ListEntry,)

admin.site.register(Author)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(List, ListAdmin)