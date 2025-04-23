# loop-to-recursion

[![Test](https://github.com/koyuki7w/loop-to-recursion/actions/workflows/test.yml/badge.svg)](https://github.com/koyuki7w/loop-to-recursion/actions/workflows/test.yml)

## Description

Convert the given Python code into an equivalent code without for/while loops

## Install

```
pip install loop-to-recursion
```

## Usage
```
$ cat sample.py
def function(x):
    l, r = 0, x + 1
    while r - l != 1:
        m = (r + l) // 2
        if x < m * m:
            r = m
        else:
            l = m
    return l
$ loop-to-recursion sample.py
$ cat sample.py
def function(x):
    m = None
    l, r = (0, x + 1)

    def _while_1(m, r, l, /):
        if r - l != 1:
            m = (r + l) // 2
            if x < m * m:
                r = m
            else:
                l = m
            return _while_1(m, r, l)
        else:
            return (m, r, l)
    m, r, l = _while_1(m, r, l)
    return l
```
