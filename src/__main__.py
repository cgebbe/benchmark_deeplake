from jsonargparse import CLI

from src.large_file import benchmark_s3_download, create_large_file
from src.png_dataset import benchmark_png_dataset, create_png_dataset

if __name__ == "__main__":
    CLI(
        [
            create_png_dataset,
            benchmark_png_dataset,
            create_large_file,
            benchmark_s3_download,
        ]
    )
