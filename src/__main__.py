from jsonargparse import CLI

from src.png_dataset import benchmark_png_dataset, create_png_dataset

if __name__ == "__main__":
    CLI(
        [
            create_png_dataset,
            benchmark_png_dataset,
        ]
    )
