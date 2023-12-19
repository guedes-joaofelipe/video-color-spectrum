import os

import numpy as np
from tqdm import tqdm

from src import frame_ops, plot
from src.video import Video


def process_video(
        video_configs: dict,
        clusters: int = 3,
        frequency: int = 10,
        kernel_size: int = 5,
        smooth: str = "GaussianBlur",
        figsize: tuple = (16,5)
    ):

    video = Video(**video_configs)

    video.download()

    video.to_frames()

    frames = video.sample(frequency)

    if smooth:
        frames = np.array([
            frame_ops.smooth(frame, kernel_size, method=smooth)
            for frame in frames
        ])

    frame_colors = np.array([
        frame_ops.get_color(frame, clusters)
        for frame in tqdm(frames)
    ])

    fig, _ = plot.spectrum(frame_colors, figsize=figsize)

    fig.savefig(os.path.join(video.output_folder, "spectrum.jpg"), bbox_inches="tight")


if __name__ == "__main__":
    import argparse

    import yaml

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configs", default="configs.yaml", help = "Path to configs yaml")
    parser.add_argument("-p", "--parallel", default=3, help = "Defines the number of parallel videos to be processed")

    args = parser.parse_args()

    with open(args.configs, "r") as file:
        configs = yaml.safe_load(file)

    video_configs = configs.pop("videos")
    n_cores = min(len(video_configs), int(args.parallel))
    print (f"Processing {n_cores} videos in parallel")

    experiments_args = [
        (
            video_config,
            configs["clusters"],
            configs["frequency"],
            configs["kernel_size"],
            configs["smooth"],
            configs["figsize"]
        )
        for video_config in video_configs
    ]

    if n_cores == 1:
        for video_config in video_configs:
            process_video(*experiments_args)
    else:
        import multiprocessing
        if n_cores <= 0:
            n_cores = multiprocessing.cpu_count()

        with multiprocessing.Pool(n_cores) as pool:
            pool.starmap(process_video, (experiments_args))
