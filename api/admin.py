from django.contrib import admin
from .models import Lecture, Profile, Rank, Result


admin.site.register(Lecture)
admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Result)