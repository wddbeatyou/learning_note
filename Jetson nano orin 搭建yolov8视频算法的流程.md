## Jetson nano orin 搭建yolov8视频算法的流程

### 一、安装JetPack开发环境

#### 1.1 JetPack简介

```
	Jetpack 是 NVIDIA 为 Jetson 系列嵌入式计算平台（如 Jetson Nano、Jetson Xavier NX、Jetson AGX Xavier 等）提供的一套软件开发工具包（SDK）。它包含了操作系统、驱动程序、库和工具，用于加速 AI 和深度学习应用的开发与部署。包含**CUDA**，**cuDNN**和**TensorRT**等库，不需要单独去一一进行安装。
```

```
第一步：sudo apt update
第二步：sudo apt install nvidia-jetpack    # 安装JetPack开发环境
第三步：sudo vim ~/.bashrc                 # 修改cuda的环境变量
       添加内容：
            export CUDA_HOME=/usr/local/cuda-11.4
            export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH
            export PATH=/usr/local/cuda-11.4/bin:/usr/local/bin/cmake:$PATH
第四步：source ~/.bashrc                   # 保存退出，更新环境变量
```

#### 1.2 检查jetpack安装情况

```
1.检查CUDA安装情况：
	命令：
		nvcc -V
    输出信息：
        nvcc: NVIDIA (R) Cuda compiler driver
        Copyright (c) 2005-2022 NVIDIA Corporation
        Built on Sun_Oct_23_22:16:07_PDT_2022
        Cuda compilation tools, release 11.4, V11.4.315
        Build cuda_11.4.r11.4/compiler.31964100_0
2.检查CUDNN安装情况：
	命令：
		dpkg -l libcudnn8
	输出信息：
		Desired=Unknown/Install/Remove/Purge/Hold
        | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
        |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
        ||/ Name           Version              Architecture Description
        +++-==============-====================-============-==========================>
        ii  libcudnn8      8.6.0.166-1+cuda11.4 arm64        cuDNN runtime libraries
 3.检查TensorRT安装情况：
 	命令：
		dpkg -l tensorrt
	输出信息：
		Desired=Unknown/Install/Remove/Purge/Hold
        | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
        |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
        ||/ Name           Version            Architecture Description
        +++-==============-==================-============-============================>
        ii  tensorrt       8.5.2.2-1+cuda11.4 arm64        Meta package for TensorRT
  4.检查OpenCV安装情况：
  	命令：
		dpkg -l tensorrt
	输出信息：
		Desired=Unknown/Install/Remove/Purge/Hold
        | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
        |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
        ||/ Name           Version             Architecture Description
        +++-==============-===================-============-===========================>
        ii  libopencv      4.5.4-8-g3e4c170df4 arm64        Open Computer Vision Library
```

### 二、安装 jtop 系统监控工具

#### 2.1 jtop 简介

```
jtop是一个监控工具，方便查看各个库和包的安装情况和对应版本
```

```
执行以下安装命令：
    sudo apt install python3-pip
    sudo -H pip3 install -U pip
    sudo -H pip install jetson-stats
开启这个监控工具：
	sudo jtop        # 如果启动出现错误的话，请重启一下 Jetson Orin 让这个服务完整启动。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250121141918638.png" alt="image-20250121141918638" style="zoom: 80%;" />

### 三、**安装 **DeepStream

#### 3.1 DeepStream简介

```
DeepStream 基于 GStreamer 框架，提供了一系列插件用于视频解码、推理、跟踪和显示。
DeepStream：
    使用 NVIDIA 的硬件加速解码器（如 NVDEC）进行视频解码，支持高效的 H.264、H.265 等格式解码。
    能够同时处理多路高分辨率视频流（如 4K、1080p），而不会显著增加 CPU 负载。
OpenCV：
    默认使用 CPU 进行视频解码，性能较低，尤其是在处理高分辨率或多路视频流时，CPU 负载会显著增加。
    虽然 OpenCV 可以通过 FFmpeg 或 GStreamer 后端支持硬件加速，但配置复杂且性能不如 DeepStream。
```

#### 3.2 安装依赖

```
sudo apt install -y libssl-dev libgstreamer1.0-0 gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav libgstrtspserver-1.0-0 libjansson-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstrtspserver-1.0-dev libx11-dev libyaml-cpp-dev
```

#### 3.3 重新安装nvidia-l4t的相关库

```
sudo apt install --reinstall -y nvidia-l4t-gstreamer nvidia-l4t-multimedia nvidia-l4t-core
```

#### 3.4 安装DeepStream-6.2

```
1.下载：deepstream_sdk_v6.2.0_jetson.tbz2 
2.官网：https://developer.nvidia.com/deepstream-sdk-download-tesla-archived   # 此网址下载x86_64架构，arm架构需自己寻找
3.安装：
    sudo tar -xvf deepstream_sdk_v6.2.0_jetson.tbz2 -C /
    cd /opt/nvidia/deepstream/deepstream-6.2
    sudo ./install.sh
    sudo ldconfig
