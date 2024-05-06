import argparse
from enum import IntEnum
import os
import string
import time

from colorama import Fore, Back, Style
from blessed import Terminal

from game.engine import Game, GameStatus, HintType
from game.guesser import Guesser


def _read_in_file(file_name) -> list[str]:
    with open(os.path.join("data", file_name), "rt") as f:
        return [line.strip() for line in f.readlines()]


class ColorMode(IntEnum):
    NORMAL = 0
    COLOR_BLIND = 1


HINT_MAP = [
    {
        HintType.MATCH: Fore.BLACK + Back.GREEN,
        HintType.NOT_IN_WORD: Fore.LIGHTBLACK_EX + Back.BLACK,
        HintType.WRONG_SPOT: Fore.BLACK + Back.YELLOW,
    },
    {
        HintType.MATCH: Fore.BLACK + Back.RED,
        HintType.NOT_IN_WORD: Fore.LIGHTBLACK_EX + Back.BLACK,
        HintType.WRONG_SPOT: Fore.BLACK + Back.LIGHTBLUE_EX,
    },
]

CHAR_COLOR_MAP = [
    {
        HintType.MATCH: Fore.GREEN,
        HintType.NOT_IN_WORD: Fore.LIGHTBLACK_EX,
        HintType.WRONG_SPOT: Fore.YELLOW,
    },
    {
        HintType.MATCH: Fore.RED,
        HintType.NOT_IN_WORD: Fore.LIGHTBLACK_EX,
        HintType.WRONG_SPOT: Fore.LIGHTBLUE_EX,
    },
]


class GameScreen:
    def __init__(self, term: Terminal, game: Game, color_blind=False, speed=500):
        self.term = term
        self.color_mode = ColorMode.COLOR_BLIND if color_blind else ColorMode.NORMAL
        self.color_blind = color_blind
        self.game = game
        self.speed = speed
        self._current_guess = 0

    def display_title(self):
        print("Welcome to WordMind!")

    def display_guesses(self):
        with self.term.location(0, 2):
            for y in range(self.game.max_guesses):
                for x in range(self.game.word_length):
                    print("\u2395", end="")
                print()

    def display_keyboard(self):
        with self.term.location(0, 2 + self.game.max_guesses + 1):
            rows = [
                "qwertyuiop",
                "asdfghjkl",
                "zxcvbnm",
            ]
            for y, row in enumerate(rows):
                print(" " * y, end="")
                for c in row:
                    if c in self.game.eliminated_letters:
                        print(
                            CHAR_COLOR_MAP[self.color_mode][HintType.NOT_IN_WORD]
                            + c
                            + " "
                            + Style.RESET_ALL,
                            end="",
                        )
                    elif c in self.game.wrong_place_letters:
                        print(
                            CHAR_COLOR_MAP[self.color_mode][HintType.WRONG_SPOT]
                            + c
                            + " "
                            + Style.RESET_ALL,
                            end="",
                        )
                    elif c in self.game.match_letters:
                        print(
                            CHAR_COLOR_MAP[self.color_mode][HintType.MATCH]
                            + c
                            + " "
                            + Style.RESET_ALL,
                            end="",
                        )
                    else:
                        print(c + " ", end="")
                print()

    def update_status(self, status: str):
        with self.term.location(0, self.game.max_guesses + 7):
            print(self.term.clear_eol)
        with self.term.location(0, self.game.max_guesses + 7):
            print(Fore.RED + status + Style.RESET_ALL)

    def get_input(self) -> str:
        current_number = len(self.game.hints)
        length = self.game.word_length
        with self.term.cbreak():
            result = ""
            done = False
            while not done:
                val = self.term.inkey()
                if val.is_sequence:
                    if val.name == "KEY_BACKSPACE" and len(result):
                        result = result[:-1]
                    elif val.name == "KEY_ENTER" and len(result) == length:
                        done = True
                elif val in string.ascii_lowercase and len(result) < length:
                    result += val
                for i in range(self.game.word_length):
                    with self.term.location((i * 1) + 0, 2 + (current_number * 1)):
                        print(result[i] if i < len(result) else "\u2395")
                self.update_status("")
        return result

    def reveal_hint(self):
        hint = self.game.hints[-1].hint_letters
        for i in range(self.game.word_length):
            with self.term.location((i * 1) + 0, 1 + (len(self.game.hints) * 1)):
                time.sleep(self.speed / 1000)
                print(
                    HINT_MAP[self.color_mode][hint[i].hint_type]
                    + hint[i].letter
                    + Style.RESET_ALL
                )


def main():
    parser = argparse.ArgumentParser(description="WordMind Game")
    parser.add_argument(
        "--word_list",
        dest="word_file",
        default="all_words.txt",
        help="list of possible guess words",
    )
    parser.add_argument(
        "--answer_words",
        dest="answer_file",
        default="words.txt",
        help="list of words the answer can come from",
    )
    parser.add_argument(
        "--solution",
        dest="solution",
        default="",
        help="force the answer to a particular word",
    )
    parser.add_argument(
        "--speed",
        dest="speed",
        default=500,
        type=int,
        help="reveal speed in ms per letter",
    )
    parser.add_argument(
        "--word_length",
        dest="word_length",
        default=5,
        help="number of letters in each word",
    )
    parser.add_argument(
        "--max_guesses", dest="max_guesses", default=6, help="maximum number of guesses"
    )
    parser.add_argument(
        "--color_blind",
        action="store_true",
        help="increase contrast for colors",
    )
    parser.add_argument(
        "--hard",
        dest="hard_mode",
        action="store_true",
        help="hard mode - strict guess enforcement (not implemented yet)",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="have the automated guesser play instead",
    )
    parser.add_argument(
        "--starting_word",
        default="",
        help="first guess if `--auto` mode is enabled",
    )
    args = parser.parse_args()
    word_list = _read_in_file(args.word_file)
    answer_list = _read_in_file(args.answer_file)
    game = Game(
        word_list=word_list,
        solution_list=answer_list,
        max_guesses=args.max_guesses,
        word_length=args.word_length,
        hard_mode=args.hard_mode,
        word=args.solution,
    )
    if args.auto:
        guesser = Guesser(game, word_list, starting_word=args.starting_word)
    term = Terminal()
    with term.fullscreen(), term.hidden_cursor():
        screen = GameScreen(term, game, speed=args.speed, color_blind=args.color_blind)
        screen.display_title()
        screen.display_guesses()

        while game.status == GameStatus.IN_PROGRESS:
            screen.display_keyboard()
            if args.auto:
                guess = guesser.compute_guess()
            else:
                guess = screen.get_input()
            if guess:
                if not game.submit_guess(guess):
                    screen.update_status(
                        f"invalid guess, {guess} is not a word I know!"
                    )
                else:
                    screen.update_status("")
                    screen.reveal_hint()

        if game.won:
            screen.update_status("You Win!")
        else:
            screen.update_status(f"You Lose!\n word was: {game._word}")
        with term.cbreak():
            _ = term.inkey()


if __name__ == "__main__":
    main()
