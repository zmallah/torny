from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    usfa_id = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    foil_rating = models.CharField(max_length=3)
    saber_rating = models.CharField(max_length=3)
    epee_rating = models.CharField(max_length=3)
    foil_director_rating = models.CharField(max_length=5)
    saber_director_rating = models.CharField(max_length=5)
    epee_director_rating = models.CharField(max_length=5)
    tournaments = models.ManyToManyField(Tournament)


class Tournament(models.Model):
    oragnizer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    fencers = models.ManyToManyField(User)
    directors = models.ManyToManyField(User)


class Pool(models.Model):
    fencers = models.ManyToManyField(User)
    director = models.ManyToManyField(User)
    bouts = models.ManyToManyField(Bout)


class Bout(models.Model):
    fencer_left = models.ForeignKey(User, on_delete=models.CASCADE)
    fencer_right = models.ForeignKey(User, on_delete=models.CASCADE)
    fencer_right_score = models.IntegerField()
    fencer_left_score = models.IntegerField()
