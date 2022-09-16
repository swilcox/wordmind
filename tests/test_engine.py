import random
from game.engine import Game, GameStatus, Hint, HintLetter, HintType


def test_game_init():
    game = Game(["point", "not"])
    assert game._word == "point"
    assert game.status == GameStatus.IN_PROGRESS
    assert game._guesses == []
    assert game._hints == []
    assert game._word_list == ["point"]
    assert game.max_guesses == 6
    assert game.hard_mode == False
    assert game.word_length == 5


def test_game_hints():
    random.seed(2)
    word_list = ["think", "point", "sleep", "thiin"]
    game = Game(word_list)
    assert game._word == "think"

    # doesn't allow a word that's not in the word list
    assert game.submit_guess("blank") == False

    # allows a word that is the word list
    assert game.submit_guess("sleep") == True

    assert len(game._guesses) == 1
    assert len(game._hints) == 1
    expected_sleep_hint = Hint(
        [
            HintLetter("s", HintType.NOT_IN_WORD),
            HintLetter("l", HintType.NOT_IN_WORD),
            HintLetter("e", HintType.NOT_IN_WORD),
            HintLetter("e", HintType.NOT_IN_WORD),
            HintLetter("p", HintType.NOT_IN_WORD),
        ]
    )
    assert expected_sleep_hint == game._hints[0]
    expected_point_hint = Hint(
        [
            HintLetter("p", HintType.NOT_IN_WORD),
            HintLetter("o", HintType.NOT_IN_WORD),
            HintLetter("i", HintType.MATCH),
            HintLetter("n", HintType.MATCH),
            HintLetter("t", HintType.WRONG_SPOT),
        ]
    )
    assert game.submit_guess("point") == True
    assert len(game._guesses) == 2
    assert expected_point_hint == game._hints[1]
    expected_thiin_hint = Hint(
        [
            HintLetter("t", HintType.MATCH),
            HintLetter("h", HintType.MATCH),
            HintLetter("i", HintType.MATCH),
            HintLetter("i", HintType.NOT_IN_WORD),
            HintLetter("n", HintType.WRONG_SPOT),
        ]
    )
    assert game.submit_guess("thiin") == True
    assert len(game._guesses) == 3
    assert expected_thiin_hint == game._hints[2]
    assert game.eliminated_letters == ["e", "l", "o", "p", "s"]


def test_game_status_changes_loss():
    random.seed(1)
    word_list = ["think", "point", "sleep"]
    game = Game(word_list)
    assert game._word == "think"
    assert game.submit_guess("sleep") == True
    assert game.submit_guess("sleep") == True
    assert game.submit_guess("sleep") == True
    assert game.submit_guess("sleep") == True
    assert game.submit_guess("sleep") == True
    assert game.status == GameStatus.IN_PROGRESS
    assert game.submit_guess("sleep") == True
    assert game.submit_guess("sleep") == False
    assert game.status == GameStatus.COMPLETE
    assert game.won == False


def test_game_status_changes_win():
    random.seed(1)
    word_list = ["think", "point", "sleep"]
    game = Game(word_list)
    assert game._word == "think"
    assert game.won == False
    assert game.submit_guess("point") == True
    assert game.status == GameStatus.IN_PROGRESS
    assert game.submit_guess("think") == True
    assert game.status == GameStatus.COMPLETE
    assert game.won == True
    assert game.submit_guess("think") == False


def test_game_letter_status():
    random.seed(1)
    word_list = ["think", "point", "sleep"]
    game = Game(word_list)
    assert game._word == "think"
    assert game.submit_guess("point") == True
    assert game.eliminated_letters == ["o", "p"]
    assert game.match_letters == ["i", "n"]
    assert game.wrong_place_letters == ["t"]


def test_guesses_and_hints():
    random.seed(1)
    word_list = ["think", "point", "sleep"]
    game = Game(word_list)
    assert game._word == "think"
    assert game.submit_guess("point") == True
    assert game.guesses == ["point"]
    assert len(game.hints) == 1


def test_solution_list():
    random.seed(1)
    solution_list = ["think", "point", "sleep"]
    word_list = solution_list + ["break"]
    game = Game(word_list, solution_list=solution_list)
    assert game._word == "think"
    assert game.submit_guess("point") == True
    assert game.guesses == ["point"]
    assert len(game.hints) == 1
