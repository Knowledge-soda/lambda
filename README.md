# Lambda calculus interpreter

Made by: Jakov Manjkas

With same rules as normaln lambda calculus, use `\` for $\lambda$ symbol. Every variable has one letter in the beggining and has optional natural number after it.

Sample usage:
```
$ python3 main.py
\> Z = (\f x . x) 
\> S = (\n f x . f (n f x)) 
\> S Z
= (\f (\x (f x)))
\> S (S Z)
= (\f (\x (f (f x))))
\> S (S Z) (\x . x x) 
= (\x ((x x) (x x)))
\> (\x . x (\x1 x2 . x2) x)
= (\x ((x (\x1 (\x2 x2))) x))
```
