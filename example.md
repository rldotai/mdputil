An example that is also a doctest.


# Working with MDPs

    >>> import mdputil
    
## Generating A Random Transition Matrix

    >>> P = mdputil.rand_p(5)
    
### Check the properties of the transition matrix

    >>> mdputil.is_matrix(P)
    True
    >>> mdputil.is_square(P)
    True
    >>> mdputil.is_nonnegative(P)
    True
    >>> mdputil.is_periodic(P)
    False
    >>> mdputil.is_reducible(P)
    False
    >>> mdputil.is_stochastic(P)
    True
    >>> mdputil.is_substochastic(P)
    True
    >>> mdputil.is_ergodic(P)
    True
    >>> mdputil.is_absorbing(P)
    False

### Operations on the matrix

    >>> mdp.get_period(P)
    1
    >>> 