# How to install

```bash
pip install -r reqs.txt
```

# How to use

First export the required environment variables for your S3 bucket:

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=...
export S3_BUCKET_NAME=...
export S3_PREFIX=...
```

Then, run

```bash
# benchmark dataset iteration speed
python -m src create_png_dataset --upload true
python -m src benchmark_png_dataset LOCAL_TF_IO
python -m src benchmark_png_dataset LOCAL_PIL
python -m src benchmark_png_dataset DEEPLAKE

# benchmark
python -m src create_large_file --upload true
python -m src benchmark_s3_download
```

# Results dataset

Values represent iterations per second, therefore the higher the better.

## Using r6i.xlarge EC2 instance in same region as S3 bucket

```bash
# LOCAL_TF_IO
Average network download speed of 0.003 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 71.21712347142183,
 'fastest_080%': 70.74242709053051,
 'fastest_090%': 70.57504339528964,
 'fastest_100%': 69.58290708458598}

# LOCAL_PIL
Average network download speed of 0.006 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 24.147134812168485,
 'fastest_080%': 24.046353009103555,
 'fastest_090%': 24.009098296450688,
 'fastest_100%': 23.86269610170065}

# DEEPLAKE
Average network download speed of 32.796 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 7.739933121490811,
 'fastest_080%': 5.86794075040542,
 'fastest_090%': 5.473526373542395,
 'fastest_100%': 5.036806951371547}
```

## Using our local NVIDIA DGX A100

```bash
# LOCAL_TF_IO
Average network download speed of 0.021 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 3082.7233011706735,
 'fastest_080%': 1430.1144451888867,
 'fastest_090%': 1155.1331859609438,
 'fastest_100%': 635.229189952172}

 # LOCAL_PIL
Average network download speed of 0.014 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 24.95310773963837,
 'fastest_080%': 24.38098781184287,
 'fastest_090%': 24.079841144019444,
 'fastest_100%': 23.523043868093495}

# DEEPLAKE
Average network download speed of 49.869 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 5.319442793318664,
 'fastest_080%': 4.268199899730012,
 'fastest_090%': 4.058714611178034,
 'fastest_100%': 3.7857384725578402}
```

## s3 download speed

```
Average network download speed of 278.114 MB/s
```
