import numpy as np
from functools import reduce
from numbers import Number
from numpy.linalg import det, pinv, matrix_rank, norm

from .linalg_util import is_diagonal, is_stochastic, is_square, mult


# td_key
# td_A
# td_b
# td_D
# td_e

# etd_key
# etd_A
# etd_b
# etd_m
# etd_f
# etd_i

# common

def propagator(A):
    """ A |--> (I - A)

    NB: Somewhat iffy terminology`
    """
    assert(is_square(A))
    I = np.eye(len(P))
    return (I - A)


def potential(A, tol=1e-6):
    """Compute the potential matrix
    ret = (I - M1*M2*...)^{-1}
    """
    assert(is_square(A))
    I = np.eye(len(A))
    ret = np.linalg.inv(I - A)
    ret[np.abs(ret) < tol] = 0 # zero values within tolerance
    return ret


def bellman(P,G,r):
    """Compute the solution to the Bellman equation."""
    assert(is_stochastic(P))
    assert(is_diagonal(G))
    I = np.eye(len(P))
    return np.dot(np.linalg.inv(I - np.dot(G,P)), r)


def least_squares(P, G, X, r):
    """Compute the optimal weights via least squares."""
    v = bellman(P, G, r)
    D = mdputils.distribution_matrix(P)
    return np.array(mult(np.linalg.pinv(mult(X.T, D, X)), X.T, D, v))


def warp(P, G, L):
    """
    The matrix which warps the distribution due to gamma and lambda.
    warp = (I - P_{\pi} \Gamma \Lambda)^{-1}
    NB: "warp matrix" is non-standard terminology.

    P : The transition matrix (under a policy)
    G : Diagonal matrix, diag([gamma(s_1), ...])
    L : Diagonal matrix, diag([lambda(s_1), ...])
    """
    assert(is_stochastic(P))
    assert(is_diagonal(G))
    assert(is_diagonal(L))
    return potential(P @ G @ L)

# TD

def td_solution(P, G, L, X, r):
    D = mdputils.distribution_matrix(P)
    A = mult(X.T, D, resolvent(P, G), X)
    A_inv = np.linalg.pinv(A)
    b = mult(X.T, D, r)
    return np.array(np.dot(A_inv, b))

# ETD

def etd_solution(P, G, L, X, ivec, r):
    # compute intermediate quantities (could be more efficient)
    di = mdputils.stationary(P) * ivec
    m = mult(resolvent(L, G, P.T), potential(G, P.T), di)
    M = np.diag(m)

    # solve the equation
    A = mult(X.T, M, potential(P, G, L), resolvent(P, G), X)
    A_inv = np.linalg.pinv(A)
    b = mult(X.T, M, potential(P, G, L), r)
    return np.array(np.dot(A_inv, b))

def followon_vector(P, G, di):
    """Compute the followon trace."""
    assert(is_stochastic(P))
    assert(is_diagonal(G))
    I = np.eye(len(P))

    return np.dot(np.linalg.inv(I - np.dot(G, P.T)), di)

def followon(P,G,di):
    """Compute the follown matrix."""
    return np.diag(np.ravel(followon_vector(P,G,di)))
