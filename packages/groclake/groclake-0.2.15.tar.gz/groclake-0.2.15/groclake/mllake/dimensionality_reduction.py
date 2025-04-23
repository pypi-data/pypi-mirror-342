
from sklearn.decomposition import PCA

class DimensionalityReducer:
    def __init__(self, n_components=2):
        self.model = PCA(n_components=n_components)

    def fit_transform(self, X):
        return self.model.fit_transform(X)
