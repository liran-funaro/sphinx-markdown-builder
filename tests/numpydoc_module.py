"""
Example module with numpydoc-style docstrings.

It is only documented by the numpydoc build (``-t numpydoc``), so it lives outside ``my_module``.
"""


def downside_risk(returns, min_acceptable_return=0.0):
    """
    Compute the downside risk of a series of returns.

    Parameters
    ----------
    returns : ndarray of shape (n_observations,)
        The observed returns.
    min_acceptable_return : float, optional
        Returns below this value count as downside.

    Returns
    -------
    risk : float
        The downside risk.
    """
    return 0.0
