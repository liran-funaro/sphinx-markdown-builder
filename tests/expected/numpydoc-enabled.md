<meta name="author" content="Liran Funaro"/>
<meta name="copyright" content="Copyright (c) 2023-2026, Liran Funaro."/>
<meta name="version" content="0.6.11"/>

<a id="numpydoc"></a>

# Numpydoc

Parameter types in numpydoc-style docstrings are rendered as definition list classifiers.

<a id="numpydoc_module.downside_risk"></a>

### downside_risk(returns, min_acceptable_return=0.0)

Compute the downside risk of a series of returns.

* **Parameters:**
  **returns** : *ndarray of shape (n_observations,)*
  : The observed returns.

  **min_acceptable_return** : *float, optional*
  : Returns below this value count as downside.
* **Returns:**
  **risk** : *float*
  : The downside risk.

<!-- !! processed by numpydoc !! -->
