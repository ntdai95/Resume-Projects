import numpy as np
from scipy.ndimage import convolve


def calculate_metrics(y_true, y_pred, K=10):
    C = np.zeros((K, K))
    for j in range(1, K + 1):
        ind_j = np.where(y_true == j)[0]
        for i in range(1, K + 1):
            ind_pre_i = np.where(y_pred == i)[0]
            C[i-1, j-1] = len(np.intersect1d(ind_j, ind_pre_i))

    accuracy = np.sum(np.diag(C)) / np.sum(C) * 100
    return C, accuracy


def hog20(Im, d, B):
    t = d // 2
    N, M = Im.shape
    hx = np.array([[-1, 0, 1]])
    hy = -hx.T
    grad_xr = convolve(Im.astype(float), hx)
    grad_yu = convolve(Im.astype(float), hy)
    magnit = np.sqrt(grad_xr**2 + grad_yu**2)
    angles = np.arctan2(grad_yu, grad_xr)
    nx1 = np.arange(0, M - d + 1, t)
    ny1 = np.arange(0, N - d + 1, t)
    h = []
    for y in ny1:
        for x in nx1:
            m_block = magnit[y:y+d, x:x+d].flatten()
            a_block = angles[y:y+d, x:x+d].flatten()
            hist, _ = np.histogram(a_block, bins=B, range=(-np.pi, np.pi), weights=m_block)
            h.extend(hist)
            
    return np.array(h).reshape(-1, 1)