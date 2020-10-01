from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.views import APIView
from .serializers import LectureSerializer, ProfessorSerializer, RankSerializer, ResultSerializer, ProfileSerializer


class LectureList(APIView):
    def get(self, request):

    def post(self, request):
