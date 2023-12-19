import typing
from typing import Tuple

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle


def spectrum(colors: np.ndarray, figsize: tuple = (50, 40)) -> Tuple[Figure, np.ndarray]:
	""" Plots a rectangular with colors defined in array

	Args:
		colors (np.ndarray): spectrum colors
		figsize (tuple, optional): Defaults to (50, 40).

	Returns:
		Tuple[Figure, np.ndarray]: Output plot and axis from matplotlib
	"""
	fig, ax = plt.subplots(figsize=figsize)

	width, height = figsize
	bar_width = width / colors.shape[0]

	x_start = 0
	for rgb_color in colors:
		hex_color = matplotlib.colors.rgb2hex((*rgb_color/255, 1))
		ax.axvline(x = x_start, ymin = 0, ymax = height, color = hex_color)
		ax.add_patch(Rectangle(
			xy = (x_start, 0),
			width = bar_width,
			height = height,
			fill = True,
			edgecolor = hex_color,
			facecolor = hex_color,
			lw = None
		))
		x_start += bar_width

	ax.set_xticks([]), ax.set_yticks([])
	for spine in ["top", "right", "bottom", "left"]:
		ax.spines[spine].set_visible(False)

	return fig, ax