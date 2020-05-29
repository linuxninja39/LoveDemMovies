import unittest

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.

from LoveDemMovies.api.models import Movie, MovieUserRating
from LoveDemMovies.api.serializers import MovieSerializer


class MoveSerializerTests(TestCase):
    def setUp(self) -> None:
        movie = Movie(title='2112', year=2112)
        movie.save()
        tom = User(first_name='Tom', last_name='Sawyer', username='ts')
        tom.save()
        kubla = User(first_name='Kubla', last_name='Khan', username='kk')
        kubla.save()
        MovieUserRating.objects.create(user=tom, movie=movie, rating=3).save()
        MovieUserRating.objects.create(user=kubla, movie=movie, rating=1).save()

    def test_rating(self):
        movie = Movie.objects.get(title='2112', year='2112')
        rate = MovieSerializer.get_rating(movie)
        self.assertEqual(2, rate)


if __name__ == '__main__':
    unittest.main()
