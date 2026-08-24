============
Math Example
============

Formula 1
   Definition of the formula as inline math:
   :math:`\frac{ \sum_{t=0}^{N}f(t,k) }{N}`.

   Some more text related to the definition.


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
   :caption: example.py

   usage: command [-h] [--option1 VALUE1]
                  [--option2 VALUE2]
                  [--option3 VALUE3]
                  argument


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


Referencing terms from a glossary
---------------------------------

Some other text that refers to :term:`Glossary2-Term2`.


Http domain directive
---------------------

.. http:get:: /users/(int:user_id)/posts/(tag)


C domain
--------

.. c:function:: PyObject *PyType_GenericAlloc(PyTypeObject *type, Py_ssize_t nitems)


Abbreviations
-------------

The :abbr:`LIFO (last-in, first-out)` queue.

An abbreviation without an explanation: :abbr:`HTML`.

An abbreviation with a quote in its explanation: :abbr:`API (Application "Programming" Interface)`.
