from django.urls import path
from .views import LectureList, LectureDetail


app_name = 'api'
urlpatterns = [
    path('', LectureList.as_view(), name='index'),
    path('<int:pk>/', LectureDetail.as_view(), name='detail'),
]