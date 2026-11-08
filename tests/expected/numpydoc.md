# Numpydoc

Built with the `numpydoc` extension, which renders parameter types as definition list classifiers.

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
