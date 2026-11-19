{{ fullname | escape | underline}}

{#
  `func3`'s numpydoc References section is documented on the `auto-module` page only. numpydoc turns it into
  citations, and Sphinx citations are global, so documenting it on both pages would define them twice: Sphinx warns
  about a duplicate citation and keeps one. A project cites one source from several places by defining it once.
#}
.. automodule:: {{ fullname }}
   :members:
   :exclude-members: func3
   {% block modules %}
   {% if modules %}
   .. rubric:: {{ _('Sub Modules') }}
   .. autosummary::
      :toctree:
      :template: custom-module-template.rst
      :recursive:
   {% for item in modules %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   .. rubric:: {{ _('Classes and Functions') }}
