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

#### 4.**安装**DeepStream

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

### 八、播放器选择

#### 1.**WebRTC** (优先选择)与VLC

```
1、协议与传输方式差异：VLC 通常使用 RTMP/HTTP-FLV/HLS，而 WebRTC 使用 UDP + 低延迟优化
    VLC 卡顿原因：
        RTMP/HTTP-FLV 基于 TCP，受丢包重传影响，网络抖动时容易卡顿。HLS 依赖分片传输，默认延迟较高（通常 6~10 秒），不适合实时场景。
    WebRTC 流畅原因：
        基于 UDP（SRTP/RTCP），支持丢包恢复和动态码率调整，延迟极低（<500ms）。 内置 NACK（丢包重传）、FEC（前向纠错） 等抗丢包机制。
    解决方案：
		如果必须用 VLC，尝试改用 低延迟 HLS 或 WebRTC 协议（部分 VLC 版本支持）：
			ffmpeg -i input -c:v libx264 -f hls -hls_flags low_latency ...	
2、缓冲策略不同
	（1）VLC 默认缓冲较大
        VLC 会缓存 2~5 秒 数据以减少卡顿，但在实时场景中反而导致延迟累积。
        调整 VLC 缓冲：
        	图形界面：工具 -> 首选项 -> 输入/编解码器 -> 高级 -> 文件缓存（ms）。
        	命令行启动 VLC 时强制低延迟：
        		vlc --network-caching=300  # 单位：毫秒（建议 300~500ms）
     （2）WebRTC 动态调整缓冲
		WebRTC 会根据网络状况动态调整缓冲（通常 <1 秒），更适合实时流。
3、解码与渲染效率
    VLC：可能默认使用 软件解码（尤其在不支持硬解的平台上），导致高 CPU 占用和卡顿。
    WebRTC浏览器：通常启用 硬件加速解码（如 Chrome 的 VA-API/DXVA2）。
    解决方案：
        强制 VLC 使用硬件解码：
            vlc --avcodec-hw=any  # 尝试启用硬解
        检查 FFmpeg 是否输出适合硬解的格式（如 h264_cuvid 解码后转 h264_nvenc 编码）。
4、时间戳（PTS/DTS）问题
	FFmpeg 推流时未正确生成时间戳：如果视频流的时间戳不连续或错误，VLC 会尝试缓冲修正，而 WebRTC 可能直接丢帧。
    解决方案：
        确保 FFmpeg 生成严格递增的 PTS：
    		ffmpeg -i input -vsync 0 -enc_time_base -1 -fflags +genpts ...
        使用 -re 参数模拟实时流（如果源非实时）：
            ffmpeg -re -i input ...
5、封装格式与流优化
	VLC 对某些封装格式处理不佳：例如，FLV 格式的元信息不完整可能导致 VLC 解析卡顿。
    解决方案：
        换用更稳定的封装格式（如 MPEG-TS）：
        	ffmpeg -i input -f mpegts udp://@:1234
        确保 FFmpeg 输出流包含关键帧间隔（GOP）：
        	-g 50 -keyint_min 25  # 每50帧一个关键帧
6、网络适应性
	WebRTC 的动态码率调整：WebRTC 会根据网络带宽自动调整分辨率/码率（如 RTCP Feedback），而 VLC 无此功能。
    解决方案：
        在 FFmpeg 中启用 动态码率（需配合支持的服务端）：
        	-x264-params "nal-hrd=cbr" -b:v 1M -maxrate 1M -minrate 1M -bufsize 1M
```

### 九、修改文件权限

```
sudo chown -R orin:orin /usr/local/include/libswscale
sudo chown -R orin:orin /usr/local/include/libav*
sudo chown -R orin:orin /usr/local/include/libavcodec/
...
```

### 十、安装mysql

```
sudo apt-get install libmysqlcppconn-dev
```

### 十一、安装 nlohmann/json 库

```
sudo apt-get install nlohmann-json3-dev
```

### 十二、安装 Eigen3

```
sudo apt-get install libeigen3-dev
```

