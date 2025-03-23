import pytest
from unittest.mock import MagicMock
from .utils import evaluate_guess
from .constants import LetterStatus, GameStatus
from rest_framework.exceptions import ValidationError


@pytest.fixture
def mock_game():
    return MagicMock(
        correct_word="apple",
        guessed_words=[],
        letter_status={
            letter: {"status": None, "locations": []}
            for letter in "abcdefghijklmnopqrstuvwxyz"
        },
        game_status=GameStatus,
    )


def test_evaluate_guess_correct_guess(mock_game):
    evaluate_guess(mock_game, "apple")
    assert mock_game.game_status == GameStatus.COMPLETE
    assert mock_game.letter_status["a"]["status"] == LetterStatus.CORRECT
    assert mock_game.letter_status["p"]["status"] == LetterStatus.CORRECT
    assert mock_game.letter_status["l"]["status"] == LetterStatus.CORRECT
    assert mock_game.letter_status["e"]["status"] == LetterStatus.CORRECT
    mock_game.save.assert_called_once()


def test_evaluate_guess_duplicate_letters(mock_game):
    mock_game.correct_word = "bobby"
    evaluate_guess(mock_game, "booby")
    assert mock_game.letter_status["b"]["status"] == LetterStatus.CORRECT
    assert mock_game.letter_status["o"]["status"] == LetterStatus.CORRECT
    assert mock_game.letter_status["y"]["status"] == LetterStatus.CORRECT
    assert mock_game.letter_status["b"]["locations"] == [0, 3]
    mock_game.save.assert_called_once()


def test_evaluate_guess_word_already_guessed(mock_game):
    mock_game.guessed_words = ["apple"]
    with pytest.raises(ValidationError) as excinfo:
        evaluate_guess(mock_game, "apple")
    assert "Word already guessed." in str(excinfo.value)


def test_evaluate_guess_wrong_length(mock_game):
    with pytest.raises(ValidationError) as excinfo:
        evaluate_guess(mock_game, "app")
    assert "Word length is wrong." in str(excinfo.value)


def test_evaluate_guess_invalid_word(mock_game, monkeypatch):
    monkeypatch.setattr("game_engine.utils.all_words", lambda: ["apple", "banana"])
    with pytest.raises(ValidationError) as excinfo:
        evaluate_guess(mock_game, "xyzzy")
    assert "Word is not valid." in str(excinfo.value)
