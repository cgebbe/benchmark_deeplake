import tensorflow as tf

physical_devices = tf.config.list_physical_devices("GPU")
for device in physical_devices:
    tf.config.experimental.set_memory_growth(device, True)

import enum
import os
from pathlib import Path

import deeplake
import numpy as np
import tensorflow as tf
import tqdm
from PIL import Image

from src import utils

utils.check_env_vars()
REPO_DIRPATH = Path(__file__).parents[1]
DATA_DIRPATH = REPO_DIRPATH / "data/pngs"
DEEPLAKE_PATH_S3 = f"s3://{os.environ['S3_BUCKET_NAME']}/{os.environ['S3_PREFIX']}"
DEEPLAKE_PATH_HUB = os.environ["DEEPLAKE_PATH"]
BATCH_SIZE = 32
NUM_WORKER = 0


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
    ds = deeplake.empty(DEEPLAKE_PATH_S3)
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


class DatasetType(enum.Enum):
    DEEPLAKE_TF = enum.auto()
    DEEPLAKE_TF_FAST = enum.auto()
    DEEPLAKE_TORCH = enum.auto()
    DEEPLAKE_TORCH_FAST = enum.auto()
    LOCAL_TF_PIL = enum.auto()
    LOCAL_TF_IO = enum.auto()


def _get_deeplake_ds(ds_type: DatasetType) -> tf.data.Dataset:
    deeplake_ds = deeplake.load(DEEPLAKE_PATH_HUB)
    # deeplake_ds = deeplake.load("hub://activeloop/coco-train")

    if ds_type == DatasetType.DEEPLAKE_TF:
        return deeplake_ds.tensorflow().batch(
            batch_size=BATCH_SIZE, drop_remainder=True
        )
    elif ds_type == DatasetType.DEEPLAKE_TF_FAST:
        return (
            deeplake_ds.dataloader()
            .tensorflow()
            .batch(batch_size=BATCH_SIZE, drop_remainder=True)
        )
    elif ds_type == DatasetType.DEEPLAKE_TORCH:
        return deeplake_ds.pytorch(
            batch_size=BATCH_SIZE,
            num_workers=NUM_WORKER,
            drop_last=True,
            pin_memory=False,
            # decode_method={"images": "pil"},
        )
    elif ds_type == DatasetType.DEEPLAKE_TORCH_FAST:
        return (
            deeplake_ds.dataloader()
            .batch(BATCH_SIZE, drop_last=True)
            .pytorch(tensors=["images"])
        )

    raise ValueError


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
        DatasetType.LOCAL_TF_PIL: load_image_pil,
        DatasetType.LOCAL_TF_IO: load_image_tf,
    }[ds_type]

    path_list = [str(p) for p in DATA_DIRPATH.glob("*.png")]
    ds = tf.data.Dataset.from_tensor_slices(path_list)
    return ds.map(load_func).batch(batch_size=BATCH_SIZE, drop_remainder=True)


def benchmark_png_dataset(ds_type: DatasetType, batch_count: int = 250):
    if ds_type.name.startswith("DEEPLAKE"):
        ds = _get_deeplake_ds(ds_type)
    else:
        ds = _get_local_ds(ds_type)

    watch = utils.StopWatch()
    with utils.measure_network_speed():
        for _, elem in tqdm.tqdm(zip(range(batch_count), ds), total=batch_count):
            watch.stop()

    try:
        # for deeplake dataset
        tensor = elem["images"]
    except TypeError:
        # for PNG dataset
        tensor = elem
    print(tensor.shape)
    print(tensor.dtype)

    watch.evaluate()
