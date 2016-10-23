from rest_framework.views import APIView
from .models import User, Tournament, UserInTournament
from rest_framework.response import Response
from .renderers import JSONRenderer
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


class Tournaments(APIView):

    def get(self, request, id=None):
        """
        creates a tournament with the given information
        """
        if id:
            data = serializers.serialize("json", [Tournament.objects.get(id=id), ])
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
