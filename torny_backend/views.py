from rest_framework.views import APIView
from .models import User, Tournament, UserInTournament
from rest_framework.response import Response
from django.core import serializers
import json


# from datetime import datetime
class CreateTournament(APIView):

    def post(self, request):
        """
        creates a tournament with the given information
        """
        tournament = Tournament(name=request.data['name'],
                                date=request.data['date'],
                                weapon=request.data['weapon'])
        tournament.save()

        data = serializers.serialize("json", [tournament, ])
        struct = json.loads(data)
        data = json.dumps(struct[0])

        return Response(data.id)


class RegisterUser(APIView):
    """
    creates a new user and corresponding profile
    """

    def post(self, request):
        user = User.objects.create_user(
                request.data['user'],
                request.data['email'],
                request.data['pass']
                )

        profile = Profile(
                user = user,
                username = request.data['user'],
                usfa_id = request.data['usfa'],
                date_of_birth = request.data['dob'],
                foil_rating = request.data['rfoil'],
                saber_rating = request.data['rsaber'],
                epee_rating = request.data['repee'],
                foil_director_rating = request.data['dfoil'],
                saber_director_rating = request.data['dsaber'],
                epee_director_rating = request.data['depee'])
        profile.save()

        # TODO: Authenticate Data before storing

        return Response("{\"result\":\"success\"}")


class AuthenticateUser(APIView):

    def post(self, request):
        return Response()


class Tournaments(APIView):

    def get(self, request, id=None):
        """
        creates a tournament with the given information
        """
        if id:
            data = serializers.serialize("json", [Tournament.objects.get(id=id)])
            struct = json.loads(data)
            data = json.dumps(struct[0])
        else:
            data = serializers.serialize("json", Tournament.objects.all())
        return Response(data)


class ListUsers(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # usernames = [user.username for user in User.objects.all()]
        # return Response(usernames)
