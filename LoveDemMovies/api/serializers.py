from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

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
        return total / count

    class Meta:
        model = Movie
        fields = ['title', 'year', 'rating']


class MovieUserRatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MovieUserRating
        fields = ['movie', 'user', 'rating']


class UserSerializerWithToken(serializers.HyperlinkedModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')