```

#### 3.5 检查安装是否正确

```
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

### 四、重新编译 OpenCV

4.1 OpenCV 简介

```
默认安装的 OpenCV 功能不全；
问题：
	通过 apt-get 或 JetPack 默认安装的 OpenCV 通常是预编译的版本，可能缺少某些功能模块（如 CUDA 支持、GStreamer 支持、Python 绑定等）。
解决方法：
	重新编译 OpenCV，确保启用所需的功能模块。
重新编译的原因：
    启用 CUDA 支持：
        利用 Jetson 的 GPU 加速 OpenCV 的计算任务（如图像处理、深度学习推理）。
    启用 GStreamer 支持：
        支持硬件加速的视频解码和编码，适合处理 RTSP 流和多路视频流。
    优化性能：
        针对 Jetson 的 ARM 架构和 GPU 进行优化，提升 OpenCV 的性能。
    自定义功能模块：
        仅启用所需的模块，减少安装包大小。
    解决依赖问题：
        确保 OpenCV 与 Jetson 上的其他库（如 TensorRT、DeepStream）兼容。
```

#### 4.2 卸载opencv

```
sudo apt purge libopencv*
sudo apt autoremove
sudo apt update
```

#### 4.3 安装依赖

```
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

#### 4.4  下载opencv-4.6.0.zip和opencv_contrib-4.6.0.zip

```
下载 opencv-4.6.0.zip：
	https://github.com/opencv/opencv/tree/4.6.0
下载 opencv_contrib-4.6.0.zip：
	https://github.com/opencv/opencv_contrib/tree/4.6.0
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250121145902266.png" alt="image-20250121145902266" style="zoom:50%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250121150100510.png" alt="image-20250121150100510" style="zoom:50%;" />

#### 4.4  解压 opencv-4.6.0.zip 和 opencv_contrib-4.6.0.zip

```
unzip opencv-4.6.0.zip
unzip opencv_contrib-4.6.0.zip
mv opencv_contrib-4.6.0 ./opencv-4.6.0
cd opencv-4.6.0
mkdir build
cd build
```

#### 4.5 设置opencv的cmake参数

```
在主环境中编译，输入命令：
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
在conda虚拟环境中编译，输入命令：
	cmake -D CMAKE_BUILD_TYPE=RELEASE\
    -D CMAKE_INSTALL_PREFIX=/usr/local\
    -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.6.0/modules\
    -D CUDA_ARCH_BIN='8.7'\
    -D CUDA_ARCH_PTX='8.7' \
    -D WITH_CUDA=1\
    -D BUILD_opencv_python3=1\
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
	-D PYTHON3_EXECUTABLE=/home/orin/software/conda/miniconda3/envs/jetpack_py38/bin/python3.8 \
	-D PYTHON3_INCLUDE_DIR=$(python3.8 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
	-D PYTHON3_LIBRARY=/home/orin/software/conda/miniconda3/envs/jetpack_py38/lib/libpython3.8.so \
	-D PYTHON3_NUMPY_INCLUDE_DIRS=/home/orin/software/conda/miniconda3/envs/jetpack_py38/lib/python3.8/site-packages/numpy/core/include \
    ..
```

#### 4.6 编译和编译安装opencv

```
sudo make -j8 && sudo make install 
```

#### 4.7 验证opencv安装情况

```
python3 -c "import cv2; print(cv2.__version__)"
```

### 五、yolov8环境搭建

#### 5.1 安装ultralytics

```
# ultralytics包含yolov8训练和预测所需的库
pip install ultralytics==8.3.59 -i https://mirrors.aliyun.com/pypi/simple/
```

#### 5.2 安装onnxruntime_gpu

```
简介：
	主要目的是为了加速深度学习模型的推理过程，尤其是在 NVIDIA GPU 上运行 ONNX 格式的模型时。
	GPU 加速：
        ONNX Runtime GPU 利用 NVIDIA GPU 的并行计算能力（通过 CUDA 和 cuDNN），显著加速模型的推理过程。
        对于计算密集型任务（如深度学习模型推理），GPU 的加速效果通常比 CPU 高出数倍甚至数十倍。
    支持多种硬件：
    	ONNX Runtime GPU 不仅支持 NVIDIA GPU，还支持 AMD GPU 和其他支持 CUDA 或 DirectML 的硬件
总之，在yolov8模型转化成tensorrt模型时，需要该库的支持。
```

