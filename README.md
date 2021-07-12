coppertop - some batteries python didn't come with

#### @pipeable

The purpose of the coppertop pipe operator is to allow code to be written in 
a more essay style format - i.e. left-to-right and top-to-bottom. The idea is 
to make it easy to express the syntax (aka sequence) of a solution.

@pipable provides for a few different syntaxes but here we focus on the three 
main ones unary, binary and ternary.

##### partial application

syntax: `f(..., a) -> f(...)`  
where `...` is used as a sentinel place-holder for future arguments


##### unary - takes 1 piped argument and 0+ called arguments

syntax: `A >> f(args)` -> `f(args)(A)`

```
from coppertop.bits import pipeable
from coppertop.std import _, anon

@pipeable
def addOne(x):
    return x + 1

@pipeable
def appendStr(x, y):
    assert isinstance(x, str) and isinstance(y, str)
    return x + y

1 >> addOne
"hello" >> appendStr(_," ") >> appendStr(_, "world!")

1 >> anon(lambda x: x +1)
```

##### binary - takes 2 piped argument and 0+ called arguments

syntax: `A >> f(args) >> B` -> `f(args)(A, B)`

```
from coppertop.bits import NotYetImplemented
from coppertop.std import each, inject

@pipeable(flavour=binary)
def add(x, y):
    return x + y

@pipeable(flavour=binary)
def op(x, action, y):
    if action == "+":
        return x + y
    else:
        raise NotYetImplemented()

1 >> add >> 1
1 >> op(_,"+",_) >> 1
[1,2] >> each >> (lambda x: x + 1)
[1,2,3] >> inject(_,0,_) >> (lambda x,y: x + y)
```

##### ternary -  - takes 3 piped argument and 0+ called arguments

syntax: `A >> f(args) >> B >> C` -> `f(args)(A, B, C)`

```
from coppertop.std import both, assertEqual

[1,2] >> both >> (lambda x, y: x + y) >> [3,4] >> assertEqual >> [4, 6]
```

##### as an exercise for the reader
```
[1,2] >> both >> (lambda x, y: x + y) >> [3,4] 
   >> each >> (lambda x: x * 2)
   >> inject(_,1,_) >> (lambda x,y: x * y)
   >> addOne >> addOne >> addOne
   >> to(str) >> appendStr(" red balloons go by")
   >> assertEqual >> ???
```

----

In progress - Julia style multi-dispatch with an algebraic type system
