# wordmind
[![codecov](https://codecov.io/gh/swilcox/wordmind/branch/main/graph/badge.svg?token=K2K5CI21NN)](https://codecov.io/gh/swilcox/wordmind)

a silly wordle knockoff for the command-line

## Prerequisites
* Install [uv](https://docs.astral.sh/uv/getting-started/installation/) on your system.
* From a command prompt in the project directory, type `uv sync`.

## how to run

### to play normally with default options

```sh
uv run wordmind
```

### to have the computer play for a particular answer word and speed up animations

```sh
uv run wordmind --auto --solution drink --speed 50
```

## To Run Tests (with Coverage)

```sh
uv run pytest --cov
```

## Things to do still

- greater coverage of tests
- tests for guesser and cli
- possibly remove colorama to just use blessed
