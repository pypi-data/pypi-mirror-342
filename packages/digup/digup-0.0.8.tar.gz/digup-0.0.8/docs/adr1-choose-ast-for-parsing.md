## Metas
- Date: 2025-05-05
- Author: Alexandre

## Context

I want to implement a word count on functions.

It would turn
```python
def process_items(items):
    if not items:
        log("No items to process.")
        return

    for item in items:
        if is_valid(item):
            handle(item)
```

into
```
word                         #      span  proportion
----------------------------------------------------
items                        3         6         75%
log                          1         1         12%
item                         3         3         38%
is_valid                     1         1         12%
handle                       1         1         12%
```

To do so, I need to : 

- count the identifier of a function
- note the lineno they first appear
- note the lineno they last appear
- know the length of the surrounding function

## Considered Options

### Parsing the source code line by line

Pros : 
- ✅ no dependency

Cons : 
- ❌ very low level


### Using AST

Pros : 
- ✅ included in the standard library
- ✅ well documented
- ✅ fast

Cons : 
- ❌ design a bit awkward (ie ast.arg isn't a subclass of ast.name)

### Using Parso

Pros : 
- ✅ give precise positions (line, column)
- ✅ offer simple navigation
- ✅ opensource
- ✅ tests cover 90% of the code
- ✅ battle-tested by jedi

Cons : 
- ❌ dependency on a third party lib
- ❌ seems slower than AST - because written in python ([ref](https://github.com/Khan/slicker/issues/30), [ref](https://medium.com/@boxed/a-quick-performance-comparison-of-python-parsers-eb86497ac733))


## Decision

I made my the first draft with parso.

But I will start with ast: it's faster, more standard, and looks simpler to me.

I will consider switching to parso if I miss features.

To facilitate such evolution, I'll try to keep the parsing lib at the edges and work on iterators over custom datastructures.