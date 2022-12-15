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

# To test the fast C++ loader, you need to connect the dataset to Deep Lake in the UI,
# see https://docs.activeloop.ai/storage-and-credentials/managed-credentials

# benchmark dataset iteration speed
python -m src benchmark_png_dataset <dataset_type>

, where <dataset_type> is one of DEEPLAKE_TF,DEEPLAKE_TF_FAST,DEEPLAKE_TORCH,DEEPLAKE_TORCH_FAST,LOCAL_TF_PIL,LOCAL_TF_IO

# benchmark
python -m src create_large_file --upload true
python -m src benchmark_s3_download
```

# Results dataset

Values represent batches per second, therefore the higher the better.

## Using p3.16xlarge EC2 instance in same region as S3 bucket

```bash
# LOCAL_TF_IO
Average network download speed of 0.005 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 1976.7370838030533,
 'fastest_080%': 953.2584918289123,
 'fastest_090%': 782.3131214157462,
 'fastest_095%': 712.142163356041,
 'fastest_098%': 658.5536492018692,
 'fastest_099%': 643.46317670449,
 'fastest_100%': 560.0356345916175}

# LOCAL TF_PIL
Average network download speed of 0.003 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 15.622719058374555,
 'fastest_080%': 15.416921506191692,
 'fastest_090%': 15.35995150015314,
 'fastest_095%': 15.332037784814702,
 'fastest_098%': 15.312128769852094,
 'fastest_099%': 15.306560207943665,
 'fastest_100%': 15.263525352712174}

# DEEPLAKE_TORCH_FAST WITH 0 WORKERS
Average network download speed of 243.532 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 108.3666643034766,
 'fastest_080%': 56.17683410632269,
 'fastest_090%': 47.459144668815604,
 'fastest_095%': 43.51762138528615,
 'fastest_098%': 40.41428631713758,
 'fastest_099%': 39.30880872266768,
 'fastest_100%': 32.68293856701203}

# DEEPLAKE_TORCH_FAST WITH 4 WORKERS
Average network download speed of 244.798 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 113.99926984873171,
 'fastest_080%': 57.01765189671227,
 'fastest_090%': 47.890749714383965,
 'fastest_095%': 43.75836789329342,
 'fastest_098%': 40.95868249135959,
 'fastest_099%': 40.15088960005184,
 'fastest_100%': 32.89305218906767}
```

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

# LOCAL_TF_PIL (first run only ~10 batches/s, so not sure how conclusive)
Average network download speed of 0.005 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 23.999852051693285,
 'fastest_080%': 23.84242109115737,
 'fastest_090%': 23.20794483674733,
 'fastest_095%': 22.703302013032868,
 'fastest_098%': 22.343847659458458,
 'fastest_099%': 22.23913063824756,
 'fastest_100%': 22.033296632745206}

# DEEPLAKE_TF
Average network download speed of 55.414 MB/s
(32, 256, 256, 3)
<dtype: 'uint8'>
{'fastest_050%': 10.247559576664269,
 'fastest_080%': 9.081544955466738,
 'fastest_090%': 8.886197040858976,
 'fastest_095%': 8.80038530644431,
 'fastest_098%': 8.719707760387276,
 'fastest_099%': 8.680136171801484,
 'fastest_100%': 8.57389746934226}

# DEEPLAKE_TORCH WITH 0 WORKERS
Average network download speed of 44.910 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 10.345577425879336,
 'fastest_080%': 8.012926508038714,
 'fastest_090%': 7.4698842768334055,
 'fastest_095%': 7.215124450493231,
 'fastest_098%': 7.032591512224645,
 'fastest_099%': 6.984303596543268,
 'fastest_100%': 6.897119847849973}

# DEEPLAKE_TORCH WITH 4 WORKERS
Average network download speed of 239.518 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 994.6877940685426,
 'fastest_080%': 30.729583113522963,
 'fastest_090%': 14.80197285104154,
 'fastest_095%': 11.799092462826035,
 'fastest_098%': 10.25614613295722,
 'fastest_099%': 9.904202378238564,
 'fastest_100%': 9.112417292774426}

# DEEPLAKE_TORCH_FAST WITH 0 WORKERS
Average network download speed of 130.012 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 78.61760603835421,
 'fastest_080%': 52.120834278011934,
 'fastest_090%': 30.617122680519167,
 'fastest_095%': 25.007448976680795,
 'fastest_098%': 22.010659401438623,
 'fastest_099%': 21.27509405872195,
 'fastest_100%': 19.6664046795036}

# DEEPLAKE_TORCH_FAST WITH 4 WORKERS
Average network download speed of 149.926 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 75.29613976018715,
 'fastest_080%': 56.64477119142843,
 'fastest_090%': 37.57940919487337,
 'fastest_095%': 29.91967567500537,
 'fastest_098%': 26.14977470092598,
 'fastest_099%': 25.136685594765733,
 'fastest_100%': 23.017890069037033}
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
