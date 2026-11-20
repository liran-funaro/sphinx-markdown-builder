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

## Raw blocks

Before the raw blocks, with inline <b>*bold*</b> HTML.

<div class="note">
  <b>*Not* escaped</b>
</div>

| Raw | Markdown |
|-----|----------|
| *a* | b        |

A raw block indented after a paragraph is in a block quote.

> <div>In a block quote</div>

A raw block indented right after a paragraph is a definition
: <div>In a definition</div>

After the raw blocks.

## Referencing terms from a glossary

Some other text that refers to [Glossary2-Term2](glossaries.md#term-Glossary2-Term2).

## Http domain directive

**`GET` `/users/`(*int:* user_id)`/posts/`(tag)**

## C domain

**Function [PyObject](https://docs.python.org/3/c-api/structures.html#c.PyObject) \*`PyType_GenericAlloc`([PyTypeObject](https://docs.python.org/3/c-api/type.html#c.PyTypeObject) \*type, [Py_ssize_t](https://docs.python.org/3/c-api/intro.html#c.Py_ssize_t) nitems)**

## JavaScript domain

**Function `no_params`()**

No parameters in a JavaScript signature.

**Function `all_required`(a, b, c)**

No optional parameters in a JavaScript signature.

**Function `empty_param_name`(a, b)**

Empty parameter name in a JavaScript signature.

**Function `empty_opt_param_name`(a, b[, ])**

Empty optional parameter in a JavaScript signature.

**Function `mid_empty_param_name`(a[, ], b)**

Middle empty optional parameter in a JavaScript signature.

**Function `last_required`([a, ][b, ]c)**

Last parameter is required.

**Function `multiple`(a[, b][, c], d)**

Multiple required parameter between optional.

**Function `span`([start, ]stop[, step])**

Optional parameters in a JavaScript signature.

**Function `trailing`(a[, b[, c]])**

Nested optional parameters after a required one.

**Function `middle`(a[, b], c)**

An optional parameter between required ones.

**Function `two_required`(a, b[, c])**

An optional parameter after two required ones.

**Function `inner_first`([[a, ]b])**

A nested optional group as the first item of a group.

**Function `deep`([[[a, ]b, ]c])**

Nested optional groups, each the first item of its group.

**Function `after_required`(x[, [a, ]b])**

A nested optional group inside an optional group after a required parameter.

**Function `two_groups`([a[, b]][, c, d])**

An optional group that contains another, then an optional group with two parameters.

**Function `unbalanced`(\[\[a\], b\]\])**

Unbalanced brackets: Sphinx cannot parse them, so it keeps the signature as text.

## Inline tabs

**First tab**

Content of the first tab.

**Second tab**

*Emphasis* starts the second tab, and a word ends it

**(Third) tab**

A label that starts with punctuation.

**A bold label**

A label in bold, like the tab labels themselves.

* **Bold and *italic* name:**
  A field name is bold too, so the bold inside it does nothing, and the italic stays.

## Sphinx Design

A card title

Body text.

[https://example.com](https://example.com)

Second card

Second body.

[https://example.org](https://example.org)

## Same-page references

See [Same-page references](#same-page-references).

## Targets

A footnote <sup>[1](#target-note)</sup>, and links to [the footnote alias](#the-footnote-alias) and [the paragraph alias](#the-paragraph-alias).

<a id="the-footnote-alias"></a>
* <a id='target-note'>**[1]**</a> A footnote with a target right before it, which keeps its own id.

<a id="the-paragraph-alias"></a>

A paragraph with a target right before it, which moves its id onto the paragraph.

## Citations

A citation reference <sup>[CIT2002](#cit2002)</sup> on the same page.

An external link to [the same anchor](https://example.org/#cit2002) is not a citation.

A link labeled like a citation, [\[CIT2002\]](https://example.org/), is not a citation either.

A cross-reference to the citation keeps its own text and stays a link: [`CIT2002`](#cit2002).

A link to [the citation alias](#the-citation-alias), a target right before the citation, which keeps its own id.

<a id="the-citation-alias"></a>
* <a id='cit2002'>**[CIT2002]**</a> A citation definition.
