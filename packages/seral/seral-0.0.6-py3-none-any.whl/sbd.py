import numpy as np
from tslearn.metrics import cdist_normalized_cc, y_shifted_sbd_vec

def sbd(X: list[np.ndarray], n_iter: int = 10) -> np.ndarray:
    """ Shape-Based-Distance (SBD) barycenter computation
    
    Implementation inspired by the tslearn library.
    See https://github.com/tslearn-team/tslearn/blob/5568c026db4b4380b99095827e0573a8f55a81f0/tslearn/clustering/kshape.py#L118

    SBD barycenter computation is first described in [1] as part of the k-Shape algorithm.



    [1] J. Paparrizos & L. Gravano. k-Shape: Efficient and Accurate
        Clustering of Time Series. SIGMOD 2015. pp. 1855-1870.

    """
    p = X[0].reshape(-1, 1)
    
    # In [1], the algorithm is used as part of the k-Shape algorithm. There it is
    # executed a number of times, as part of the Refinement step.
    # Here, we run the algorithm a number of times, to enable prototype convergence.
    for i in range(n_iter):

        sz = len(X[0])
        for x in X: assert x.shape[0] == sz
        X = [x.reshape(-1, 1) for x in X]
        X_np = np.array(X)
        assert X_np.shape[0] == len(X)
        assert X_np.shape[1] == sz
        assert X_np.shape[2] == 1
        X = X_np

        norms = np.linalg.norm(X, axis=(1, 2))

        sz = X.shape[1]
        Xp = y_shifted_sbd_vec(p, X,
                                norm_ref=-1,
                                norms_dataset=norms)
        S = np.dot(Xp[:, :, 0].T, Xp[:, :, 0])
        Q = np.eye(sz) - np.ones((sz, sz)) / sz
        M = np.dot(Q.T, np.dot(S, Q))
        _, vec = np.linalg.eigh(M)
        mu_k = vec[:, -1].reshape((sz, 1))

        # The way the optimization problem is (ill-)formulated, both mu_k and
        # -mu_k are candidates for barycenters
        # In the following, we check which one is best candidate
        dist_plus_mu = np.sum(np.linalg.norm(Xp - mu_k, axis=(1, 2)))
        dist_minus_mu = np.sum(np.linalg.norm(Xp + mu_k, axis=(1, 2)))
        if dist_minus_mu < dist_plus_mu:
            mu_k *= -1
        p = mu_k

    return p