# Highlight identifiers


I want a tool that highlight identifiers.

Given a file `code.py` with a function 
```
def my_function(a, b):
   l1 = [a]
   l2 = [b]
   return l1 + l2
```

It would be used like this
```bash
# Highlight all the identifiers of the function
digup highlight -f my_function

# Highlight only the word a
digup highlight -f my_function -w a
```
