# Math Example

Formula 1
: Definition of the formula as inline math:
  $\frac{ \sum_{t=0}^{N}f(t,k) }{N}$.
  <br/>
  Some more text related to the definition.

Formula 2 : *float* : *optional*
: A term with classifiers (e.g., numpydoc parameter types).

Formula 3 : *float*
: An already-emphasized classifier.

Display math:

$$
\begin{aligned}
x &= 1 \\
y &= 2
\end{aligned}
$$

# Code Example

```pycon
>>> print("first line\nsecond line")
first line
second line
```

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

# Line Block

text
sub text
<br/>
more text
<br/>
<br/>
<br/>

## Other text

other text

## Text that looks like Markdown

\# not a heading

\> not a quote

Text with \[brackets\](not a link) and List\<int>.

reStructuredText would start a list at these markers, but not on the continuation lines of a paragraph:
1\. not a list
2\) not a list
\+ not a list
\- 5 degrees overnight, a mid-line - stays.

## Referencing terms from a glossary

Some other text that refers to [Glossary2-Term2](glossaries.md#term-Glossary2-Term2).

## Http domain directive

### GET /users/(*int:* user_id)/posts/(tag)

## C domain

### [PyObject](https://docs.python.org/3/c-api/structures.html#c.PyObject) \*PyType_GenericAlloc([PyTypeObject](https://docs.python.org/3/c-api/type.html#c.PyTypeObject) \*type, [Py_ssize_t](https://docs.python.org/3/c-api/intro.html#c.Py_ssize_t) nitems)

## Inline tabs

Content of the first tab.

Content of the second tab.

## Same-page references

See [Same-page references](#same-page-references).

## Citations

A citation reference <sup>[CIT2002](#cit2002)</sup> on the same page.

* <a id='cit2002'>**[CIT2002]**</a> A citation definition.
