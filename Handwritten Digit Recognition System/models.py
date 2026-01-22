import numpy as np


def f_SRMCC(x, D, muK):
    mu, K = muK[0], int(muK[1])
    N1, P = D.shape
    Xh = np.vstack([D[:N1-1, :], np.ones((1, P))])
    y = D[N1-1, :].astype(int) - 1
    W = x.reshape(N1, K, order='F')
    f = 0
    for p in range(P):
        xp = Xh[:, p]
        scores = xp @ W
        t0 = np.sum(np.exp(scores))
        tp = np.exp(scores[y[p]])
        f += np.log(tp / t0)

    return -f/P + 0.5 * mu * (x.T @ x)


def g_SRMCC(x, D, muK):
    mu, K = muK[0], int(muK[1])
    N1, P = D.shape
    Xh = np.vstack([D[:N1-1, :], np.ones((1, P))])
    y = D[N1-1, :].astype(int) - 1
    W = x.reshape(N1, K, order='F')
    g = np.zeros((N1, K))
    for k in range(K):
        ink = np.where(y == k)[0]
        gk = -np.sum(Xh[:, ink], axis=1) / P
        wk = W[:, k]
        for p in range(P):
            xp = Xh[:, p]
            tp = np.exp(xp @ wk)
            t0 = P * np.sum(np.exp(xp @ W))
            gk += (tp / t0) * xp
        g[:, k] = gk

    return g.flatten(order='F') + mu * x


def f_SVM_MCC(x, D, CK):
    C, K = CK[0], int(CK[1])
    N1, P = D.shape
    Xh = np.vstack([D[:N1-1, :], np.ones((1, P))])
    y = D[N1-1, :].astype(int) - 1
    W = x.reshape(N1, K, order='F')
    W_feat = W[:N1-1, :]
    reg = 0.5 * np.sum(W_feat**2)
    loss = 0
    for p in range(P):
        xp = Xh[:, p]
        scores = W.T @ xp
        sy = scores[y[p]]
        for m in range(K):
            if m != y[p]:
                val = 2 + scores[m] - sy
                if val > 0:
                    loss += val

    return reg + C * loss


def g_SVM_MCC(x, D, CK):
    C, K = CK[0], int(CK[1])
    N1, P = D.shape
    Xh = np.vstack([D[:N1-1, :], np.ones((1, P))])
    y = D[N1-1, :].astype(int) - 1
    W = x.reshape(N1, K, order='F')
    dW = np.zeros((N1, K))
    for p in range(P):
        xp = Xh[:, p]
        scores = W.T @ xp
        sy = scores[y[p]]
        for m in range(K):
            if m != y[p]:
                val = 2 + scores[m] - sy
                if val > 0:
                    dW[:, m] += C * xp
                    dW[:, y[p]] -= C * xp
                    
    dW[:N1-1, :] += W[:N1-1, :]
    return dW.flatten(order='F')