<meta name="author" content="Liran Funaro"/>
<meta name="copyright" content="Copyright (c) 2023-2026, Liran Funaro."/>
<meta name="version" content="0.6.11"/>

<a id="math-example"></a>

# Math Example

Formula 1
: Definition of the formula as inline math: $\frac{ \sum_{t=0}^{N}f(t,k) }{N}$.
  <br/>
  Some more text related to the definition.

Display math:

$$
\begin{aligned}
x &= 1 \\
y &= 2
\end{aligned}
$$

<a id="code-example"></a>

# Code Example

```pycon
>>> print("first line\nsecond line")
first line
second line
```

<a id="multi-line-code-block"></a>

## Multi-line Code Block

```console
usage: command [-h] [--option1 VALUE1]
               [--option2 VALUE2]
               [--option3 VALUE3]
               argument
```

```default
x = 1
```

```python
docutils_code_directive = True
```

```python
class_before_language = True
```

```yaml
key: value
```

```python
"""Configuration file for the Sphinx documentation builder."""
import sys
from pathlib import Path

mod_path = Path(__file__).parent.parent.absolute()
if mod_path not in sys.path:
    sys.path.insert(0, str(mod_path))
```

A literal block after a `highlight` directive:

```c
int x = 1;
```

Inline: ``a`b`` and `` `x` ``.

````markdown
```python
x = 1
```
````

<a id="line-block"></a>

# Line Block

text sub text
<br/>
more text
<br/>
<br/>
<br/>

<a id="other-text"></a>

## Other text

other text

<a id="text-that-looks-like-markdown"></a>

## Text that looks like Markdown

\# not a heading

\> not a quote

Text with \[brackets\](not a link) and List\<int>.

reStructuredText would start a list at these markers, but not on the continuation lines of a paragraph: 1. not a list 2) not a list + not a list - 5 degrees overnight, a mid-line - stays.

<a id="raw-blocks"></a>

## Raw blocks

Before the raw blocks, with inline  HTML.

| Raw | Markdown |
|-----|----------|
| *a* | b        |

After the raw blocks.

<a id="referencing-terms-from-a-glossary"></a>

## Referencing terms from a glossary

Some other text that refers to [Glossary2-Term2](https://localhost/glossaries.html#term-Glossary2-Term2).

<a id="http-domain-directive"></a>

## Http domain directive

<a id="get--users-(int-user_id)-posts-(tag)"></a>

### GET /users/(*int:* user_id)/posts/(tag)

<a id="c-domain"></a>

## C domain

<a id="c.PyType_GenericAlloc"></a>

### [PyObject](https://docs.python.org/3/c-api/structures.html#c.PyObject) \*PyType_GenericAlloc([PyTypeObject](https://docs.python.org/3/c-api/type.html#c.PyTypeObject) \*type, [Py_ssize_t](https://docs.python.org/3/c-api/intro.html#c.Py_ssize_t) nitems)

<a id="inline-tabs"></a>

## Inline tabs

Content of the first tab.

Content of the second tab.

<a id="same-page-references"></a>

## Same-page references

See [Same-page references](#same-page-references).
