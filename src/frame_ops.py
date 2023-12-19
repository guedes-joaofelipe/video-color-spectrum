import cv2
import numpy as np
from sklearn.cluster import KMeans

RANDOM_STATE = 0

def centroid_histogram(clt):
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	hist = hist.astype("float")
	hist /= hist.sum()

	return hist

def get_color(frame: np.ndarray, n_clusters=10) -> np.ndarray:
	frame = frame.reshape((frame.shape[0] * frame.shape[1], 3))
	clt = KMeans(n_clusters = n_clusters, random_state=RANDOM_STATE)
	clt.fit(frame)
	hist = centroid_histogram(clt)
	predominant_color_index = np.argmax(hist)
	return clt.cluster_centers_[predominant_color_index]

def smooth(frame: np.ndarray, kernel_size: int = 5, method="GaussianBlur") -> np.ndarray:
	kernel = (kernel_size, kernel_size)

	if method == "GaussianBlur":
		if kernel_size % 2 == 0:
			raise ValueError("Kernel size for Gaussian Blur must be odd number.")

		frame = cv2.GaussianBlur(frame, kernel, 0)
	elif method == "Median":
		frame = cv2.medianBlur(frame, kernel_size)
	elif method == "Average":
		frame = cv2.blur(frame, kernel)
	else:
		raise ValueError("Smooth method must be: GaussianBlur, Median or Average")

	return frame