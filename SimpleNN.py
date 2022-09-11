import numpy as np


class SimpleNN:
    def __init__(self, input_dim: int):
        self._list = [(input_dim, None, None, None)]

    def add(self, units: int, activation="relu", use_bias: bool = False):
        dim_prev = self._list[-1][0]
        if use_bias:
            bias = np.random.random((1, units)) - 0.5
        else:
            bias = None

        weights = np.random.random((units,dim_prev)) - 0.5
        self._list.append((units, activation, bias, weights))

    def predict(self, input_vector: np.ndarray, verbose: bool = 0):
        z = input_vector
        for i, item in enumerate(self._list[1:]):
            z = np.dot(item[3], z.T).T
            if item[2] is not None:
                z += item[2]
            if item[1] == "relu":
                z = np.where(z > 0, z, 0)
            elif item[1] == "softmax":
                ex = np.exp(z)
                z = ex / ex.sum()
        return z
