from django.contrib import admin
from .models import Genre, Movie, Actor

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Actor)
