import numpy as np


def bt_lsearch(x, d, fname, gname, D, params):
    rho, gma, a = 0.1, 0.5, 1.0
    f0 = fname(x, D, params)
    g0 = gname(x, D, params)
    while fname(x + a * d, D, params) > f0 + rho * a * (g0.T @ d):
        a *= gma
        if a < 1e-10: break

    return a


def run_bfgs(Dtr, fname, gname, params, iter_count):
    N1, K = Dtr.shape[0], int(params[1])
    xk = np.zeros(N1 * K)
    fk = fname(xk, Dtr, params)
    gk = gname(xk, Dtr, params)
    dk = -gk
    ak = bt_lsearch(xk, dk, fname, gname, Dtr, params)
    dtk = ak * dk
    xk_new = xk + dtk
    for k in range(1, iter_count + 1):
        gk_new = gname(xk_new, Dtr, params)
        gmk = gk_new - gk
        gk = gk_new
        rk = 1.0 / (dtk.T @ gmk)
        if rk <= 0:
            dk = -gk
        else:
            tk = dtk.T @ gk
            qk = gk - (rk * tk) * gmk
            bk = rk * (gmk.T @ qk - tk)
            dk = bk * dtk - qk

        xk = xk_new
        ak = bt_lsearch(xk, dk, fname, gname, Dtr, params)
        dtk = ak * dk
        xk_new = xk + dtk
        print(f"  Iter {k}: Loss {fname(xk_new, Dtr, params):.4e}")
        
    return xk_new.reshape(N1, K, order='F')