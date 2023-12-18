import os

import numpy as np
from tqdm import tqdm

from src import palette, plot
from src.video import Video


def process_video(video_configs: dict, clusters=3, frequency=10):

    video = Video(**video_configs)

    video.download()

    video.to_frames()

    frames = video.sample(frequency = 15)

    frame_colors = np.array([
        palette.get_frame_color(frame, clusters)
        for frame in tqdm(frames)
    ])


    fig, _ = plot.spectrum(frame_colors)

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

    n_cores = int(args.parallel)
    print (f"Processing {n_cores} videos in parallel")
    if n_cores == 1:
        for video_configs in configs["videos"]:
            process_video(
                video_configs = video_configs,
                clusters = configs["clusters"],
                frequency = configs["frequency"]
            )
    else:
        import multiprocessing
        if n_cores <= 0:
            n_cores = multiprocessing.cpu_count()
        experiments_args = [
            (video_configs, configs["clusters"], configs["frequency"])
            for video_configs in configs["videos"]
        ]
        with multiprocessing.Pool(n_cores) as pool:
            pool.starmap(process_video, (experiments_args))
