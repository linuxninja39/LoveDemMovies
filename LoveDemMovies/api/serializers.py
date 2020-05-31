from functools import reduce

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from LoveDemMovies.api.models import Movie, MovieUserRating


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    rating = serializers.SerializerMethodField(source='get_rating')

    @staticmethod
    def get_rating(movie):
        movie_user_ratings = movie.movieuserrating_set.all()
        count = movie_user_ratings.count()
        if movie_user_ratings.count() < 1:
            return 0
        if movie_user_ratings.count() == 1:
            return movie_user_ratings.first().rating

        # result = reduce(lambda a, b: a.rating + b.rating, movie_user_ratings) / movie_user_ratings.count()
        # not sure why the reduce is failing, using for instead
        total = 0
        for movie_user_rating in movie_user_ratings:
            total += movie_user_rating.rating
        return total/count

    class Meta:
        model = Movie
        fields = ['title', 'year', 'rating']


class MovieUserRatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovieUserRating
        fields = ['movie', 'user', 'rating']
