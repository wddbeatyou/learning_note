## 基于C++的视频算法开发流程

### 一、刷机后必要工具安装

#### 1.安装JetPack开发环境

```
sudo apt update
sudo apt install openssh-server
sudo apt install nvidia-jetpack
```

#### 2.修改cuda的环境变量

```
sudo vim ~/.bashrc
添加内容：
	export CUDA_HOME=/usr/local/cuda-11.4
    export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH
    export PATH=/usr/local/cuda-11.4/bin:/usr/local/bin/cmake:$PATH
source ~/.bashrc
验证cuda安装情况：
	nvcc -V
	dpkg -l libcudnn8
	dpkg -l tensorrt
	dpkg -l libopencv
```

#### 3.安装jtop系统监控工具

```
sudo apt install python3-pip
sudo -H pip3 install -U pip
sudo -H pip install jetson-stats
查看：
	sudo systemctl restart jtop.service
	sudo jtop
```

#### 4.**安装****DeepStream**

```
安装依赖：
    sudo apt install -y libssl-dev libgstreamer1.0-0 gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav libgstrtspserver-1.0-0 libjansson-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstrtspserver-1.0-dev libx11-dev libyaml-cpp-dev
    
重新安装nvidia-l4t的相关库：
	sudo apt install --reinstall -y nvidia-l4t-gstreamer nvidia-l4t-multimedia nvidia-l4t-core
安装DeepStream-6.2
	sudo tar -xvf deepstream_sdk_v6.2.0_jetson.tbz2 -C /
    cd /opt/nvidia/deepstream/deepstream-6.2
    sudo ./install.sh
    sudo ldconfig
验证：
	deepstream-app  --version-all
```

### 二、cmake源码编译

```
卸载旧版本 CMake
    sudo apt remove --purge cmake
    sudo apt autoremove

准备编译环境
    sudo apt update
    sudo apt install build-essential libssl-dev

下载 CMake 源码
	wget https://github.com/Kitware/CMake/releases/download/v3.27.7/cmake-3.27.7.tar.gz

解压源码包
	# tar -zxvf cmake-3.27.7.tar.gz
	unzip CMake-3.27.7.zip
进入源码目录
	# cd cmake-3.27.7
	cd CMake-3.27.7
配置编译选项
	./bootstrap --prefix=/usr/local/cmake-3.27.7    // 15min左右

编译源码
	make -j$(nproc)  //10min左右

安装 CMake
	sudo make install

配置环境变量
    echo 'export PATH=/usr/local/cmake-3.27.7/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
修改权限（可选，如果不修改权限，后续执行该命令时加上sudo）
    sudo chown -R orin:orin /usr/local/cmake-3.27.7
验证安装
    cmake --version
```

### 三、编译 jetson-ffmpeg

```
下载：
	sudo apt install -y build-essential checkinstall pkg-config yasm git gfortran
    git clone https://github.com/Keylost/jetson-ffmpeg.git
	cd jetson-ffmpeg && mkdir build && cd build
编译：
    cmake ..
    make -j$(nproc)
    sudo make install
    sudo ldconfig
```

### 四、编译 ffmpeg

```
下载：
    git clone git://source.ffmpeg.org/ffmpeg.git -b release/7.1 --depth=1
    cd jetson-ffmpeg
    ./ffpatch.sh ../ffmpeg
    cd ../ffmpeg
依赖：
	sudo apt install libx264-dev libx265-dev
配置：
	sudo ./configure --enable-nonfree --enable-gpl --enable-cuda-nvcc --enable-nvmpi --enable-libx264 --enable-libx265 --extra-cflags="-I/usr/local/cuda-11.4/include -fPIC" --extra-ldflags="-L/usr/local/cuda-11.4/lib64" --nvcc="/usr/local/cuda-11.4/bin/nvcc" --enable-shared
编译：
    sudo make -j$(nproc)
    sudo make install
    sudo ldconfig
查看：
	ffmpeg -version
	sudo chown -R orin:orin /usr/local/include/libavcodec/
	sudo chown -R orin:orin /usr/local/include/libavutil/
	sudo chown -R orin:orin /usr/local/include/libavformat/
	sudo chown -R orin:orin /usr/local/include/libswscale/
	sudo chown -R orin:orin /usr/local/include/libavdevice/
```

### 五、opencv 源码编译

```
卸载opencv：
    sudo apt purge libopencv*
    sudo apt autoremove
    sudo apt update
```

