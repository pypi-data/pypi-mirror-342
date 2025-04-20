# Dig up 

A cli-tool that helps you dig up knowledge from Python legacy code.

## How to use

Install it along your python project:
```bash
pip install digup
```

Then run
```
digup wc -f my_long_function
```
to display the word count of the function and get hints about what to refactor:
```
demo.py::my_long_function: 
------------------------------------------------------------------------
word                                             #      span  proportion
------------------------------------------------------------------------
print                                           11        22         34%
count                                            8        15         23%
match                                            6         8         12%
status                                           6        26         40%
ip_counts                                        4        37         57%
defaultdict                                      4         4          6%
int                                              4         4          6%
ip                                               4        20         31%
url                                              4        22         34%
day                                              4        23         35%
```

```bash

digup tree     # display the list of modules
digup tree -f  # display the list of functions

# the codebase wordcount
digup wc

# the word count of all functions
digup wc -f

# the word count of the function my_long_function
# (to be precise, all the functions that contains my_long_function)
digup wc -f my_long_function

digup wc -c MyClass


digup wc -d tests/test_data/selecting_class/a_class_in_a_sub_directory/
```

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

### How to public a new version

Increment the version in [pyproject.toml](pyproject.toml).

Delete the previous artefacts
```bash
rm dist/*
```

Build the project
```
python -m build
```

Upload the artefacts
```
python -m twine upload dist/*
```