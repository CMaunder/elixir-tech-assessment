from django.db import models
import random
from django.core.exceptions import ValidationError

from .constants import LetterStatus, GameStatus
from .utils import all_words


def get_random_word():  # TODO - change this to get the daily word
    return random.choice(all_words()).upper()


def all_letters():
    return dict(
        (chr(letter), {"status": LetterStatus.UNKNOWN, "locations": []})
        for letter in range(ord("A"), ord("Z") + 1)
    )


class User(models.Model):
    id = models.AutoField(primary_key=True)


class Game(models.Model):

    id = models.AutoField(primary_key=True)
    letter_status = models.JSONField(default=all_letters)
    guessed_words = models.JSONField(default=list)

    game_status = models.CharField(
        max_length=20, choices=GameStatus.choices, default=GameStatus.IN_PROGRESS
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    correct_word = models.CharField(
        max_length=5,
        default=get_random_word,
    )

    @property
    def guess_count(self):
        return len(self.guessed_words)
