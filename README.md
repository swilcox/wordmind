# wordmind
[![codecov](https://codecov.io/gh/swilcox/wordmind/branch/main/graph/badge.svg?token=K2K5CI21NN)](https://codecov.io/gh/swilcox/wordmind)

a silly wordle knockoff for the command-line

## Prerequisites
* Install [rye](https://rye-up.com/) on your system.
* From a command prompt in the project directory, type `rye sync`.

## how to run

### to play normally with default options

```sh
rye run python wordmind.py
```

### to have the computer play for a particular answer word and speed up animations

```sh
rye run python wordmind.py --auto --solution drink --speed 50
```

## To Run Tests

```sh
rye run pytest
```

## Things to do still

- greater coverage of tests
- tests for guesser and cli
- possibly remove colorama to just use blessed
