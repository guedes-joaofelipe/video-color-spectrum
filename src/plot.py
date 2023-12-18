import typing
from typing import Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def get_color_bars(colors: np.ndarray, height: int = 1) -> np.ndarray:
	""" Creates arrays of colors to be plotted as bars

	Args:
		colors (np.ndarray): bar colors
		height (int, optional): bar height. Defaults to 1.

	Returns:
		np.ndarray: color bars to be plotted
	"""
	n_bars = colors.shape[0]
	width = n_bars
	bar_width = 1 / n_bars
	bar = np.zeros((height, width, 3), dtype = "uint8")

	startX = 0
	for color in colors:
		endX = startX + (width * bar_width)
		cv2.rectangle(
			bar,
			pt1=(int(startX), 0),
			pt2=(int(endX), height),
			color=color.astype("uint8").tolist(),
			thickness=0
		)
		startX = endX

	return bar


def spectrum(colors: np.ndarray, figsize: tuple = (50, 40)) -> Tuple[Figure, np.ndarray]:
	""" Plots a rectangular with colors defined in array

	Args:
		colors (np.ndarray): spectrum colors
		figsize (tuple, optional): Defaults to (50, 40).

	Returns:
		Tuple[Figure, np.ndarray]: Output plot and axis from matplotlib
	"""
	bars = get_color_bars(colors, height=figsize[1])

	fig, ax = plt.subplots(figsize=figsize)
	ax.set_xticks([]), ax.set_yticks([])
	for spine in ["top", "right", "bottom", "left"]:
		ax.spines[spine].set_visible(False)

	ax.imshow(bars)
	return fig, ax