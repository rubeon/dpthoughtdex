from django.contrib import admin
from dpthoughtdex.models import Source, Author, Link

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'url')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('author', 'url', 'source')

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Source, SourceAdmin)