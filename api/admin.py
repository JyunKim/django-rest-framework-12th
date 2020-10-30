from django.contrib import admin
from .models import Lecture, Profile, Rank, Result


admin.site.register(Lecture, Profile, Rank, Result)