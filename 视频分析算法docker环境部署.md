## jetson orin nano基于yolov8模型docker部署

### 1.安装nvidia-docker2

```

```

### 2.拉取镜像

```
1.拉取支持cuda的镜像环境
docker pull nvidia/cuda:11.4.3-devel-ubuntu20.04
2.生成容器
docker run -it --gpus all --name yolov8_container nvidia/cuda:11.4.3-devel-ubuntu20.04 /bin/bash
3.进入容器，再安装python和pip
apt-get update
apt-get update && apt-get install -y python3 python3-pip
```

### 3.安装cudnn

#### 3.1安装过程

3.1.1 官网：https://developer.nvidia.com/rdp/cudnn-archive

3.1.2 下载cuda对应版本的cudnn

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250213102431438.png" alt="image-20250213102431438" style="zoom: 50%;" />

3.1.3 安装

```
下载：cudnn-local-repo-ubuntu2004-8.6.0.163_1.0-1_arm64.deb
安装：dpkg -i cudnn-local-repo-ubuntu2004-8.6.0.163_1.0-1_arm64.deb
依赖：apt-get install libcudnn8 libcudnn8-dev
```

#### 3.2问题

问题1：ImportError: libnuma.so.1: cannot open shared object file: No such file or directory

```
解决办法：
    apt update
    apt install libnuma1
```

问题2：ImportError: libopenblas.so.0: cannot open shared object file: No such file or directory

```
解决办法：
    apt update
    apt install libopenblas-dev
```

### 4.安装torch和torchvision

```
torch:
	网址：https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
    下载：torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
    安装：pip install torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
    查看：
    	import torch
        print(torch.__version__)
        print(torch.cuda.is_available())
torchvision:
	网址：https://github.com/pytorch/vision/tree/release/0.16
    下载：vision-release-0.16.zip
    安装：
        apt install libopenblas-base libopenmpi-dev libomp-dev 
        apt install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev 
    	unzip vision-release-0.16.zip
        cd vision-release-0.16
        python3 setup.py install --user   # 10min的运行时间
    查看：
    	import torchvision
    	print(torchvision.__version__)
```















