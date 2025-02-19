## jetson orin nano基于yolov8模型docker部署-------视频分析模型

### 1.安装nvidia-docker2

```
第一步：
	distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
第二步：
	sudo apt-get update
	sudo apt-get install -y nvidia-docker2
第三步：镜像源添加一下内容：
	 "runtimes": {
                        "nvidia": {
                        "path": "nvidia-container-runtime",
                        "runtimeArgs": []
                                }
                        },
     "default-runtime": "nvidia"
注意：
	如果不安装nvidia-docker2，后续拉取镜像源失败；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250219104346666.png" alt="image-20250219104346666" style="zoom: 50%;" />

### 2.拉取镜像

```
1.拉取支持cuda的镜像环境
	docker pull nvcr.io/nvidia/l4t-base:35.4.1
2.生成容器
    docker run -it --name=video_arm64 -v /home/orin/project/icms/construct_manage_arm/docker_config:/docker_config nvcr.io/nvidia/l4t-base:35.4.1 bash
3.进入容器，再安装python和pip(如果镜像中自带python和pip，可选)
    apt-get update
    apt-get update && apt-get install -y python3 python3-pip
```

**注意！注意！注意！：**

```
# 后续操作都是在容器中进行的操作；
docker exec -it video_arm64 bash   # 进入容器
```

### 3.安装cuda，cudnn和tensorrt

```
cudnn安装：
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
	dpkg -i python3-libnvinfer-dev_8.5.2-1+cuda11.4_arm64.deb 
	dpkg -i python3-libnvinfer_8.5.2-1+cuda11.4_arm64.deb 
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
        python3 setup.py install --user   # 15min的运行时间
    查看：
    	import torchvision
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
    cd opencv-4.6.0
    mkdir build
    cd build
5.编译：
	cmake -D CMAKE_BUILD_TYPE=RELEASE\
        -D CMAKE_INSTALL_PREFIX=/usr/local\
        -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.6.0/modules\
        -D CUDA_ARCH_BIN='8.7'\
        -D CUDA_ARCH_PTX='8.7' \
        -D WITH_CUDA=1\
        -D BUILD_opencv_python3=1\
        -D BUILD_opencv_python2=1\
        -D WITH_FFMPEG=1 \
        -D WITH_V4L=ON\
        -D WITH_QT=ON\
        -D WITH_OPENGL=ON\
        -D ENABLE_FAST_MATH=1 \
        -D CUDA_FAST_MATH=1\
        -D WITH_CUBLAS=1\
        -D OPENCV_GENERATE_PKGCONFIG=1\
        -D WITH_GTK_2_X=ON\
        -D WITH_GSTREAMER=ON\
        -D BUILD_TESTS=OFF \
        -D BUILD_PERF_TESTS=OFF \
        -D BUILD_EXAMPLES=OFF \
        ..
6.安装：
	sudo make -j8 && sudo make install 
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

### 8.问题

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

