import os
import numpy as np

DATA_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, os.pardir, 'data'))

def StandardScaler():
  from sklearn.preprocessing import StandardScaler
  return StandardScaler()

class load:
  @staticmethod
  def mat(name: str, data_path: str = DATA_PATH) -> tuple[np.ndarray, np.ndarray]:
    """Returns `(X, y)`, with `X :: [n, d]`, `y :: [n]`"""
    from scipy.io import loadmat
    data = loadmat(os.path.join(data_path, name))
    X = data['X']
    y = data['Y'][:, 0]
    return X, y

  @staticmethod
  def allaml(name: str = 'ALLAML.mat', data_path: str = DATA_PATH):
    X_raw, y_raw = load.mat(name, data_path)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y

  @staticmethod
  def colon(name: str = 'colon.mat', data_path: str = DATA_PATH):
    X_raw, y_raw = load.mat(name, data_path)
    X = (X_raw/2) # {-2, 2} -> {-1, 1}
    y = y_raw.clip(0) # {-1, 1} -> {0, 1}
    return X, y

  @staticmethod
  def gli(name: str = 'GLI_85.mat', data_path: str = DATA_PATH):
    X_raw, y_raw = load.mat(name, data_path)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y

  @staticmethod
  def leukemia(name: str = 'leukemia.mat', data_path: str = DATA_PATH):
    X_raw, y_raw = load.mat(name, data_path) # X values are {-2, 2}
    X = (X_raw/2) # {-2, 2} -> {-1, 1}
    y = y_raw.clip(0) # {-1, 1} -> {0, 1}
    return X, y

  @staticmethod
  def prostate(name: str = 'Prostate_GE.mat', data_path: str = DATA_PATH):
    X_raw, y_raw = load.mat(name, data_path)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y

  @staticmethod
  def smk(name: str = 'SMK_CAN_187.mat', data_path: str = DATA_PATH):
    X_raw, y_raw = load.mat(name, data_path)
    X = StandardScaler().fit_transform(X_raw)
    y = y_raw-1 # {1, 2} -> {0, 1}
    return X, y
  
  @staticmethod
  def datasets(data_path: str = DATA_PATH):
    """Returns a dictionary of datasets"""
    return {
      'allaml': lambda: load.allaml(data_path=data_path),
      'colon': lambda: load.colon(data_path=data_path),
      'gli': lambda: load.gli(data_path=data_path),
      'leukemia': lambda: load.leukemia(data_path=data_path),
      'prostate': lambda: load.prostate(data_path=data_path),
      'smk': lambda: load.smk(data_path=data_path),
    }