from rest_framework import serializers
from .models import Lecture, Result, Rank, Profile


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class RankSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.lecture.name

    class Meta:
        model = Rank
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    ranks = RankSerializer(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = '__all__'
