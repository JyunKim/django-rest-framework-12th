from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LectureList, LectureDetail


app_name = 'api'
urlpatterns = [
    path('lectures/', LectureList.as_view(), name='index'),
    path('lectures/<int:pk>/', LectureDetail.as_view(), name='detail'),
]

# url endpoint에 format 추가
urlpatterns = format_suffix_patterns(urlpatterns)
