import random
from enum import Enum
from dataclasses import dataclass


class HintType(Enum):
    NOT_IN_WORD = 0
    WRONG_SPOT = 1
    MATCH = 2


@dataclass
class HintLetter:
    letter: str
    hint_type: HintType


@dataclass
class Hint:
    hint_letters: list[HintLetter]

    def accounted_for(self, letter):
        return sum(
            1
            for hl in self.hint_letters
            if hl.letter == letter and hl.hint_type != HintType.NOT_IN_WORD
        )


class GameStatus(Enum):
    IN_PROGRESS = 0
    COMPLETE = 1


class Game:
    def __init__(
        self,
        word_list: list[str],
        *,
        solution_list: list[str] = None,
        max_guesses=6,
        word_length=5,
        hard_mode=False,
        word=""
    ):
        self.word_length = word_length
        self.max_guesses = max_guesses
        self.hard_mode = hard_mode
        self._guesses = []
        self._hints = []
        self._word_list = [word for word in word_list if len(word) == self.word_length]
        self._solution_list = (
            [word for word in solution_list if len(word)]
            if solution_list
            else self._word_list
        )
        self._word = self._choose_word() if not word else word
        self.status = GameStatus.IN_PROGRESS

    def _choose_word(self) -> str:
        return random.choice(self._solution_list)

    def _update_game_status(self):
        if self._guesses[-1] == self._word or len(self._guesses) >= self.max_guesses:
            self.status = GameStatus.COMPLETE

    @property
    def hints(self) -> list[Hint]:
        return self._hints

    @property
    def guesses(self) -> list[str]:
        return self._guesses

    @property
    def won(self) -> bool:
        if self._guesses and self._guesses[-1] == self._word:
            return True
        return False

    @property
    def eliminated_letters(self) -> list[str]:
        f_letters = set()
        e_letters = set()
        for hint in self._hints:
            for hl in hint.hint_letters:
                if hl.hint_type == HintType.NOT_IN_WORD:
                    e_letters.add(hl.letter)
                else:
                    f_letters.add(hl.letter)
        elim_list = list(e_letters - f_letters)
        elim_list.sort()
        return elim_list

    def _find_letters(self, hint_type: HintType) -> list[str]:
        f_letters = set()
        for hint in self._hints:
            for hl in hint.hint_letters:
                if hl.hint_type == hint_type:
                    f_letters.add(hl.letter)
        found_list = list(f_letters)
        found_list.sort()
        return found_list

    @property
    def eliminated_letters(self) -> list[str]:
        e_list = list(
            set(self._find_letters(HintType.NOT_IN_WORD))
            - set(self._find_letters(HintType.MATCH))
            - set(self._find_letters(HintType.WRONG_SPOT))
        )
        e_list.sort()
        return e_list

    @property
    def match_letters(self) -> list[str]:
        return self._find_letters(HintType.MATCH)

    @property
    def wrong_place_letters(self) -> list[str]:
        return self._find_letters(HintType.WRONG_SPOT)

    def submit_guess(self, guess: str) -> bool:
        if (
            guess not in self._word_list
            or len(self._guesses) >= self.max_guesses
            or self.status != GameStatus.IN_PROGRESS
        ):
            return False
        self._guesses.append(guess)
        hint_letters = []
        for i, letter in enumerate(guess):
            if letter == self._word[i]:
                hint_letters.append(HintLetter(letter=letter, hint_type=HintType.MATCH))
            else:
                # initially mark all non-matches as not_in_word
                hint_letters.append(
                    HintLetter(letter=letter, hint_type=HintType.NOT_IN_WORD)
                )
        # loop back thru and identify mis-matches as appropriate
        hint = Hint(hint_letters)
        for i, letter in enumerate(guess):
            if (
                letter != self._word[i] and letter in self._word
            ):  # is the letter in the word but not in the right spot
                if hint.accounted_for(letter) < self._word.count(letter):
                    # only show as wrong_spot if that letter isn't already accounted for somehow
                    hint.hint_letters[i].hint_type = HintType.WRONG_SPOT
        self._hints.append(hint)
        self._update_game_status()
        return True