```
安装依赖：
	#sudo apt install -y build-essential checkinstall pkg-config yasm git gfortran
    sudo apt update
    sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
    sudo apt install -y software-properties-common
    sudo apt install -y libjasper1 libjasper-dev
    sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev libtbb-dev libatlas-base-dev libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev libxvidcore-dev libopencore-amrnb-dev libopencore-amrwb-dev x264 v4l-utils
    sudo apt install -y python3-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
```

```
文件解压：
    unzip opencv-4.6.0.zip
    unzip opencv_contrib-4.6.0.zip
    mv opencv_contrib-4.6.0 ./opencv-4.6.0
    cd opencv-4.6.0 && mkdir build && cd build
```

```
配置：
	sudo cmake \
-D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.6.0/modules \
-D CUDA_ARCH_BIN='8.7' \
-D WITH_CUDA=ON \
-D WITH_GSTREAMER=ON \
-D WITH_GSTREAMER_0_10=OFF \
-D BUILD_opencv_gapi=ON \
-D BUILD_opencv_python3=OFF \
-D BUILD_opencv_python2=OFF \
-D FFMPEG_INCLUDE_DIR=/usr/local/include \
-D FFMPEG_LIBRARIES="/usr/local/lib/libavcodec.so;/usr/local/lib/libavformat.so;/usr/local/lib/libavutil.so;/usr/local/lib/libswscale.so" \
-D WITH_V4L=ON \
-D WITH_QT=OFF \
-D WITH_OPENGL=ON \
-D ENABLE_FAST_MATH=1 \
-D CUDA_FAST_MATH=1 \
-D WITH_CUBLAS=1 \
-D OPENCV_GENERATE_PKGCONFIG=ON \
-D WITH_GTK=ON \
-D BUILD_TESTS=OFF \
-D BUILD_PERF_TESTS=OFF \
-D BUILD_EXAMPLES=OFF \
-D BUILD_opencv_wechat_qrcode=OFF \
-D BUILD_opencv_xfeatures2d=OFF \
.. 
```

```
安装：
	运行时间：50min
	sudo make -j$(nproc) && sudo make install
	sudo chmod -R a+r /usr/local/include/opencv4
```

### 六、docker及docker compose安装

```
sudo apt-get update
sudo apt-get install -y docker.io
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
查看：
	docker compose --version
	docker --version
配置镜像源：
sudo vim /etc/docker/daemon.json
添加以下内容：
	{ 
        "registry-mirrors": ["https://jockerhub.com/",
                            "https://docker.rainbond.cc", 
                            "https://mirror.iscas.ac.cn", 
                            "https://docker.mirrors.ustc.edu.cn",
                            "https://docker.mirrors.sjtug.sjtu.edu.cn",
                            "https://docker.nju.edu.cn",
                            "https://docker.m.daocloud.io",
                            "https://mirror.baidubce.com",
                            "https://dockerproxy.com",
                            "https://mirror.aliyuncs.com",
                            "https://dockertest.jsdelivr.fyi",
                            "https://docker.jsdelivr.fyi",
                            "https://dockercf.jsdelivr.fyi",
                            "https://docker-cf.registry.cyou",
                            "https://docker.registry.cyou"],
        "runtimes": {
            "nvidia": { 
                "path": "nvidia-container-runtime", 
                "runtimeArgs": [] 
            } 
        } 
    }
将当前用户加入 docker 组：
    sudo usermod -aG docker $USER
    newgrp docker
重启docker服务：	
    sudo systemctl daemon-reload
    sudo systemctl restart docker
拉取镜像：
	docker pull bluenviron/mediamtx:latest
设置开机自启：
	docker run -d --name mediamtx -e MTX_RTSPTRANSPORTS=tcp -p 8554:8554 bluenviron/mediamtx
	docker update --restart=always mediamtx
```

### 七、ffmpeg 推流

```
ffmpeg -i ./test.mp4 -c:v h264_nvmpi -preset fast ./output.mp4
ffmpeg -stream_loop -1 -re -i test.mp4 -c:v libx264 -preset fast -tune zerolatency -rtsp_transport tcp -f rtsp rtsp://172.20.31.102:8554/live/stream
```

### 八、修改文件权限

```
sudo chown -R orin:orin /usr/local/include/libswscale
sudo chown -R orin:orin /usr/local/include/libav*
sudo chown -R orin:orin /usr/local/include/libavcodec/
...
```

### 九、安装mysql

```
sudo apt-get install libmysqlcppconn-dev
```

### 十、**安装 nlohmann/json 库**

```
sudo apt-get install nlohmann-json3-dev
```

### 十一、安装 Eigen3

```
sudo apt-get install libeigen3-dev
```

