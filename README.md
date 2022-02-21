# wordmind
a silly wordle knockoff for the command-line

## Prerequisites
* Python 3.9 or higher on your system.
* Install [PDM](https://pdm.fming.dev) on your system.
* From a command prompt in the project directory, type `pdm install`.

## how to run

Once you're inside a virtualenv with the necessary requirements:

### to play normally with default options

```sh
pdm run python3 wordmind.py
```

### to have the computer play for a particular answer word and speed up animations

```sh
pdm run python3 wordmind.py --auto true --solution drink --speed 50
```

## To Run Tests

```sh
pdm run pytest
```

## Things to do still

- coverage for tests
- greater coverage of tests
- tests for guesser and cli
- possibly remove colorama to just use blessed
