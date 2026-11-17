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

A raw block indented after a paragraph is in a block quote.

A raw block indented right after a paragraph is a definition

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

<a id="javascript-domain"></a>

## JavaScript domain

<a id="no_params"></a>

### no_params()

No parameters in a JavaScript signature.

<a id="all_required"></a>

### all_required(a, b, c)

No optional parameters in a JavaScript signature.

<a id="empty_param_name"></a>

### empty_param_name(a, b)

Empty parameter name in a JavaScript signature.

<a id="empty_opt_param_name"></a>

### empty_opt_param_name(a, b[, ])

Empty optional parameter in a JavaScript signature.

<a id="mid_empty_param_name"></a>

### mid_empty_param_name(a[, ], b)

Middle empty optional parameter in a JavaScript signature.

<a id="last_required"></a>

### last_required([a, ][b, ]c)

Last parameter is required.

<a id="multiple"></a>

### multiple(a[, b][, c], d)

Multiple required parameter between optional.

<a id="span"></a>

### span([start, ]stop[, step])

Optional parameters in a JavaScript signature.

<a id="trailing"></a>

### trailing(a[, b[, c]])

Nested optional parameters after a required one.

<a id="middle"></a>

### middle(a[, b], c)

An optional parameter between required ones.

<a id="two_required"></a>

### two_required(a, b[, c])

An optional parameter after two required ones.

<a id="inner_first"></a>

### inner_first([[a, ]b])

A nested optional group as the first item of a group.

<a id="deep"></a>

### deep([[[a, ]b, ]c])

Nested optional groups, each the first item of its group.

<a id="after_required"></a>

### after_required(x[, [a, ]b])

A nested optional group inside an optional group after a required parameter.

<a id="two_groups"></a>

### two_groups([a[, b]][, c, d])

An optional group that contains another, then an optional group with two parameters.

<a id="unbalanced"></a>

### unbalanced(\[\[a\], b\]\])

Unbalanced brackets: Sphinx cannot parse them, so it keeps the signature as text.

<a id="inline-tabs"></a>

## Inline tabs

**First tab**

Content of the first tab.

**Second tab**

*Emphasis* starts the second tab, and a word ends it

**(Third) tab**

A label that starts with punctuation.

<a id="same-page-references"></a>

## Same-page references

See [Same-page references](#same-page-references).
