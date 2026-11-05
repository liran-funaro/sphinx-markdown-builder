:orphan:

Object signatures
=================

.. py:function:: top_level()

   .. rubric:: Object rubric

   .. topic:: Object topic

      Topic text.

   .. list-table:: Object table
      :header-rows: 1

      * - Heading
      * - Cell

.. py:method:: Standalone.method()

.. py:class:: Outer

   .. py:attribute:: value

   .. py:method:: method()

   .. py:class:: Inner

      .. py:method:: method()

   .. py:method:: sibling()

.. py:function:: after_class()

.. py:function:: overloaded(value: int)
                 overloaded(value: str)

   Both signatures are separate paragraphs.

.. autofunction:: my_module.func1
   :no-index:

Section
-------

.. py:function:: in_section()

Subsection
~~~~~~~~~~

.. py:function:: in_subsection()

   Details
   ^^^^^^^

   Details remain a document section.

   More details
   """"""""""""

   A nested docstring section.

   .. py:class:: Local

      .. py:method:: method()

.. py:function:: after_docstring()

Level four
^^^^^^^^^^

.. py:function:: at_four()

Level five
""""""""""

.. py:class:: AtFive

   .. py:method:: deep_method()

Level six
+++++++++

.. py:function:: at_six()

Level seven
###########

.. py:function:: at_seven()

Sibling section
---------------

.. py:function:: restored_section()

Signature markup
----------------

.. py:function:: generic[T](value: list[T], *args, marker="*`<tag>", **kwargs) -> list[T]

.. cpp:class:: Box

   .. cpp:function:: template<typename T> T *get(T *value)

   .. cpp:class:: Inner

      .. cpp:member:: int value

.. c:function:: int *lookup(const char *name)

.. js:class:: Widget(options)

   .. js:method:: run(value)

.. rst:directive:: sample

.. option:: --sample <value>

.. describe:: raw *name* `value` <tag>

.. describe:: `edge`

.. http:get:: /objects/(int:object_id)

   An HTTP signature.
