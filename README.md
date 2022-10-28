[![CI](https://github.com/lpenz/tuzue/actions/workflows/ci.yml/badge.svg)](https://github.com/lpenz/tuzue/actions/workflows/ci.yml)
[![coveralls](https://coveralls.io/repos/github/lpenz/tuzue/badge.svg?branch=main)](https://coveralls.io/github/lpenz/tuzue?branch=main)
[![Documentation Status](https://readthedocs.org/projects/tuzue/badge/?version=latest)](https://tuzue.readthedocs.io/en/latest/?badge=latest)

# tuzue

Fuzzy-filtering menu-based interactive curses interface for python,
plus utilities.


## Library usage

Basic usage of the library is very simple:

```{.py}
import tuzue

fruits = [ "avocado", "berry", "cherry", "durian", "eggfruit" ]
favorite = tuzue.navigate(fruits, "What is your favorite fruit?")
print("Your favorite fruit is", favorite)
```

That generates the following possible interaction:

![demo-navigate](demos/demo-navigate.gif)


## Inspecting in pdb

tuzue is very useful to inspect object trees in [pdb]. Example session
where we use tuzue to inspect itself:

![demo-pdb](demos/demo-pdb.gif)


[pdb]: https://docs.python.org/3/library/pdb.html
