# Dig up 

A cli-tool that helps you dig up knowledge from Python legacy code.

## How to use

Install it along your python project:
```bash
pip install digup
```

### Word count

Display the word count at the codebase level:
```bash
digup wc | head -n 20

# (digup312) lxnd@dune digup % digup wc | head -n 15
# 38 modules
# --------------------------------------------------
# word                                    occurences
# --------------------------------------------------
# self                                            81
# str                                             59
# node                                            52
# int                                             50
# code                                            48
# list                                            38
# Word                                            38
# WordCount                                       36
# args                                            36
# Path                                            30
# functions                                       26
```

Display the wordcount of a long function:
```bash
digup wc -f my_long_function
#demo.py::my_long_function: 
#------------------------------------------------------------------------
#word                                             #      span  proportion
#------------------------------------------------------------------------
#print                                           11        22         34%
#count                                            8        15         23%
#match                                            6         8         12%
#status                                           6        26         40%
#ip_counts                                        4        37         57%
#defaultdict                                      4         4          6%
#int                                              4         4          6%
#ip                                               4        20         31%
#url                                              4        22         34%
#day                                              4        23         35%
```

> 💡 A high number of occurrences with a low proportion is a sign of something that can be extracted.

Display the help:
```
digup wc --help
```

### List the modules, the classes, the functions

```bash

digup ls     # list of modules of the current directory (recursively)
digup ls -f  # list of modules of the current directory (recursively)
digup ls -c  # list of modules of the current directory (recursively)
```

List the 10 longest functions, sorted by length:
```bash
digup ls -f --sort -n 10

# 10/99 functions
# ------------------------------------------------------------------------------------------------------------------------
# functions                                                                                                         length
# ------------------------------------------------------------------------------------------------------------------------
# src/cli.py::main                                                                                                      87
# drafts/my_long_function.py::my_long_function                                                                          65
# src/termcolor.py::colored                                                                                             58
# src/highlight_identifiers.py::highlight_identifiers                                                                   43
# src/termcolor.py::_can_do_colour                                                                                      31
# drafts/test_compute_word_count_with_parso.py::word_counts                                                             29
# src/termcolor.py::cprint                                                                                              28
# src/count_words.py::word_count                                                                                        27
# tests/word_count/test_compute_word_count_on_a_function.py::test_a_complex_case                                        27
# src/colors.py::_hsv_to_rgb                                                                                            26
```

Display the help:
```bash
digup ls -h
```

### Highlight the identifiers

```
digup hi -f highlight_identifiers
```

![](docs/highlight_example.png)

## Developer documentation

### How to install the project

```bash
python -m venv ../venvs/digup312
source ../venvs/digup312
python -m ensurepip --upgrade
python -m pip install setuptools --upgrade
python -m pip install -r requirements.txt

# To be able to run `digup` cli in the project
python -m pip install -e .
```

### How to publish a new version

1. Increment the version in [pyproject.toml](pyproject.toml).
2. Type `make release`
