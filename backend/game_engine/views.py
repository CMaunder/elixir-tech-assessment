from django.shortcuts import render
from django.http import JsonResponse
from .models import Game, User, GameStatus, LetterStatus
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import (
    GameSerializer,
    UserSerializer,
)
from .utils import all_words, evaluate_guess


class UserView(APIView):
    def get(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    def post(self, request, user_id=None):
        if user_id:
            return Response(
                {"message": "Method Not Allowed: User ID should not be provided."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        user = User.objects.create()
        Game.objects.create(user=user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GameView(APIView):
    def get(self, request, game_id=None):
        if not game_id:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)

        game = Game.objects.get(id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def post(self, request):
        data = json.loads(request.body)
        user_id = data["user_id"]
        game = Game.objects.create(user_id=user_id)
        serializer = GameSerializer(game)
        return Response(serializer.data)


class UserActiveGameView(APIView):
    def get(self, request, user_id):
        games = Game.objects.filter(user_id=user_id, game_status=GameStatus.IN_PROGRESS)
        if games:
            serializer = GameSerializer(games[0])
            return Response(serializer.data)
        else:
            return Response(
                {"message": "No active game found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, user_id):
        if user_id is None:
            return Response(
                {"message": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        active_games = User.objects.get(id=user_id).games.filter(
            game_status=GameStatus.IN_PROGRESS
        )
        if active_games:
            return Response(
                {"message": "User already has an active game."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        game = Game.objects.create(user_id=user_id)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def patch(self, request, user_id):
        if not request.body:
            return Response(
                {"message": "Request body is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = json.loads(request.body)
        active_games = User.objects.get(id=user_id).games.filter(
            game_status=GameStatus.IN_PROGRESS
        )
        if not active_games:
            return Response(
                {"message": "No active game found for the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        game_id = active_games[0].id
        guessed_word = data["guessed_word"]
        game = Game.objects.get(id=game_id)
        if game.game_status == GameStatus.IN_PROGRESS:
            game = evaluate_guess(game, guessed_word)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Game is not in progress."},
                status=status.HTTP_400_BAD_REQUEST,
            )
