import pytest
from unittest.mock import MagicMock, patch
from .utils import evaluate_guess
from .constants import LetterStatus, GameStatus
from rest_framework.exceptions import ValidationError


@pytest.fixture
def mock_game():
    def _mock_game(correct_word="apple", guessed_words=None, guess_count=5):
        game = MagicMock()
        game.correct_word = correct_word
        game.guessed_words = guessed_words or []
        game.letter_status = {
            letter: {"status": None, "locations": []}
            for letter in "abcdefghijklmnopqrstuvwxyz"
        }
        game.game_status = None
        game.guess_count = guess_count
        return game

    return _mock_game


class TestEvaluateGuessValidation:
    def test_raises_error_when_word_already_guessed(self, mock_game):
        game = mock_game(guessed_words=["apple"])
        with pytest.raises(ValidationError, match="Word already guessed."):
            evaluate_guess(game, "apple")

    def test_raises_error_when_word_length_is_wrong(self, mock_game):
        game = mock_game()
        with pytest.raises(ValidationError, match="Word length is wrong."):
            evaluate_guess(game, "app")

    @patch("game_engine.utils.all_words", return_value=["apple", "grape", "mango"])
    def test_raises_error_when_word_is_invalid(self, mock_all_words, mock_game):
        game = mock_game()
        with pytest.raises(ValidationError, match="Word is not valid."):
            evaluate_guess(game, "xyzzy")


class TestEvaluateGuessGameplay:
    def test_sets_game_complete_when_guess_is_correct(self, mock_game):
        game = mock_game(guess_count=2)
        evaluate_guess(game, "apple")
        assert game.game_status == GameStatus.COMPLETE
        assert game.guessed_words == ["apple"]

    def test_sets_game_failed_when_last_incorrect_guess(self, mock_game):
        game = mock_game(guess_count=5)
        evaluate_guess(game, "grape")
        assert game.game_status == GameStatus.FAILED
        assert "grape" in game.guessed_words

    def test_updates_letter_status_for_partial_match(self, mock_game):
        game = mock_game()
        evaluate_guess(game, "apply")

        assert game.letter_status["a"]["status"] == LetterStatus.CORRECT
        assert game.letter_status["p"]["status"] == LetterStatus.CORRECT
        assert game.letter_status["l"]["status"] == LetterStatus.CORRECT
        assert game.letter_status["y"]["status"] == LetterStatus.INCORRECT


class TestEvaluateGuessAdditionalCases:
    def test_handles_all_letters_wrong(self, mock_game):
        game = mock_game(correct_word="apple")
        evaluate_guess(game, "brown")

        assert all(
            game.letter_status[letter]["status"] == LetterStatus.INCORRECT
            for letter in "brown"
        )
        assert "brown" in game.guessed_words

    def test_handles_multiple_correct_letters(self, mock_game):
        game = mock_game(correct_word="speed")
        evaluate_guess(game, "peeps")

        # 'e' is correct (position 2), 'p' and 's' are present but wrong positions
        assert game.letter_status["p"]["status"] == LetterStatus.CONTAINS
        assert game.letter_status["e"]["status"] == LetterStatus.CORRECT
        assert game.letter_status["s"]["status"] == LetterStatus.CONTAINS

    def test_handles_duplicate_letters_correctly(self, mock_game):
        game = mock_game(correct_word="berry")
        evaluate_guess(game, "error")

        # First 'r' is correct (position 3), second is present (position 4)
        assert game.letter_status["r"]["status"] == LetterStatus.CORRECT
        assert game.letter_status["r"]["locations"] == [
            2
        ]  # Only marks correct position
        assert game.letter_status["e"]["status"] == LetterStatus.CONTAINS

    def test_handles_all_letters_present_but_wrong_positions(self, mock_game):
        game = mock_game(correct_word="stare")
        evaluate_guess(game, "tares")

        assert all(
            game.letter_status[letter]["status"] == LetterStatus.CONTAINS
            for letter in "tares"
        )

    def test_handles_partial_match_with_duplicates(self, mock_game):
        game = mock_game(correct_word="drama")
        evaluate_guess(game, "amass")

        # 'a' appears twice in correct word, once in correct position
        # 'm' is correct, 's' is incorrect
        assert game.letter_status["a"]["status"] == LetterStatus.CORRECT
        assert game.letter_status["a"]["locations"] == [2]
        assert game.letter_status["m"]["status"] == LetterStatus.CONTAINS
        assert game.letter_status["s"]["status"] == LetterStatus.INCORRECT

    def test_handles_exact_duplicate_letters(self, mock_game):
        game = mock_game(correct_word="llama")
        evaluate_guess(game, "lulls")

        # First two 'l's are correct, third is present (only 2 'l's in correct word)
        assert game.letter_status["l"]["status"] == LetterStatus.CORRECT
        assert game.letter_status["l"]["locations"] == [0]
        assert game.letter_status["u"]["status"] == LetterStatus.INCORRECT
        assert game.letter_status["s"]["status"] == LetterStatus.INCORRECT
