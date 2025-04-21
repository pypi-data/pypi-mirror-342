import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.io import loadmat

DATA_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))

class load:
  @staticmethod
  def mat(name: str, data_path: str = DATA_PATH) -> tuple[np.ndarray, np.ndarray]:
    """Returns `(X, y)`, with `X :: [n, d]`, `y :: [n]`"""
    data = loadmat(os.path.join(data_path, name))
    X = data['X']
    y = data['Y'][:, 0]
    return X, y

  @staticmethod
  def allaml(name: str = 'ALLAML.mat'):
    X_raw, y_raw = load.mat(name)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y

  @staticmethod
  def colon(name: str = 'colon.mat'):
    X_raw, y_raw = load.mat(name)
    X = (X_raw/2) # {-2, 2} -> {-1, 1}
    y = y_raw.clip(0) # {-1, 1} -> {0, 1}
    return X, y

  @staticmethod
  def gli(name: str = 'GLI_85.mat'):
    X_raw, y_raw = load.mat(name)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y

  @staticmethod
  def leukemia(name: str = 'leukemia.mat'):
    X_raw, y_raw = load.mat(name) # X values are {-2, 2}
    X = (X_raw/2) # {-2, 2} -> {-1, 1}
    y = y_raw.clip(0) # {-1, 1} -> {0, 1}
    return X, y

  @staticmethod
  def prostate(name: str = 'Prostate_GE.mat'):
    X_raw, y_raw = load.mat(name)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y

  @staticmethod
  def smk(name: str = 'SMK_CAN_187.mat'):
    X_raw, y_raw = load.mat(name)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y
  
  datasets = {
    'allaml': allaml,
    'colon': colon,
    'gli': gli,
    'leukemia': leukemia,
    'prostate': prostate,
    'smk': smk
  }