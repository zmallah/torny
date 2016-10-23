from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=64)
    usfa_id = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    foil_rating = models.CharField(max_length=5)
    saber_rating = models.CharField(max_length=5)
    epee_rating = models.CharField(max_length=5)
    foil_director_rating = models.CharField(max_length=5)
    saber_director_rating = models.CharField(max_length=5)
    epee_director_rating = models.CharField(max_length=5)


class Role(models.Model):
    role_type = models.CharField(max_length=64)


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    users = models.ManyToManyField(User, through='UserInTournament')
    weapon = models.CharField(max_length=100)
    event_type = models.CharField(max_length=16)
    location = models.CharField(max_length=100)


class UserInTournament(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.BooleanField()
    date_registration = models.DateField()


class Bout(models.Model):
    fencer_left = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='%(class)s_fence_left')
    fencer_right = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='%(class)s_fence_right')
    fencer_right_score = models.IntegerField()
    fencer_left_score = models.IntegerField()


class Pool(models.Model):
    fencers = models.ManyToManyField(User,
                                     related_name='%(class)s_fence_pool')
    director = models.ManyToManyField(User,
                                      related_name='%(class)s_dir_pool')
    bouts = models.ManyToManyField(Bout)
