# Lambda calculus interpreter

Made by: Jakov Manjkas

## Syntax
Variables consist of single lowercase letter, optionally followed by a number: `v12`, `x`, `y`, `z0`, `s22`.

Terms are made by combining variables by application and abstraction.  Parenthesis `(` and `)` can be used for grouping.
Application is denoted by writing one subterm after another (with or without space): `xy`, `a p12`.
Abstraction is denoted by writing `λ` or `\` followed by one or more variables, then `.` then subterm: `\fx.x`, `\a.aa`, `\b.b(\a.ba)`. Dot may be ommited if subterm begins with `(`.

Writing a single term on a line will calculate term's $\beta$ normal form.

Terms can have aliases, alias name (also called termname) starts with upercase letter and can contain letters and numerals, i.e. `A`, `Omega`, `W11`

Assigning a term to it's alias is done with `=` operator.  Simple assignment doesn't cause calculating normal form.
Assigning a term's normal form to an alias is done with `<=` operator.
On lines which have assignment operators no output will be written.  Left hand side of the operator must be a valid termname.

There are three testing operators:
- `==` tests if two terms are $\alpha$ convertible.
- `->` tests if right term is normal form of the left term (will compute normal form of the left hand side)
- `~` tests if two terms have the same normal form (will compute normal form of the right hand side)

Sample usage:
```
$ python3 main.py
λ> D = \x.xx
λ> Omega = D D
λ> K = \xy.x
λ> I = \a.a
λ> K I Omega
-> λa . a
= I
λ> ZERO = \fx.x
λ> Sc = \nfx.f(nfx) 
λ> ONE <= Sc ZERO 
λ> TWO <= Sc ONE 
λ> TWO
-> λf x . f (f x)
λ> \ab.a(ab) == TWO
True
λ> THREE <= Sc TWO
λ> FOUR <= Sc THREE
λ> Plus = \mn.n Sc m
λ> Plus TWO TWO
-> λf x . f (f (f (f x)))
= FOUR
λ> Plus TWO TWO == FOUR
False
λ> Plus TWO TWO -> FOUR
True
λ> Plus TWO TWO -> Plus ONE THREE
False
λ> Plus TWO TWO ~ Plus ONE THREE
True
```
