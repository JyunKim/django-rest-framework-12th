from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import LectureList, LectureDetail
from rest_framework import routers
from .views import LectureViewSet, ProfileViewSet, RankViewSet


'''
app_name = 'api'
urlpatterns = [
    path('lectures/', LectureList.as_view(), name='index'),
    path('lectures/<int:pk>/', LectureDetail.as_view(), name='detail'),

]
# APPEND_SLASH가 디폴트로 설정되어 있어서 일치하는 패턴이 없으면 자동으로 url 끝에 / 붙여줌
# 하지만 POST같은 요청의 경우 redirect 시 submit한 데이터가 유실될 수 있으므로 에러 발생시킴

# url에 format 추가
urlpatterns = format_suffix_patterns(urlpatterns)
'''

router = routers.DefaultRouter()
router.register(r'lectures', LectureViewSet)  # r: raw string(\도 그대로 출력)
router.register(r'profiles', ProfileViewSet)
router.register(r'ranks', RankViewSet)

urlpatterns = router.urls
