from rest_framework.views import APIView
from .models import User, Tournament, UserInTournament, Profile, Pool, Event, EventLog, Role
from rest_framework.response import Response
from django.core import serializers
from django.contrib.auth import authenticate
import json


def serialize_model(data):
    data = serializers.serialize("json", [data])
    struct = json.loads(data)
    return json.dumps(struct[0])


# from datetime import datetime
class CreateTournament(APIView):

    def post(self, request):
        """
        creates a tournament with the given information
        """
        tournament = Tournament(name=request.data['name'],
                                # date=request.data['date'],
                                weapon=request.data['weapon'],
                                event_type=request.data['event_type'],
                                location=request.data['location']
                                )
        tournament.save()

        data = serialize_model(tournament)

        return Response(data.id)


class RegisterUser(APIView):
    """
    creates a new user and corresponding profile
    """

    def post(self, request):
        user = User.objects.create_user(
            request.data['user'],
            request.data['email'],
            request.data['pass'],
        )

        profile = Profile(
            user=user,
            username=request.data['user'],
            usfa_id=request.data['usfa'],
            date_of_birth=request.data['dob'],
            foil_rating=request.data['rfoil'],
            saber_rating=request.data['rsaber'],
            epee_rating=request.data['repee'],
            foil_director_rating=request.data['dfoil'],
            saber_director_rating=request.data['dsaber'],
            epee_director_rating=request.data['depee'])

        profile.save()

        # TODO: Authenticate Data before storing

        return Response("{\"result\":\"success\"}")


class AuthenticateUser(APIView):

    def post(self, request):
        user = authenticate(
            username=request.data['user'],
            password=request.data['pass']
        )
        if user is None:
            return Response("Bad Username or Password")

        return Response("success")


class Tournaments(APIView):

    def get(self, request, id=None):
        """
        creates a tournament with the given information
        """
        if id:
            data = serialize_model(Tournament.objects.get(id=id))
        else:
            data = serializers.serialize("json", Tournament.objects.all())
        return Response(data)


class RegisterUserInTournament(APIView):

    def post(self, request):
        user_id = request.data['user_id'] or request.user.id

        registration = UserInTournament(
            tournament=Tournament.objects.get(id=request.data['tournament_id']),
            user=User.objects.get(id=user_id),
            role=Role.objects.get(id=request.data['role']),
            status=True
        )

        registration.save()
        return Response(serialize_model(registration))


class Seeding(APIView):

    def post(self, request):
        tournament = Tournament.objects.get(id=request.data['tournament_id'])
        if tournament.weapon == 'foil':
            rating = 'foil_rating'
        elif tournament.weapon == 'saber':
            rating = 'saber_rating'
        elif tournament.weapon == 'epee':
            rating = 'epee_rating'

        fencers = tournament.users.objects.filter(role=1).order_by(rating)
        directors = tournament.users.objects.filter(role=2)

        directors_count = directors.count()

        pools = list()
        pool_count = 0
        for director in directors:
            pools[pool_count] = Pool(tournament=tournament.id,
                                     director=director.id)
            pool_count = pool_count + 1

        pool_count = 0
        for fencer in fencers:
            pools[pool_count].fencers.add(fencer)
            if pool_count != directors_count:
                pool_count = pool_count + 1
            else:
                pool_count = 0
            pools[pool_count].save()

        data = serializers.serialize("json", pools)
        return Response(data)


class CreateTourn(APIView):
    """
    Create Tournmanet
    """

    def post(self, request):
        tourn = Tournament(
            name=request.data['tournName'],
            date=request.data['date'],
            weapon=request.data['weaponSelect'],
            event_type=request.data['eventType'],
            location=request.data['location']
        )
        tourn.save()

        return Response('success')


class ListTourns(APIView):
    """
    List Tournaments
    """

    def get(self, request):
        tourns = Tournament.objects.all()
        out = []
        for t in tourns:
            out.append(
                {
                    "name": t.name,
                    "date": t.date,
                    "weapon": t.weapon,
                    "event_type": t.event_type,
                    "location": t.location
                }
            )
        return Response(out)


class LogEvent(APIView):

    def post(self, request):
        bout = request.data['bout_id']
        fencer = request.data['fencer']
        event = Event(bout=bout, event_type=request.data['event_id'],
                      fencer=fencer)
        if event.event_type.event_type == 'touch_scored':
            if bout.fencer_left == fencer:
                bout.fencer_left_score = bout.fencer_left_score + 1
            else:
                bout.fencer_right_score = bout.fencer_right_score + 1

            bout.save()
            event.fencer_left_score = bout.fencer_left_score
            event.fencer_right_score = bout.fencer_right_score
        elif event.event_type.event_type == 'bout_over':
            bout.completed = True
        event.save()


class NextBout(APIView):

    def post(self, request):
        return Pool.objects.get(request.data['pool_id']).bouts.filter(completed=0)
