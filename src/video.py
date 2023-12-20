import logging
import os
from datetime import datetime

import cv2
import numpy as np
from pytube import YouTube

from . import default, files


class Video:
    experiments_folder = "./"
    log_filepath = None

    def __init__(self, url: str, output_folder: str, resolution: str = "144p"):
        self.url = url
        self.output_folder = os.path.join(default.DATA_FOLDER, output_folder)
        self.resolution = resolution

        files.create_folder(self.output_folder)
        self.video_filepath = os.path.join(self.output_folder, "video.mp4")
        self.frames_folder = os.path.join(self.output_folder, "frames")
        self.frames = []
        self._set_experiments_folder()
        self._set_logger()

    def _set_logger(self):
        """Sets video logger object"""
        self.logger = logging.getLogger(self.experiments_folder)
        self.logger.setLevel(logging.INFO)

        self.log_filepath = os.path.join(self.experiments_folder, "logger.log")
        handler = logging.FileHandler(self.log_filepath, mode="w")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _set_experiments_folder(self):
        self.experiments_folder = os.path.join(
            self.output_folder,
            "experiments",
            datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
        )
        files.create_folder(self.experiments_folder)

    def download(self, force=False) -> str:
        """Downloads video from youtube URL"""

        if not force and files.exists(self.video_filepath):
            self.logger.info(
                f"Video file already exists in path `{self.video_filepath}` (force is {force})"
            )
        else:
            yt = YouTube(self.url)
            streams = yt.streams.filter(file_extension="mp4", res=self.resolution)
            if len(streams) > 0:
                filepath = streams[0].download(self.output_folder)
                filepath = files.rename(filepath, "video.mp4")
            else:
                raise ValueError(
                    f"Video with MP4 extension and {self.resolution} resolution not found"
                )
            self.logger.info(f"Video downloaded to `{self.video_filepath}`")
        return self.video_filepath

    def to_frames(self) -> int:
        """Transforms video into frames and saves them into frames/ folder"""
        files.create_folder(self.frames_folder)

        video = cv2.VideoCapture(self.video_filepath)
        success, image = video.read()

        self.frames = []
        while success:
            output_filepath = os.path.join(
                self.frames_folder, f"frame_{len(self.frames)}.jpg"
            )
            if not cv2.imwrite(output_filepath, image):
                self.logger.warn(f"Failed writing frame {len(self.frames)}")
            self.frames.append(output_filepath)
            success, image = video.read()

        self.logger.info(
            f"{len(self.frames)} frames downloaded to `{self.frames_folder}`"
        )
        return self.frames

    def __getitem__(self, index):
        filepath = self.frames[index]
        return self.load_frame_from_file(filepath)

    def sample(self, frequency: int = 30) -> np.ndarray:
        """Samples 1 in every {frequency} frames"""
        return np.array(
            [self.__getitem__(i) for i in range(len(self.frames)) if i % frequency == 0]
        )

    def load_frame_from_file(self, filepath: str) -> np.ndarray:
        """Loads single frame from filepath"""
        image = cv2.imread(filepath)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
