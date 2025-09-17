## jetson orin nano基于yolov8模型docker部署-------视频分析模型

### 1.安装**`nvidia-container-toolkit`**

```
第一步：
    docker安装:
        sudo apt-get install -y docker.io
        sudo systemctl start docker
        sudo systemctl enable docker
        docker --version
        sudo vim /etc/docker/daemon.json
    docker compose安装:
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        docker-compose --version
第二步：
	curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add - distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
    sudo apt-get update
第三步：修改（宿主机）文件“sudo vim /etc/apt/sources.list.d/nvidia-container-runtime.list”，将版本“18.04”改成“20.04”；
 	deb https://nvidia.github.io/libnvidia-container/stable/ubuntu20.04/$(ARCH) /
    #deb https://nvidia.github.io/libnvidia-container/experimental/ubuntu20.04/$(ARCH) /
    deb https://nvidia.github.io/nvidia-container-runtime/stable/ubuntu20.04/$(ARCH) /
    #deb https://nvidia.github.io/nvidia-container-runtime/experimental/ubuntu20.04/$(ARCH) /
第四步：
	sudo apt-get update
	sudo apt-get install -y nvidia-container-toolkit
	sudo nvidia-ctk runtime configure --runtime=docker
	sudo systemctl restart docker
	docker info | grep -i runtime
注意：
	nvidia-container-toolkit：是为多种架构（包括 ARM64）设计的通用解决方案，专门针对 Jetson 系列设备（基于 ARM 架构）进行了优化，能够更好地适配 Jetson Orin Nano 的 ARM64 架构，确保在该架构上稳定运行并充分发挥 NVIDIA GPU 的性能；
	nvidia-docker2：最初主要是为 x86_64 架构设计的，虽然也在一定程度上支持其他架构，但对于 ARM64 架构的支持可能不够完善，在 Jetson Orin Nano 这类 ARM64 设备上使用可能会出现兼容性问题，导致安装失败或无法正常使用 GPU 资源。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250219104346666.png" alt="image-20250219104346666" style="zoom: 80%;" />

### 2.拉取镜像

```
1.拉取支持cuda的镜像环境
	docker pull nvcr.io/nvidia/l4t-base:35.4.1
2.生成容器
    docker run -it --runtime=nvidia --name=video_arm64 nvcr.io/nvidia/l4t-base:35.4.1 bash
    docker run -it --runtime=nvidia --name=people_count -v /home/orin/project/icms/docker_config:/icms/docker_config nvcr.io/nvidia/l4t-base:35.4.1 bash
3.进入容器，再安装python和pip(如果镜像中自带python和pip，可选)
    apt-get update && apt-get install -y python3-pip
注意：
	使用 --runtime=nvidia 参数指定 NVIDIA 运行时后，容器可以访问宿主机的 NVIDIA GPU。这样，在容器内就可以运行需要 GPU 加速的应用程序，例如深度学习训练、图形渲染等。
```

**注意！注意！注意！：**

```
# 后续操作都是在容器中进行的操作；
docker exec -it video_arm64 bash   # 进入容器
```

### 3.安装cuda，cudnn和tensorrt

```
cuda安装：
	apt install cuda
检查：
	nvcc -V
配置路径：
	export PATH=/usr/local/cuda/bin:$PATH
```

```
cudnn安装：
	apt install libcudnn8-dev
检查：
		dpkg -l libcudnn8
```

```
tensorrt安装：
	apt install tensorrt
检查：
	dpkg -l tensorrt
绑定python与tensorrt：
	dpkg -i python3-libnvinfer_8.5.2-1+cuda11.4_arm64.deb 
	dpkg -i python3-libnvinfer-dev_8.5.2-1+cuda11.4_arm64.deb 
```

### 4.安装torch和torchvision

```
torch:
	网址：https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
    下载：torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
    安装：
    	apt-get update
		apt-get install -y libopenblas-base libopenblas-dev
    	pip install torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
    查看：
    	python3 -c "import torch ; print(torch.__version__);print(torch.cuda.is_available())"
        import torch
        print(torch.__version__)
        print(torch.cuda.is_available())
torchvision:
	网址：https://github.com/pytorch/vision/tree/release/0.16
    下载：vision-release-0.16.zip
    安装：
        apt-get install libopenblas-base libopenmpi-dev libomp-dev 
        apt-get install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev 
    	unzip vision-release-0.16.zip && cd vision-release-0.16
        python3 setup.py install --user   # 15min的运行时间
    查看：
    	python3 -c "import torchvision ; print(torchvision.__version__)"
    	import torchvision               # 不要在安装目录下执行，不然会告警
    	print(torchvision.__version__)   
```

### 5.安装 Yolov8

```
# ultralytics包含yolov8训练和预测所需的库
pip install ultralytics==8.3.59 -i https://mirrors.aliyun.com/pypi/simple/
pip uninstall opencv-python           # 卸载，opencv无法利用GPU直接加速,需要下载opencv源码进行编译
```

### 6.重新安装OpenCV

```
1.卸载：
	sudo apt purge libopencv*
    sudo apt autoremove
    sudo apt update
2.安装依赖：
	sudo apt install -y build-essential checkinstall cmake pkg-config yasm git gfortran
    sudo apt update
    sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
    sudo apt install -y software-properties-common
    sudo apt update
    sudo add-apt-repository "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ xenial main multiverse restricted universe"
    sudo apt update
    sudo apt install -y libjasper1 libjasper-dev
    sudo apt install -y libjpeg8-dev libpng-dev libtiff5-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine2-dev libv4l-dev
    sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev libtbb-dev libatlas-base-dev libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev libxvidcore-dev libopencore-amrnb-dev libopencore-amrwb-dev x264 v4l-utils
    sudo apt install -y python3-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
