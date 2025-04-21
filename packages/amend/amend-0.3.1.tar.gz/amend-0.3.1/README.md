# Amend

Ensure your values are right

![GitHub License](https://img.shields.io/github/license/suflaj/amend?style=flat-square)

![GitHub Tag](https://img.shields.io/github/v/tag/suflaj/amend?style=flat-square)

![GitHub Repo stars](https://img.shields.io/github/stars/suflaj/amend?style=flat-square) ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/suflaj/amend/total?style=flat-square) ![GitHub repo size](https://img.shields.io/github/repo-size/suflaj/amend?style=flat-square)


## Motivation

Often times I write a lot of boilerplate code to validate and correct certain values. I have decided to create a package to stop doing it for some of the things I use. The goals of this package:

- perform routine type validation and correction (amend!)
- do not rely on third-party libraries
  - if it's outside standard Python, amends should be handled by package maintainers
- do not overcomplicate things
  - what can easily be done with a processing pipeline should be done with a processing pipeline

Using this, hopefully, writing argument parsers and ensuring correctness in functionality should be slightly easier, while forcing people to explicitly handle more elaborate and specific use cases.

## Installation

You can install this with pip:

```bash
pip install amend
```

Alternatively, you can install this from source:
```
git clone git@github.com:suflaj/amend.git
cd amend
pip install .
```

## Running tests

Amend uses your run-of-the-mill `unittest`. Therefore, to test the whole package, you can simply do:

```bash
python3 -m unittest amend.testing
```

If you wish to test some specific module you can reference the testing module with unittest. For example, if you want to unit test built-in amendments, do:

```bash
python3 -m unittest amend.testing.unit.built_in
```

For more info on how to use `unittest`, look [here](https://docs.python.org/3/library/unittest.html).

## Things to do

This package is in beta. For it to reach a full release it will need to receive:

- ReadTheDocs documentations
- usage examples
- some actual usage (will start to substitute my boilerplate for it)

Currently, it wasn't battle tested. I put in some effort to write it well, but not necessarily optimally. However, even though I do not recommend you use this for production, you can use it for many things, and presumably it should work. If it doesn't, [create an issue](https://github.com/suflaj/amend/issues). The format doesn't really matter currently.
