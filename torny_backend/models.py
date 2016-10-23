from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    role = models.CharField(max_length=64)


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    # date = models.DateField()
    users = models.ManyToManyField(User, through='UserInTournament')
    weapon = models.CharField(max_length=100)
    event_type = models.CharField(max_length=16)
    location = models.CharField(max_length=100)


class UserInTournament(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.BooleanField()
    date_registration = models.DateField(default=timezone.now)


class Pool(models.Model):
    fencers = models.ManyToManyField(User,
                                     related_name='%(class)s_fence_pool')
    director = models.ManyToManyField(User,
                                      related_name='%(class)s_dir_pool')
    tournament = models.ForeignKey(Tournament)


class Bout(models.Model):
    pool = models.ForeignKey(Pool)
    fencer_left = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='%(class)s_fence_left')
    fencer_right = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='%(class)s_fence_right')
    fencer_left_score = models.IntegerField()
    fencer_right_score = models.IntegerField()
    completed = models.BooleanField(default=False)


class Event(models.Model):
    event_type = models.CharField(max_length=64)


class EventLog(models.Model):
    bout = models.ForeignKey(Bout)
    event_type = models.ForeignKey(Event)
    fencer = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='%(class)s_fencer')
    fencer_left_score = models.IntegerField()
    fencer_right_score = models.IntegerField()
