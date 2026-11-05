:orphan:

Signature headings
==================

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

   Both signatures have the same heading level.

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

   Details belong under the function.

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

   .. py:method:: capped_method()

Level six
+++++++++

.. py:function:: at_six()

Level seven
###########

.. py:function:: at_seven()

Sibling section
---------------

.. py:function:: restored_section()
