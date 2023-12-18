# Video Color Spectrum

This repository contains the script to extract the color spectrum of a YouTube video.

## Example

By applying the pipeline for [this video](https://www.youtube.com/watch?v=eAS0XDyI_M8), we get the following color spectrum:

![](./docs/youtube-print.png)

![Color Spectrum](./docs/spectrum-example.jpg)


# Running the pipeline

## Define configs

You can extract the color spectrum for multiple videos by adding their configs as an item in the `configs.yaml` file. To do so, define it with the following structure:

```yaml
-
    output_folder: {extration output folder}
    url: {YouTube URL video}
    resolution: {video resolution (defaults to 144p)}
```


## Execute pipeline

Once configs are define, execute the following command:

```bash
make run
```

or, to use other parameters:

```bash
python main.py --parallel=1 --configs=configs.yaml 
```

- `parallel`: defines how many videos will be processed in parallel using the `multiprocessing` library
- `configs`: defines the path to the configs yaml file