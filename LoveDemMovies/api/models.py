from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=250)
    year = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'year'], name='unique_title_year')
        ]

    def __str__(self):
        return "%s: %s" % (self.title, self.year)


class MovieUserRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie', 'user'], name='movie_user_unique')
        ]

    def __str__(self):
        return "%s: %f" % (self.movie.title, self.rating)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return "%s" % self.comment
