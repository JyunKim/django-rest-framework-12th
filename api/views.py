from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lecture, Professor, Profile
from .serializers import LectureSerializer, ResultSerializer, RankSerializer, ProfileSerializer
from rest_framework.decorators import action
from django.db.models import Q


'''
# APIView를 사용하여 프론트와 소통
class LectureList(APIView):
    # format=None - 포맷을 query parameter가 아닌 format suffix로 전달
    def get(self, request, format=None):
        lectures = Lecture.objects.all()
        # 모델 인스턴스를 파이썬 내부 자료형으로 변환
        # 쿼리셋을 직렬화할 때는 many=True
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LectureSerializer(data=request.data)
        # valid 하지 않으면 status code 400 raise
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LectureDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Lecture, pk=pk)

    def get(self, request, pk, format=None):
        lecture = self.get_object(pk)
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        lecture = self.get_object(pk)
        serializer = LectureSerializer(lecture, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        lecture = self.get_object(pk)
        lecture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()

    @action(methods=['post'], detail=False)  # detail: list인지 detail인지
    def filter(self, request):
        pf = Professor.objects.get(pk=request.POST['professor'])
        lectures = Lecture.objects.filter(Q(name=request.POST['name']) | Q(professor=pf)).order_by('grade')
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def result(self, request, pk):
        lecture = get_object_or_404(Lecture, pk=pk)
        result = lecture.result
        serializer = ResultSerializer(result)
        return Response(serializer.data)

    @action(detail=True)
    def rank(self, request, pk):
        lecture = get_object_or_404(Lecture, pk=pk)
        ranks = lecture.ranks.all().order_by('-mileage', 'grade')
        serializer = RankSerializer(ranks, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @action(detail=True)
    def mileage_cut(self, request, pk):
        mileage_cut = {}
        user = get_object_or_404(Profile, pk=pk)
        for lecture in user.lectures.all():
            if lecture.result.include_second_major:
                if user.major == lecture.department or user.second_major == lecture.department:
                    mileage_cut[lecture.name] = lecture.ranks.filter(is_included=True, grade=user.grade, success=True
                                                                     ).order_by('mileage')[0].mileage
                else:
                    mileage_cut[lecture.name] = lecture.ranks.filter(is_included=False, grade=user.grade, success=True
                                                                     ).order_by('mileage')[0].mileage
            else:
                if user.major == lecture.department:
                    mileage_cut[lecture.name] = lecture.ranks.filter(is_included=True, grade=user.grade, success=True
                                                                     ).order_by('mileage')[0].mileage
                else:
                    mileage_cut[lecture.name] = lecture.ranks.filter(is_included=False, grade=user.grade, success=True
                                                                     ).order_by('mileage')[0].mileage
        return Response(mileage_cut)
