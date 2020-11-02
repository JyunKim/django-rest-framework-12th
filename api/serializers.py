from rest_framework import serializers
from .models import Lecture, Result, Rank, Profile


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class RankSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()  # 함수의 반환값을 필드로(default=get_~)
    # API 서버에 serializer로 name 필드가 추가되어서 나타남

    def get_name(self, obj):  # obj: rank 객체
        return obj.lecture.name

    class Meta:
        model = Rank
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    ranks = RankSerializer(many=True, read_only=True)  # ranks field 추가(nested)

    class Meta:
        model = Lecture
        fields = '__all__'
