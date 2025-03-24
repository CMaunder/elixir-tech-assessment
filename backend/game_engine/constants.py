from django.db import models


class GameStatus(models.TextChoices):
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    ABANDONED = "abandoned"
    FAILED = "failed"


class LetterStatus(models.TextChoices):
    CONTAINS = "contains"
    INCORRECT = "incorrect"
    CORRECT = "correct"
    UNKNOWN = "unknown"
