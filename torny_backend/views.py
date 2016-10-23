from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Tournament, UserInTournament

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
        return Response(tournament.id)


class ListUsers(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
