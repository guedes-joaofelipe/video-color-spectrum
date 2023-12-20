import os

import mlflow
import numpy as np
from tqdm import tqdm

from src import default, frame_ops, plot
from src.video import Video


def process_video(
    video_configs: dict,
    color_extraction: dict = default.COLOR_EXTRACTION,
    frequency: int = default.FREQUENCY,
    smooth: dict = default.SMOOTH,
    figsize: tuple = default.FIGSIZE,
    tracking_uri: str = default.TRACKING_URI,
):
    mlflow.set_tracking_uri(tracking_uri)
    experiment = mlflow.set_experiment(video_configs["output_folder"])

    with mlflow.start_run(experiment_id=experiment.experiment_id, nested=True):
        configs = {
            "video_configs": video_configs,
            "color_extraction": color_extraction,
            "frequency": frequency,
            "smooth": smooth,
        }
        for key, value in configs.items():
            mlflow.log_param(key, value)

        video = Video(**video_configs)

        video.download(force=False)

        video.to_frames()

        frames = video.sample(frequency)

        if smooth:
            frames = np.array([frame_ops.smooth(frame, **smooth) for frame in frames])

        frame_colors = np.array(
            [frame_ops.get_color(frame, color_extraction) for frame in tqdm(frames)]
        )

        fig, _ = plot.spectrum(frame_colors, figsize=figsize)
        mlflow.log_figure(fig, "spectrum.jpg")
        mlflow.log_artifact(video.log_filepath)


if __name__ == "__main__":
    import argparse

    import yaml

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--configs", default="configs.yaml", help="Path to configs yaml"
    )
    parser.add_argument(
        "-p",
        "--parallel",
        default=3,
        help="Defines the number of parallel videos to be processed",
    )

    args = parser.parse_args()

    with open(args.configs, "r") as file:
        configs = yaml.safe_load(file)

    video_configs = configs.pop("videos")
    n_cores = min(len(video_configs), int(args.parallel))
    print(f"Processing {n_cores} videos in parallel")

    experiments_args = [
        (
            video_config,
            configs["color_extraction"],
            configs["frequency"],
            configs["smooth"],
            configs["figsize"],
            configs["tracking_uri"],
        )
        for video_config in video_configs
    ]

    if n_cores == 1:
        for args in experiments_args:
            process_video(*args)
    else:
        import multiprocessing

        if n_cores <= 0:
            n_cores = multiprocessing.cpu_count()

        with multiprocessing.Pool(n_cores) as pool:
            pool.starmap(process_video, (experiments_args))
