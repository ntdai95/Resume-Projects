import numpy as np
import scipy.io as sio
import time
from sklearn.decomposition import PCA
from models import f_SRMCC, g_SRMCC, f_SVM_MCC, g_SVM_MCC
from optimizers import run_bfgs
from utils import calculate_metrics, hog20


# --- LOAD DATA ---
X1600 = sio.loadmat('data/X1600.mat')['X1600']
Te28 = sio.loadmat('data/Te28.mat')['Te28']
Lte28 = sio.loadmat('data/Lte28.mat')['Lte28'].flatten()
ytr = np.repeat(np.arange(1, 11), 1600)
ytest = Lte28 + 1
K = 10

# --- CASE 1: SOFTMAX (RAW) ---
print("\n--- CASE 1: SOFTMAX RAW ---")
tic = time.time()
Dtr = np.vstack([X1600, ytr])
Ws1 = run_bfgs(Dtr, f_SRMCC, g_SRMCC, [0.1, K], 50)
Dtest1 = np.vstack([Te28, np.ones((1, 10000))])
y_pred1 = np.argmax(Dtest1.T @ Ws1, axis=1) + 1
C1, acc1 = calculate_metrics(ytest, y_pred1)
print(f"Accuracy: {acc1:.2f}%, Time: {time.time()-tic:.0f}s")

# --- CASE 2: SOFTMAX + HOG ---
print("\n--- CASE 2: SOFTMAX HOG ---")
tic = time.time()
Htr = np.hstack([hog20(X1600[:, i].reshape(28,28, order='F'), 7, 9) for i in range(16000)])
Hte = np.hstack([hog20(Te28[:, i].reshape(28,28, order='F'), 7, 9) for i in range(10000)])
Dhtr = np.vstack([Htr, ytr])
Ws2 = run_bfgs(Dhtr, f_SRMCC, g_SRMCC, [0.1, K], 50)
Dhtest = np.vstack([Hte, np.ones((1, 10000))])
y_pred2 = np.argmax(Dhtest.T @ Ws2, axis=1) + 1
C2, acc2 = calculate_metrics(ytest, y_pred2)
print(f"Accuracy: {acc2:.2f}%, Time: {time.time()-tic:.0f}s")

# --- CASE 3: SVM (C=0.1) ---
print("\n--- CASE 3: SVM RAW (C=0.1) ---")
tic = time.time()
Ws3 = run_bfgs(Dtr, f_SVM_MCC, g_SVM_MCC, [0.1, K], 50)
y_pred3 = np.argmax(Dtest1.T @ Ws3, axis=1) + 1
C3, acc3 = calculate_metrics(ytest, y_pred3)
print(f"Accuracy: {acc3:.2f}%, Time: {time.time()-tic:.0f}s")

# --- CASE 4: SVM + PCA (r=50) ---
print("\n--- CASE 4: SVM PCA (r=50, C=0.1) ---")
tic = time.time()
pca = PCA(n_components=50)
Xtr_pca = pca.fit_transform(X1600.T).T
Xte_pca = pca.transform(Te28.T).T
Dptr = np.vstack([Xtr_pca, ytr])
Ws4 = run_bfgs(Dptr, f_SVM_MCC, g_SVM_MCC, [0.1, K], 50)
Dptest = np.vstack([Xte_pca, np.ones((1, 10000))])
y_pred4 = np.argmax(Dptest.T @ Ws4, axis=1) + 1
C4, acc4 = calculate_metrics(ytest, y_pred4)
print(f"Accuracy: {acc4:.2f}%, Time: {time.time()-tic:.0f}s")