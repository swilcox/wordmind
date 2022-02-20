from multiprocessing.connection import answer_challenge
import random
import re
import sys


from wordmind import Game, GameStatus, HintType


class Guesser:
    def __init__(self, game: Game, word_list: list[str], starting_word: str = ""):
        self.word_list = word_list
        self.starting_word = (
            starting_word if starting_word else random.choice(word_list)
        )
        self.game = game

    def compute_guess(self) -> str:
        if len(self.game.hints) == 0:
            return self.starting_word
        exclude_letters = "".join(self.game.eliminated_letters)
        must_contain = []
        regex = ""
        for i, hl in enumerate(self.game.hints[-1].hint_letters):
            if hl.hint_type == HintType.MATCH:
                regex += hl.letter
                must_contain.append(hl.letter)
            else:
                addtl_excluded = ""
                for hint in self.game.hints:
                    if hint.hint_letters[i].hint_type == HintType.WRONG_SPOT:
                        addtl_excluded += hint.hint_letters[i].letter
                regex += f"[^{exclude_letters+addtl_excluded}]"
                if hl.hint_type == HintType.WRONG_SPOT:
                    must_contain.append(hl.letter)
        r = re.compile(regex)
        possible_words = [
            pw
            for pw in filter(r.match, self.word_list)
            if all(must_contain.count(l) <= pw.count(l) for l in must_contain)
        ]
        return random.choice(possible_words)

    def play(self):
        while self.game.status == GameStatus.IN_PROGRESS:
            self.game.submit_guess(self.compute_guess())
