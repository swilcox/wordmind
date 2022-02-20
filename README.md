# wordmind
a silly wordle knockoff for the command-line

## how to run

Once you're inside a virtualenv with the necessary requirements:

### to play normally with default options

```sh
python wordmind_cli.py
```

### to have the computer play for a particular answer word and speed up animations

```sh
python wordmind_cli.py --auto true --solution drink --speed 50
```


## Things to do still

- switch off of pipenv
- coverage for tests
- greater coverage of tests
- tests for guesser and cli
- possibly remove colorama to just use blessed
