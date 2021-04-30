coppertop - some batteries python didn't come with

1) a decorator that adds pipeing to functions
2) some d-style ranges
3) misc

#### piping

##### unary - takes 1 piped argument and 0+ called arguments
1 >> addOne

1 >> add(1)

##### binary - takes 2 piped argument and 0+ called arguments

1 >> add >> 1
1 >> op(_,"+",_) >> 1

##### ternary -  - takes 3 piped argument and 0+ called arguments

[1,2] >> both >> (lambda x, y: x + y) >> [3,4] >> assertEqual >> [4, 6]


----

In progress - Julia style multidispatch with an algebraic type system
