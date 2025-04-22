# Items selection

3 mécanismes entre en jeu : 
- l'ensemble des fichiers sources
- le filtrage de motif dans ces fichiers sources (fonction, classe)
- le mode d'aggrégation

I want to apply a wordcount to : 
- a function
- a class
- a module
- a package (several modules)
- the codebase (several modules)

It would be nice to have flexibility (so I don't have to type the exact identifier of the element).


This feature is inspired by [pytest filter mecanism](https://docs.pytest.org/en/stable/how-to/usage.html#specifying-which-tests-to-run) :
- pytest -k 'MyClass and not method'
- pytest tests/test_mod.py::test_func

```
tests/test_mod.py::TestClass::test_method
``` 

Looking for a snake_case name can return : 
- nothing
- a single function
- several functions
- a class (context managers use snake_case by convention)
- several classes

Looking for a class can return : 


The aggregation level can be : 
- functions
- class
- module
