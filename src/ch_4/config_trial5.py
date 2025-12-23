# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

class ExponentialKernel(Kernel):
    def __init__(self, length_scale=0.0001, length_scale_bounds=(0.0001, 0.01)):
        self.length_scale = length_scale
        self.length_scale_bounds = length_scale_bounds

    @property
    def hyperparameter_length_scale(self):
        return Hyperparameter("length_scale", "numeric", self.length_scale_bounds)

    def __call__(self, X, Y=None, eval_gradient=False):
        X = check_array(X)
        if Y is None:
            Y = X
        dists = np.sqrt(np.sum((X[:, np.newaxis, :] - Y[np.newaxis, :, :]) ** 2, axis=2))
        K = np.exp(-dists / self.length_scale)
        
        if eval_gradient:
            if not self.hyperparameter_length_scale.fixed:
                length_scale_gradient = (dists / (self.length_scale ** 2)) * K
                return K, np.expand_dims(length_scale_gradient, axis=2)
            else:
                return K, np.empty((X.shape[0], X.shape[0], 0))
        return K

    def diag(self, X):
        return np.ones(X.shape[0])

    def is_stationary(self):
        return True
