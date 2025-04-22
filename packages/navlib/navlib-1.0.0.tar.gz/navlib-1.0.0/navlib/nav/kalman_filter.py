"""
This module provides functions to work with Kalman filters.

Functions:
    kf_lti_discretize: Discretize a Linear Time-Invariant (LTI) system using the matrix fraction decomposition.
    kf_predict: Prediction step of the Kalman filter.
    kf_update: Update step of the Kalman filter.

Authors: Sebastián Rodríguez-Martínez and Giancarlo Troni
Contact: srodriguez@mbari.org
"""

from typing import Tuple

import numpy as np
from scipy.linalg import expm


def kf_lti_discretize(
    Ac: np.ndarray,
    Bc: np.ndarray = None,
    Qc: np.ndarray = None,
    dt: float = 1,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Discretize a Linear Time-Invariant (LTI) system using the matrix fraction decomposition
    for use in a discrete-time Kalman filter.

    Args:
        Ac (np.ndarray): Continuos state transition matrix.
        Bc (np.ndarray): Continuos input matrix, by default None.
        Qc (np.ndarray): Continuos covariance matrix, by default None.
        dt (float): Time step, by default 1.

    Returns:
        transition_mat (np.ndarray): Discrete state transition matrix.
        inpu_mat (np.ndarray): Discrete input matrix.
        covariance_mat (np.ndarray): Discrete covariance matrix.

    Raises:
        TypeError: If Ac, Bc or Qc are not numpy arrays.
        ValueError: If Ac is not a 2D matrix, if Ac and Bc do not have the same number of rows,
            if Qc is not a square matrix, if Qc does not have the same number of rows as Ac.
    """
    # Convert to numpy array
    if isinstance(Ac, list):
        Ac = np.array(Ac)
    if isinstance(Bc, list):
        Bc = np.array(Bc)
    if isinstance(Qc, list):
        Qc = np.array(Qc)

    # Check inputs type
    if not isinstance(Ac, np.ndarray):
        raise TypeError("Ac must be a numpy array")
    if Bc is not None and not isinstance(Bc, np.ndarray):
        raise TypeError("Bc must be a numpy array")
    if Qc is not None and not isinstance(Qc, np.ndarray):
        raise TypeError("Qc must be a numpy array")
    if not isinstance(dt, (int, float)):
        raise TypeError("dt must be a number")

    # Force the input matrix to be a column vector
    if Bc is not None and Bc.ndim == 1:
        Bc = Bc[:, np.newaxis] if Bc.ndim == 1 else np.vstack(Bc)

    # Check that the shape of the matrices is correct
    if Ac.ndim != 2:
        raise ValueError("Ac must be a 2D matrix")
    if Bc is not None and Bc.shape[0] != Ac.shape[0]:
        raise ValueError("Ac and Bc must have the same number of rows")
    if Qc is not None and Qc.shape[0] != Qc.shape[1]:
        raise ValueError("Qc must be a square matrix")
    if Qc is not None and Qc.shape[0] != Ac.shape[0]:
        raise ValueError("Qc must have the same number of rows as Ac")

    # Check the number of states
    n = Ac.shape[0]

    # Default to zero non provided matrices
    if Bc is None:
        Bc = np.zeros([n, 1])

    if Qc is None:
        Qc = np.zeros([n, n])

    # Discretize state transition and input matrix (close form)
    # Ad = expm(Ac*dt)
    M = np.vstack([np.hstack([Ac, Bc]), np.zeros([1, n + 1])])
    ME = expm(M * dt)

    # Discretize state transition and input matrix
    Ad = ME[:n, :n]
    Bd = ME[:n, n:]

    # Discretize Covariance: by (Van Loan, 1978)
    F = np.vstack([np.hstack([-Ac, Qc]), np.hstack([np.zeros([n, n]), Ac.T])])
    G = expm(F * dt)
    Qd = np.dot(G[n:, n:].T, G[:n, n:])

    # # Discretize Covariance: by matrix fraction decomposition
    # Phi = vstack([hstack([Ac,            Qc]),
    #               hstack([np.zeros([n,n]),-Ac.T])])
    # AB  = np.dot (scipy.linalg.expm(Phi*dt), vstack([np.zeros([n,n]),np.eye(n)]))
    # Qd  = np.linalg.solve(AB[:n,:].T, AB[n:2*n,:].T).T

    return Ad, Bd, Qd


def kf_predict(
    x: np.ndarray,
    P: np.ndarray,
    A: np.ndarray = None,
    Q: np.ndarray = None,
    B: np.ndarray = None,
    u: np.ndarray = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prediction step of the Kalman filter.

    Args:
        x (np.ndarray): State mean.
        P (np.ndarray): State covariance.
        A (np.ndarray): State transition matrix, by default None.
        Q (np.ndarray): Process noise covariance, by default None.
        B (np.ndarray): Input matrix, by default None.
        u (np.ndarray): Input vector, by default None.

    Returns:
        updated_state_mean (np.ndarray): Updated state mean.
        updated_state_cov (np.ndarray): Updated state covariance.

    Raises:
        TypeError: If A, Q, B, u, x or P are not numpy arrays.
        ValueError: If A is not a 2D matrix, if x and A do not have the same number of rows,
            if B is not a 2D matrix, if the number of columns in B is not equal to the number of rows in u,
            if B does not have the same number of rows as x, if P is not a square matrix,
            if P is not a square matrix, if Q is not a square matrix, if Q does not have the same number of rows as A.
    """
    # Convert to numpy array
    if isinstance(A, list):
        A = np.array(A)
    if isinstance(Q, list):
        Q = np.array(Q)
    if isinstance(B, list):
        B = np.array(B)
    if isinstance(u, list):
        u = np.array(u)
    if isinstance(x, list):
        x = np.array(x)
    if isinstance(P, list):
        P = np.array(P)

    # Check inputs type
    if A is not None and not isinstance(A, np.ndarray):
        raise TypeError("A must be a numpy array")
    if Q is not None and not isinstance(Q, np.ndarray):
        raise TypeError("Q must be a numpy array")
    if B is not None and not isinstance(B, np.ndarray):
        raise TypeError("B must be a numpy array")
    if u is not None and not isinstance(u, np.ndarray):
        raise TypeError("u must be a numpy array")
    if not isinstance(x, np.ndarray):
        raise TypeError("x must be a numpy array")
    if not isinstance(P, np.ndarray):
        raise TypeError("P must be a numpy array")

    # Force the state, input and control matrices to be column vectors
    x = x[:, np.newaxis] if x.ndim == 1 else x
    if u is not None:
        u = u[:, np.newaxis] if u.ndim == 1 else u

    # Check that the shape of the matrices is correct
    if A is not None and A.ndim != 2:
        raise ValueError("A must be a 2D matrix")
    if A is not None and x.shape[0] != A.shape[0]:
        raise ValueError("x and A must have the same number of rows")
    if B is not None and B.ndim != 2:
        raise ValueError("B must be a 2D matrix")
    if u is not None and B is not None and u.shape[0] != B.shape[1]:
        raise ValueError(
            "The number of columns in B must be equal to the number of rows in u"
        )
    if B is not None and B.shape[0] != x.shape[0]:
        raise ValueError("B must have the same number of rows as x")
    if P.ndim != 2 or P.shape[0] != P.shape[1]:
        raise ValueError("P must be a square matrix")
    if A is not None and P.shape[0] != A.shape[0]:
        raise ValueError("P must have the same number of rows as A")
    if Q is not None and (Q.ndim != 2 or Q.shape[0] != Q.shape[1]):
        raise ValueError("Q must be a square matrix")
    if Q is not None and A is not None and Q.shape[0] != A.shape[0]:
        raise ValueError("Q must have the same number of rows as A")

    # Check Arguments
    n = A.shape[0] if A is not None else x.shape[0]

    # Default state transition matrix to the identity matrix if not provided
    if A is None:
        A = np.eye(n)

    # Default process noise covariance to zero matrix if not provided
    if Q is None:
        Q = np.zeros((n, n))

    # Default input matrix to the identity matrix if not provided
    if B is None and u is not None:
        B = np.eye(n, u.shape[0])

    # Prediction step
    # State
    if u is None:
        x = A @ x
    else:
        x = A @ x + B @ u

    # Covariance
    P = A @ P @ A.T + Q

    return x.squeeze(), P.squeeze()


def kf_update(
    x: np.ndarray,
    P: np.ndarray,
    y: np.ndarray,
    H: np.ndarray,
    R: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Update step of the Kalman filter.

    Args:
        x (np.ndarray): State mean.
        P (np.ndarray): State covariance.
        y (np.ndarray): Measurement.
        H (np.ndarray): Measurement matrix.
        R (np.ndarray): Measurement noise covariance.

    Returns:
        x (np.ndarray): Updated state mean.
        P (np.ndarray): Updated state covariance.
        K (np.ndarray): Kalman Gain.
        dy (np.ndarray): Measurement residual.
        S (np.ndarray): Covariance residual.

    Raises:
        TypeError: If x, P, y, H or R are not numpy arrays.
        ValueError: If x is not a numpy array, if P is not a numpy array, if y is not a numpy array,
            if H is not a 2D matrix, if R is not a square matrix, if P is not a square matrix,
            if P does not have the same number of rows as x, if H does not have the same number of columns as rows in x,
            if x and y do not have the same number of rows, if R does not have the same number of rows as y.
    """
    # Convert to numpy array
    if isinstance(x, list):
        x = np.array(x)
    if isinstance(P, list):
        P = np.array(P)
    if isinstance(y, list):
        y = np.array(y)
    if isinstance(H, list):
        H = np.array(H)
    if isinstance(R, list):
        R = np.array(R)

    # Check inputs type
    if not isinstance(x, np.ndarray):
        raise TypeError("x must be a numpy array")
    if not isinstance(P, np.ndarray):
        raise TypeError("P must be a numpy array")
    if not isinstance(y, np.ndarray):
        raise TypeError("y must be a numpy array")
    if not isinstance(H, np.ndarray):
        raise TypeError("H must be a numpy array")
    if not isinstance(R, np.ndarray):
        raise TypeError("R must be a numpy array")

    # Force the state and measurements to be column vectors
    x = x[:, np.newaxis] if x.ndim == 1 else x
    y = y[:, np.newaxis] if y.ndim == 1 else y

    # Check dimensions
    if P.ndim != 2 or P.shape[0] != P.shape[1]:
        raise ValueError("P must be a square matrix")
    if P.shape[0] != x.shape[0]:
        raise ValueError("P must have the same number of rows as x")
    if H.ndim != 2:
        raise ValueError("H must be a 2D matrix")
    if x.shape[0] != H.shape[1]:
        raise ValueError("H must have the same number of columns as rows in x")
    if R.ndim != 2 or R.shape[0] != R.shape[1]:
        raise ValueError("R must be a square matrix")
    if R.shape[0] != y.shape[0]:
        raise ValueError("R must have the same number of rows as y")

    # Compute measurement residual
    dy = y - H @ x
    # Compute covariance residual
    S = R + H @ P @ H.T
    # Compute Kalman Gain
    K = P @ H.T @ np.linalg.inv(S)

    # Update state estimate
    x = x + K @ dy
    P = P - K @ H @ P

    return x.squeeze(), P.squeeze(), K.squeeze(), dy.squeeze(), S.squeeze()