```
1.下载：onnxruntime_gpu-1.18.0-cp38-cp38-linux_aarch64.whl
2.网址：
	https://elinux.org/Jetson_Zoo#ONNX_Runtime
3. 安装：
	pip install onnxruntime_gpu-1.18.0-cp38-cp38-linux_aarch64.whl
	pip install onnxslim==0.1.47 -i https://mirrors.aliyun.com/pypi/simple/
	pip install onnx==1.17.0 -i https://mirrors.aliyun.com/pypi/simple/
4.查看jetpack版本：
	sudo jetson_release
注意：
	下载onnxruntime_gpu文件时，需要注意jetpack和python版本，不同版本肯能存在不兼容现象；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250121160555494.png" alt="image-20250121160555494" style="zoom: 67%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250121160928941.png" alt="image-20250121160928941" style="zoom: 67%;" />

### 5.3  安装 pytorch 和 torchvision

```
简介：
    PyTorch：
        提供核心的张量计算和深度学习框架，支持 GPU 加速（通过 CUDA）。
    torchvision：
        基于 PyTorch，专门为计算机视觉任务提供工具和模型，依赖于 PyTorch，但不是 PyTorch 的一部分，需要单独安装。
        torchvision 是 PyTorch 的一个官方扩展库，专门用于计算机视觉任务。它提供了以下功能：
            数据集：预加载的常用数据集（如 COCO、CIFAR、MNIST 等）。
            数据预处理：图像变换、数据增强工具（如随机裁剪、旋转、翻转等）。
            模型：预训练的经典计算机视觉模型（如 ResNet、VGG、MobileNet 等）。
            工具函数：如图像读取、保存、可视化等。
```

```
1.卸载torch:
	pip uninstall torch     # 原先的torch无法利用GPU，与CUDA不兼容
2.下载 torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
3.网址：https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
4.安装：
	pip install torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl       # 切换至该文件下
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250121162141919.png" alt="image-20250121162141919" style="zoom: 50%;" />

```
1.下载 vision-release-0.16.zip
2.网址：https://github.com/pytorch/vision/tree/release/0.16
3.安装：
	sudo apt install python3-pip libopenblas-base libopenmpi-dev libomp-dev 
    sudo apt install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev 
    unzip vision-release-0.16.zip
    cd vision-release-0.16
    python3 setup.py install --user
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250121162637172.png" alt="image-20250121162637172" style="zoom: 50%;" />

```
验证pytorch安装情况：
	import torch
	print(torch.__version__)
	print(torch.cuda.is_available())
验证torchvision安装情况：
    import torchvision
    print(torchvision.__version__)
```

### 六、环境配置

#### 6.1 tensorrt的配置

```
# tensorrt是安装在主环境中，虚拟环境无法直接调用，只能通过以下办法创建软连接
ln -s /usr/lib/python3.8/dist-packages/tensorrt /home/x/archiconda3/envs/yolov8/lib/python3.8/site-packages/tensorrt
```

#### 6.2 opencv的配置

```
# opencv编译完成后无法直接调用cv2库，需要将编译后的文件移动到虚拟环境中
cp /home/orin/software/opencv/opencv-4.6.0/build/lib/python3/cv2.cpython-38-aarch64-linux-gnu.so /home/orin/software/conda/miniconda3/envs/jetpack_py38/lib/python3.8/site-packages/
```

#### 6.3 虚拟环境中运行python脚本的流程

```
第一步：conda activate jetpack_py38
第二步：export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstnvvideo4linux2.so:/usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstnvvidconv.so
第三步：python server.py
注意：
	第一步与第二步执行顺序不要弄错；
```

#### 6.4  解决网络摄像头模糊问题

```
import cv2

def camera_play(url_cam):
    url_gstream = (
        'rtspsrc location={} ! '
        'rtph264depay ! '
        'h264parse ! '
        'nvv4l2decoder ! '
        'nvvidconv ! '
        'video/x-raw,width=2560,height=1440,format=(string)BGRx ! '
        'videoconvert ! '
        'video/x-raw,format=(string)BGR ! '
        'appsink drop=true sync=false'
    )    # 硬解码设置
    url =  url_gstream.format(url_cam)
    cap = cv2.VideoCapture(url)
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    url_cam = "rtsp://admin:HuaWei123@172.20.31.91:554/LiveMedia/ch1/Media1/tracklD=1" #根据实际情况修改,海康格式
    camera_play(url_cam)
```

```
解释：
	一般情况下，使用opencv连接网络摄像头读取视频流，会报错：[hevc @ 000001716439ec80] Could not find ref with POC 2，在人员跟踪中无法进行实时检测,
	这是因为边缘设备进行的是软解码，需要进行硬解码，而以上deepstream和opencv的安装编译才能完成硬解码；
```

以上便完成yolov8所需环境的搭建，后面的自己研究。

### 七、 配置opencv动态链接库

```
sudo gedit /etc/ld.so.conf.d/opencv.conf
```

在打开的文件中加入以下语句：

```
/usr/local/lib
```

执行以下语句生效：

```
sudo ldconfig
```

### 八、配置pkg-config

```
sudo gedit /etc/bash.bashrc
```

在打开的文件末尾加入以下语句：

```
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
export PKG_CONFIG_PATH
```

执行以下语句生效：

```
source /etc/bash.bashrc
```

### 九、环境配置验证

```
find ./ -name opencv4.pc    #出现./unix-install/opencv4.pc表示正常
pkg-config --cflags opencv4  #出现-I/usr/local/include/opencv4表示正常
```