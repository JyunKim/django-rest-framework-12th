from django.contrib import admin
from .models import Lecture, Profile, Rank, Result, Professor


admin.site.register(Lecture)
admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Result)
admin.site.register(Professor)