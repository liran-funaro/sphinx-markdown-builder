============
Math Example
============

Formula 1
   Definition of the formula as inline math:
   :math:`\frac{ \sum_{t=0}^{N}f(t,k) }{N}`.

   Some more text related to the definition.

Formula 2 : float : optional
   A term with classifiers (e.g., numpydoc parameter types).

Formula 3 : *float*
   An already-emphasized classifier.


Display math:

.. math::

      \begin{aligned}
      x &= 1 \\
      y &= 2
      \end{aligned}


============
Code Example
============

>>> print("first line\nsecond line")
first line
second line

Multi-line Code Block
---------------------

.. code-block:: console

   usage: command [-h] [--option1 VALUE1]
                  [--option2 VALUE2]
                  [--option3 VALUE3]
                  argument

.. code-block::
   :class: code

   x = 1

.. code:: python

   docutils_code_directive = True

.. code-block:: python
   :class: extra

   class_before_language = True

.. sourcecode:: yaml

   key: value

.. literalinclude:: conf.py
   :language: python
   :lines: 1-7

.. highlight:: c

A literal block after a ``highlight`` directive::

   int x = 1;

.. highlight:: default

Inline: ``a`b`` and ```x```.

.. code-block:: markdown

   ```python
   x = 1
   ```


==========
Line Block
==========

| text
  sub text
| more text
|
|


Other text
----------

other text


Text that looks like Markdown
-----------------------------

# not a heading

> not a quote

Text with [brackets](not a link) and List<int>.

reStructuredText would start a list at these markers, but not on the continuation lines of a paragraph:
1. not a list
2) not a list
+ not a list
- 5 degrees overnight, a mid-line - stays.


Raw blocks
----------

.. role:: raw-html(raw)
   :format: html

Before the raw blocks, with inline :raw-html:`<b>*bold*</b>` HTML.

.. raw:: html

   <div class="note">
     <b>*Not* escaped</b>
   </div>

.. raw:: markdown

   | Raw | Markdown |
   |-----|----------|
   | *a* | b        |

.. raw:: latex

   \newpage

A raw block indented after a paragraph is in a block quote.

   .. raw:: html

      <div>In a block quote</div>

A raw block indented right after a paragraph is a definition
   .. raw:: html

      <div>In a definition</div>

After the raw blocks.


Referencing terms from a glossary
---------------------------------

Some other text that refers to :term:`Glossary2-Term2`.


Http domain directive
---------------------

.. http:get:: /users/(int:user_id)/posts/(tag)


C domain
--------

.. c:function:: PyObject *PyType_GenericAlloc(PyTypeObject *type, Py_ssize_t nitems)

JavaScript domain
-----------------

.. js:function:: no_params()

   No parameters in a JavaScript signature.

.. js:function:: all_required(a, b, c)

   No optional parameters in a JavaScript signature.

.. js:function:: empty_param_name(a, b, )

   Empty parameter name in a JavaScript signature.

.. js:function:: empty_opt_param_name(a, b, [])

   Empty optional parameter in a JavaScript signature.

.. js:function:: mid_empty_param_name(a, [], b)

   Middle empty optional parameter in a JavaScript signature.

.. js:function:: last_required([a], [b], c)

  Last parameter is required.

.. js:function:: multiple(a, [b], [c], d)

  Multiple required parameter between optional.

.. js:function:: span([start, ]stop[, step])

   Optional parameters in a JavaScript signature.

.. js:function:: trailing(a[, b[, c]])

   Nested optional parameters after a required one.

.. js:function:: middle(a[, b], c)

   An optional parameter between required ones.

.. js:function:: two_required(a, b[, c])

   An optional parameter after two required ones.

.. js:function:: inner_first([[a], b])

   A nested optional group as the first item of a group.

.. js:function:: deep([[[a, ]b, ]c])

   Nested optional groups, each the first item of its group.

.. js:function:: after_required(x[, [a], b])

   A nested optional group inside an optional group after a required parameter.

.. js:function:: two_groups([a[, b]], [c, d])

   An optional group that contains another, then an optional group with two parameters.

.. js:function:: unbalanced([[a], b]])

   Unbalanced brackets: Sphinx cannot parse them, so it keeps the signature as text.

Inline tabs
-----------

.. tab:: First tab

   Content of the first tab.

.. tab:: Second tab

   *Emphasis* starts the second tab, and a word ends it

.. tab:: (Third) tab

   A label that starts with punctuation.

.. tab:: **A bold label**

   A label in bold, like the tab labels themselves.

:**Bold** and *italic* name: A field name is bold too, so the bold inside it does nothing, and the italic stays.

Sphinx Design
-------------

.. card:: A card title
   :link: https://example.com

   Body text.

.. card:: Second card
   :link: https://example.org

   Second body.

Same-page references
--------------------

See `Same-page references`_.

Targets
-------

A footnote [#target-note]_, and links to `the footnote alias`_ and `the paragraph alias`_.

.. _the footnote alias:

.. [#target-note] A footnote with a target right before it, which keeps its own id.

.. _the paragraph alias:

A paragraph with a target right before it, which moves its id onto the paragraph.

Citations
---------

A citation reference [CIT2002]_ on the same page.

An external link to `the same anchor <https://example.org/#cit2002>`_ is not a citation.

A link labeled like a citation, `[CIT2002] <https://example.org/>`__, is not a citation either.

A cross-reference to the citation keeps its own text and stays a link: :any:`CIT2002`.

A link to `the citation alias`_, a target right before the citation, which keeps its own id.

.. _the citation alias:

.. [CIT2002] A citation definition.
