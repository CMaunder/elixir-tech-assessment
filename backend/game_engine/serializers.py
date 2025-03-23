from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    guess_count = serializers.IntegerField()

    class Meta:
        model = Game
        fields = "__all__"


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    games = GameSerializer(many=True)
