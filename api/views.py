from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from .models import Lecture, Professor, Profile, Rank
from .serializers import LectureSerializer, ResultSerializer, RankSerializer, ProfileSerializer
from rest_framework.decorators import action
from django.db.models import Q  # filter or 연산 가능
from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend


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
        # Serializer 인자에 data를 넣으면 deserialize -> data를 모델에 삽입
        serializer = LectureSerializer(data=request.data)
        # valid 하지 않으면 status code 400 raise
        serializer.is_valid(raise_exception=True)  # -> serializer.validated_data
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


class LectureFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    professor = filters.CharFilter(method='find_by_professor')

    class Meta:
        model = Lecture
        fields = ['name', 'professor']

    def find_by_professor(self, queryset, name, value):
        return queryset.filter(professor__name__icontains=value)


class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LectureFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  # 인증을 부여받은 대상만 update, delete 가능

    # @action(methods=['get'], detail=False, url_path='lecture-filter')  # detail: list인지 detail인지
    # def search_lecture(self, request):  # 입력을 query string으로 받음
    #     lecture_name = request.query_params.get('name')
    #     # request.GET도 가능, request.data[~]는 body에 담긴 data 접근(POST)
    #     if lecture_name is not None:
    #         lectures = Lecture.objects.filter(name__icontains=lecture_name).order_by('grade')
    #         # __icontains: 대소문자 구분 없이 포함 여부 확인
    #         # filter(~__gt=~): greater than, lt(less than), gte(greater than equal), lte
    #         serializer = LectureSerializer(lectures, many=True)
    #         return Response(serializer.data)
    #     return Response("검색 결과가 없습니다.")

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


class ProfileUpdatePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object.
        # account.user == 현재 접속 중인 user
        return obj.user == request.user


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (ProfileUpdatePermission,)  # 유저는 자신의 정보만 update, delete 가능

    @action(detail=True, url_path='mileage-cut')
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


class RankViewSet(viewsets.ModelViewSet):
    serializer_class = RankSerializer
    queryset = Rank.objects.all()
