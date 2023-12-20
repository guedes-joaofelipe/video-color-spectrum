import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans


class Extraction:
    model = None
    train_set = np.ndarray([])

    def __init__(self) -> None:
        pass

    def fit(self, frame: np.ndarray):
        raise NotImplementedError

    def transform(self, frame: np.ndarray):
        raise NotImplementedError

    def get_predominant_color(self):
        raise NotImplementedError


def get_extraction_model(method: str, params: dict) -> Extraction:
    if method == "KMeans":
        model = ExtractionKMeans(params)
    elif method == "DBSCAN":
        model = ExtractionDBSCAN(params)
    else:
        raise ValueError(
            "Unsupported clustering method. Possible values: KMeans, DBSCAN"
        )

    return model


class ExtractionKMeans(Extraction):
    def __init__(self, params: dict) -> None:
        super().__init__()

        self.model = KMeans(**params)

    def fit(self, frame: np.ndarray):
        self.train_set = frame
        return self.model.fit(frame)

    def transform(self, frame: np.ndarray):
        return self.model.predict(frame)

    def get_centroids(self):
        df = pd.DataFrame(self.train_set)
        df["cluster"] = self.model.labels_
        return df.groupby("cluster").mean()

    def get_predominant_color(self) -> np.ndarray:
        df = pd.DataFrame()
        df["cluster"] = self.model.labels_
        predominant_centroid_index = (
            df["cluster"].value_counts().sort_values(ascending=False).index[0]
        )

        centroids = self.get_centroids()

        return centroids.loc[predominant_centroid_index].values


class ExtractionDBSCAN(Extraction):
    def __init__(self, params: dict) -> None:
        super().__init__()

        self.model = DBSCAN(**params)

    def fit(self, frame: np.ndarray):
        self.train_set = frame
        return self.model.fit(frame)

    def transform(self, frame: np.ndarray):
        return self.model.transform(frame)

    def get_centroids(self):
        df = pd.DataFrame(self.train_set)
        df["cluster"] = self.model.labels_
        return df.groupby("cluster").mean()

    def get_predominant_color(self) -> np.ndarray:
        df = pd.DataFrame()
        df["cluster"] = self.model.labels_
        predominant_centroid_index = (
            df["cluster"].value_counts().sort_values(ascending=False).index[0]
        )

        centroids = self.get_centroids()

        return centroids.loc[predominant_centroid_index].values
