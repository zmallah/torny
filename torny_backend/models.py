from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    usfa_id = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    foil_rating = models.CharField(max_length=5)
    saber_rating = models.CharField(max_length=5)
    epee_rating = models.CharField(max_length=5)
    foil_director_rating = models.CharField(max_length=5)
    saber_director_rating = models.CharField(max_length=5)
    epee_director_rating = models.CharField(max_length=5)
    email = models.EmailField()


class Role(models.Model):
    role_type = models.CharField(max_length=64)


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    users = models.ManyToManyField(User, through='Membership')


class UserInTournament(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_registration = models.DateField()


class Bout(models.Model):
    fencer_left = models.ForeignKey(User, on_delete=models.CASCADE)
    fencer_right = models.ForeignKey(User, on_delete=models.CASCADE)
    fencer_right_score = models.IntegerField()
    fencer_left_score = models.IntegerField()


class Pool(models.Model):
    fencers = models.ManyToManyField(User)
    director = models.ManyToManyField(User)
    bouts = models.ManyToManyField(Bout)
