from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from LoveDemMovies.api.models import Movie, MovieUserRating
from LoveDemMovies.api.serializers import UserSerializer, GroupSerializer, MovieSerializer, MovieUserRatingSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovieUserRatingViewSet(viewsets.ModelViewSet):
    queryset = MovieUserRating.objects.all()
    serializer_class = MovieUserRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