```

```
3.下载：
	opencv-4.6.0.zip和opencv_contrib-4.6.0.zip：
	官网：
        https://github.com/opencv/opencv/tree/4.6.0
        https://github.com/opencv/opencv_contrib/tree/4.6.0
4.解压：
	unzip opencv-4.6.0.zip
    unzip opencv_contrib-4.6.0.zip
    mv opencv_contrib-4.6.0 ./opencv-4.6.0
    cd opencv-4.6.0 && mkdir build && cd build
5.编译：
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.6.0/modules \
      -D CUDA_ARCH_BIN='8.7' \
      -D CUDA_ARCH_PTX='8.7' \
      -D WITH_CUDA=1 \
      -D BUILD_opencv_python3=1 \
      -D BUILD_opencv_python2=1 \
      -D WITH_FFMPEG=1 \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D ENABLE_FAST_MATH=1 \
      -D CUDA_FAST_MATH=1 \
      -D WITH_CUBLAS=1 \
      -D OPENCV_GENERATE_PKGCONFIG=1 \
      -D WITH_GTK=ON \
      -D WITH_GTK_2_X=OFF \
      -D WITH_GSTREAMER=ON \
      -D BUILD_TESTS=OFF \
      -D BUILD_PERF_TESTS=OFF \
      -D BUILD_EXAMPLES=OFF \
      ..
	运行时间：5min
6.安装：
	运行时间：50min
	sudo make -j$(nproc) && sudo make install 
7.验证：
	import cv2
	print(cv2.__version__)
注意：
	# opencv编译完成后无法直接调用cv2库，需要将编译后的文件移动到python环境中
	cp /docker_config/opencv-4.6.0/build/lib/python3/cv2.cpython-38-aarch64-linux-gnu.so /usr/lib/python3.8/dist-packages/
```

### 7.**安装 **DeepStream

```
安装依赖：
    sudo apt install -y libssl-dev libgstreamer1.0-0 gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav libgstrtspserver-1.0-0 libjansson-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstrtspserver-1.0-dev libx11-dev libyaml-cpp-dev
    sudo apt install --reinstall -y nvidia-l4t-gstreamer nvidia-l4t-multimedia nvidia-l4t-core
下载：
	deepstream_sdk_v6.2.0_jetson.tbz2 
官网：
	https://catalog.ngc.nvidia.com/orgs/nvidia/resources/deepstream/files?version=6.3
安装：
    sudo tar -xvf deepstream_sdk_v6.2.0_jetson.tbz2 -C /
    cd /opt/nvidia/deepstream/deepstream-6.2
    sudo ./install.sh
    sudo ldconfig
查看：
	输入命令：
		deepstream-app  --version-all     # 第一次执行会出现一些警告（warning）信息，再执行一次就会正常出现
    输出信息：
        deepstream-app version 6.2.0
        DeepStreamSDK 6.2.0
        CUDA Driver Version: 11.4
        CUDA Runtime Version: 11.4
        TensorRT Version: 8.5
        cuDNN Version: 8.6
        libNVWarp360 Version: 2.0.1d3
```

### 8.ffmpeg源码编译

```
1.网址：https://github.com/FFmpeg/FFmpeg/tree/release/5.1
下载：FFmpeg-release-5.1.zip
```

```
运行配置文件：
	./configure \
      --enable-nonfree \
      --enable-cuda-nvcc \
      --enable-libnpp \
      --extra-cflags=-I/usr/local/cuda-11.4/include \
      --extra-ldflags=-L/usr/local/cuda-11.4/lib64 \
      --enable-gpl \
      --enable-libx264 \
      --enable-libx265 \
      --nvcc=/usr/local/cuda-11.4/bin/nvcc
```

```
编译：
	make -j$(nproc)
	sudo make install
查看：
	ffmpeg -version
```

### 9.问题

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

问题3：E: Unable to locate package nvidia-jetpack

```
下载 NVIDIA 的公钥文件：
	wget https://repo.download.nvidia.com/jetson/jetson-ota-public.asc
将公钥添加到 APT 的密钥环中：
	sudo apt-key add jetson-ota-public.asc
更新软件包列表：
	sudo apt-get update
```

### 10.conda环境搭建

```
1.下载：Miniconda3-py39_25.1.1-2-Linux-aarch64.sh
2.安装:
	chmod +x Miniconda3-py39_25.1.1-2-Linux-aarch64.sh
	./Miniconda3-py39_25.1.1-2-Linux-aarch64.sh
3.配置文件：/etc/systemd/resolved.conf
4.修改文件：.condarc
	添加以下：
		channels:
          - defaults
        show_channel_urls: true
        default_channels:
          - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
          - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
          - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
        custom_channels:
          conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
          msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
          bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
          menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
          pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
          pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
          simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  5.执行命令：
  		conda config --add channels defaults
  		conda clean --all
		conda update --all
		conda create -n py38 python=3.8
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250307165632218.png" alt="image-20250307165632218" style="zoom: 67%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250307165723681.png" alt="image-20250307165723681" style="zoom:67%;" />

### 11.视频算法运行

```
修改文件
    cd /home/orin/miniconda3/envs/py38_video/lib/python3.8/site-packages/tensorrt
    sudo vim __init__.py
    将其中的 np.bool 替换为 bool 或者 np.bool_；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250310111148758.png" alt="image-20250310111148758" style="zoom: 67%;" />