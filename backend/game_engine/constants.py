from django.db import models


class GameStatus(models.TextChoices):
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    ABANDONED = "abandoned"


class LetterStatus(models.TextChoices):
    CONTAINS = "contains"
    INCORRECT = "incorrect"
    CORRECT = "correct"
