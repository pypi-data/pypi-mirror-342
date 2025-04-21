# Wordly

A python client to communicate with servers implementing the
[Dictionary Server Protocol](https://datatracker.ietf.org/doc/html/rfc2229)

## Getting Started

```
pip install wordly
```

## Usage

Once installed you may use wordly from the command line:

```
$ wordly programming
"programming" wn "WordNet (r) 3.0 (2006)"
programming
    n 1: setting an order and time for planned events [syn:
         {scheduling}, {programming}, {programing}]
    2: creating a sequence of instructions to enable the computer to
       do something [syn: {programming}, {programing}, {computer
       programming}, {computer programing}]
.
```

Or you may import `Word` from `wordly` in your scripts.

```py
from wordly import Word

w = Word("curious")

print(w.definition)
```
