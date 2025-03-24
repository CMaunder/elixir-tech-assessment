from rest_framework.exceptions import ValidationError
from .constants import LetterStatus, GameStatus


def load_words_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def all_words():
    return load_words_from_file("allowed_words.txt")


def all_letters():
    return [chr(letter) for letter in range(ord("a"), ord("z") + 1)]


def evaluate_guess(game, guessed_word):
    if guessed_word in set(game.guessed_words):  # set for O(1) lookup
        raise ValidationError(
            {"message": "Word already guessed."},
        )
    if len(guessed_word) != len(game.correct_word):
        raise ValidationError(
            {"message": "Word length is wrong."},
        )
    if not guessed_word.lower() in set(all_words()):  # set for O(1) lookup
        raise ValidationError(
            {"message": "Word is not valid."},
        )

    for i, letter in enumerate(guessed_word):
        if letter == game.correct_word[i]:

            game.letter_status[letter]["status"] = LetterStatus.CORRECT
            game.letter_status[letter]["locations"] = game.letter_status[letter][
                "locations"
            ] + [i]
        elif (
            letter in game.correct_word
            and not game.letter_status[letter]["status"]
            == LetterStatus.CORRECT  # handles duplicate letter case if letter is already correct
        ):
            game.letter_status[letter]["status"] = LetterStatus.CONTAINS
        elif letter not in game.correct_word:
            game.letter_status[letter]["status"] = LetterStatus.INCORRECT
    if guessed_word == game.correct_word:
        game.game_status = GameStatus.COMPLETE
    elif game.guess_count >= 5:
        game.game_status = GameStatus.FAILED
    game.guessed_words.append(guessed_word)
    game.save()
    return game
