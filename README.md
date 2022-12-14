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

# DEEPLAKE_TORCH WITH 2 WORKERS
Average network download speed of 105.221 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 71.03030989460096,
 'fastest_080%': 13.434375749102742,
 'fastest_090%': 10.428007032120984,
 'fastest_100%': 8.136889988358998}

# DEEPLAKE_TORCH WITH 8 WORKERS
Average network download speed of 574.021 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 1425.8308925312817,
 'fastest_080%': 59.240661515145945,
 'fastest_090%': 24.860454092616912,
 'fastest_100%': 10.786872859144813}


# DEEPLAKE_TORCH_FAST WITH 2 WORKERS
Average network download speed of 132.805 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 52.879918585452494,
 'fastest_080%': 15.823851421710934,
 'fastest_090%': 12.558904732617254,
 'fastest_100%': 10.189517706242173}

# DEEPLAKE_TORCH_FAST WITH 4 WORKERS (recommended by deeplake lib)
Average network download speed of 294.941 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 2780.2772386437155,
 'fastest_080%': 45.71588514046043,
 'fastest_090%': 18.538429777091956,
 'fastest_095%': 14.711939092086698,
 'fastest_098%': 12.724920817866078,
 'fastest_099%': 12.251549112879632,
 'fastest_100%': 11.176130240816159}


# DEEPLAKE_TORCH_FAST WITH 8 WORKERS
Average network download speed of 572.419 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 2297.58404143897,
 'fastest_080%': 918.5837665117919,
 'fastest_090%': 50.19128639455475,
 'fastest_095%': 19.681063008997892,
 'fastest_098%': 13.894113122655455,
 'fastest_099%': 12.896967839142068,
 'fastest_100%': 10.664840590445777}


# DEEPLAKE_TORCH_FAST WITH 16 WORKERS
Average network download speed of 767.680 MB/s
torch.Size([32, 256, 256, 3])
torch.uint8
{'fastest_050%': 1039.6186457482333,
 'fastest_080%': 325.205012012097,
 'fastest_090%': 155.04550152553452,
 'fastest_095%': 26.40634880796745,
 'fastest_098%': 11.20506356752272,
 'fastest_099%': 9.774871581296054,
 'fastest_100%': 7.122003009553231}
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
