import tensorflow as tf

physical_devices = tf.config.list_physical_devices("GPU")
for device in physical_devices:
    tf.config.experimental.set_memory_growth(device, True)


import os
import time
from pathlib import Path
from pprint import pprint

import deeplake
import numpy as np
import tensorflow as tf
import tqdm
from PIL import Image

from src.utils import check_env_vars, measure_network_speed

check_env_vars()
REPO_DIRPATH = Path(__file__).parents[1]
DATA_DIRPATH = REPO_DIRPATH / "data/pngs"
DEEPLAKE_PATH = f"s3://{os.environ['S3_BUCKET_NAME']}/{os.environ['S3_PREFIX']}"


def _create_pngs(
    file_count: int = 10_000,
    image_size: int = 256,
    channel_count: int = 3,
    dtype: str = "uint8",
):
    DATA_DIRPATH.mkdir(exist_ok=True, parents=True)
    for cnt in tqdm.trange(file_count):
        image = np.random.randint(
            low=0,
            high=256,
            size=(image_size, image_size, channel_count),
            dtype=dtype,
        )
        img = Image.fromarray(image)
        img.save(DATA_DIRPATH / f"{cnt:05}.png")


def _upload_dataset():
    ds = deeplake.empty(DEEPLAKE_PATH)
    with ds:
        ds.create_tensor("images", htype="image", sample_compression="png")

    path_list = list(DATA_DIRPATH.glob("*.png"))
    with ds:
        for path in tqdm.tqdm(path_list):
            ds.append({"images": deeplake.read(path)})


def create_png_dataset(upload=True):
    _create_pngs()
    if upload:
        _upload_dataset()


from enum import Enum


class DatasetType(Enum):
    DEEPLAKE = 1
    LOCAL_TF_IO = 2
    LOCAL_PIL = 3


def _get_deeplake_ds() -> tf.data.Dataset:
    deeplake_ds = deeplake.load(DEEPLAKE_PATH)
    return deeplake_ds.tensorflow()


def _get_local_ds(ds_type: DatasetType) -> tf.data.Dataset:
    def _load_image_pil(path: str):
        img = Image.open(path)
        return np.asarray(img)

    def load_image_pil(path: str):
        return tf.numpy_function(_load_image_pil, [path], tf.uint8)

    def load_image_tf(path: str):
        image = tf.io.read_file(path)
        return tf.io.decode_image(image, channels=0)

    load_func = {
        DatasetType.LOCAL_PIL: load_image_pil,
        DatasetType.LOCAL_TF_IO: load_image_tf,
    }[ds_type]

    path_list = [str(p) for p in DATA_DIRPATH.glob("*.png")]
    ds = tf.data.Dataset.from_tensor_slices(path_list)
    return ds.map(load_func)


def benchmark_png_dataset(
    ds_type: DatasetType, batch_size: int = 32, batch_count: int = 250
):
    if ds_type == DatasetType.DEEPLAKE:
        ds = _get_deeplake_ds()
    else:
        ds = _get_local_ds(ds_type)

    if batch_size > 1:
        ds = ds.batch(batch_size, drop_remainder=True)

    durations = []
    with measure_network_speed():
        last_t = time.time()
        for _, elem in tqdm.tqdm(zip(range(batch_count), ds), total=batch_count):
            current_t = time.time()
            durations.append(current_t - last_t)
            last_t = current_t

    try:
        # for deeplake dataset
        tensor = elem["images"]
    except TypeError:
        # for png dataset
        tensor = elem
    assert isinstance(tensor, tf.Tensor)
    print(tensor.shape)
    print(tensor.dtype)

    durations.sort()
    iterations_per_second = {
        f"fastest_{x:03d}%": 1 / np.mean(durations[0 : int(x / 100 * len(durations))])
        for x in [50, 80, 90, 100]
    }
    pprint(iterations_per_second)
