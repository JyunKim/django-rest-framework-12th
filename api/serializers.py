from rest_framework import serializers
from .models import Lecture, Professor, Rank, Result, Profile


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
