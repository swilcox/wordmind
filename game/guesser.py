import random
import re


from game.engine import Game, GameStatus, HintType


class Guesser:
    def __init__(
        self,
        game: Game,
        word_list: list[str],
        starting_word: str = "",
        search_cache: dict = None,
    ):
        self.word_list = word_list
        self.starting_word = (
            starting_word if starting_word else random.choice(word_list)
        )
        self._use_cache = True if search_cache is not None else False
        self.cache = search_cache

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
                if len(exclude_letters + addtl_excluded):
                    regex += f"[^{exclude_letters+addtl_excluded}]"
                else:
                    regex += f"[a-z]"
                if hl.hint_type == HintType.WRONG_SPOT:
                    must_contain.append(hl.letter)
        try:
            r = re.compile(regex)
        except Exception as ex:
            print("offending regex: " + regex)
            raise ex
        if self._use_cache:
            tmp_words = self.cache.get(regex, None) or list(
                filter(r.match, self.word_list)
            )
            if regex not in self.cache:
                self.cache[regex] = tmp_words
            # print(len(tmp_words))
        else:
            tmp_words = filter(r.match, self.word_list)
        possible_words = [
            pw
            for pw in tmp_words
            if all(must_contain.count(l) <= pw.count(l) for l in must_contain)
        ]
        return random.choice(possible_words)

    def play(self):
        while self.game.status == GameStatus.IN_PROGRESS:
            self.game.submit_guess(self.compute_guess())
