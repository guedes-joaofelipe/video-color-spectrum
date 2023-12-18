import cv2
import numpy as np
from sklearn.cluster import KMeans

def centroid_histogram(clt):
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	hist = hist.astype("float")
	hist /= hist.sum()

	return hist

def get_frame_color(frame: np.ndarray, n_clusters=10) -> np.ndarray:
	frame = frame.reshape((frame.shape[0] * frame.shape[1], 3))
	clt = KMeans(n_clusters = n_clusters)
	clt.fit(frame)
	hist = centroid_histogram(clt)
	predominant_color_index = np.argmax(hist)
	return clt.cluster_centers_[predominant_color_index]
