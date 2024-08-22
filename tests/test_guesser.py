import random
from wordmind.game.engine import Game, GameStatus
from wordmind.game.guesser import Guesser


def test_basic_guesser():
    word_list = ["think", "point", "sleep", "thiin"]
    game = Game(word_list, word="think")
    random.seed(1)
    guesser = Guesser(game=game, word_list=word_list)
    first_guess = guesser.compute_guess()
    assert first_guess == "point"
    game.submit_guess(first_guess)
    next_guess = guesser.compute_guess()
    assert next_guess == "think"


def test_forced_first_guess():
    word_list = ["blink", "plink", "think", "thiin"]
    game = Game(word_list, word="plink")
    random.seed(1)
    guesser = Guesser(game=game, word_list=word_list, starting_word="think")
    first_guess = guesser.compute_guess()
    assert first_guess == "think"


def test_guess_logic():
    word_list = ["blink", "plink", "think", "thiin", "thinp"]
    game = Game(word_list, word="plink")
    random.seed(1)
    guesser = Guesser(game=game, word_list=word_list, starting_word="thinp")
    first_guess = guesser.compute_guess()
    assert first_guess == "thinp"
    game.submit_guess(first_guess)
    for x in range(5):
        random.seed(x)  # no matter what it should pick `plink`
        second_guess = guesser.compute_guess()
        assert second_guess == "plink"


def test_guess_cache():
    word_list = ["blink", "plink", "think", "thiin", "thinp"]
    my_cache = {}
    game = Game(word_list, word="plink")
    random.seed(1)
    guesser = Guesser(
        game=game, word_list=word_list, starting_word="thinp", search_cache=my_cache
    )
    guesser.play()
    assert my_cache == {"[^ht][^ht]in[^htp]": ["blink", "plink"]}
    # replay so that the cache gets used
    game = Game(word_list, word="plink")
    random.seed(1)
    guesser = Guesser(
        game=game, word_list=word_list, starting_word="thinp", search_cache=my_cache
    )
    guesser.play()


def test_play_logic():
    word_list = ["blink", "plink", "think", "thiin", "thinp"]
    game = Game(word_list, word="plink")
    guesser = Guesser(game=game, word_list=word_list, starting_word="thinp")
    guesser.play()
    assert game.status == GameStatus.COMPLETE
    assert game.won is True
    assert len(game.guesses) == 2
