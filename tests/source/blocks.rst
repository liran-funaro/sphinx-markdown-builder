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


Referencing terms from a glossary
---------------------------------

Some other text that refers to :term:`Glossary2-Term2`.


Http domain directive
---------------------

.. http:get:: /users/(int:user_id)/posts/(tag)


C domain
--------

.. c:function:: PyObject *PyType_GenericAlloc(PyTypeObject *type, Py_ssize_t nitems)

Inline tabs
-----------

.. tab:: First tab

   Content of the first tab.

.. tab:: Second tab

   Content of the second tab.

Same-page references
--------------------

See `Same-page references`_.

Citations
---------

A citation reference [CIT2002]_ on the same page.

.. [CIT2002] A citation definition.
