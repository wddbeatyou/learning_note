## 基于C++的docker视频跟踪算法部署

### 一、docker安装

```
执行命令：
    sudo apt-get update
    sudo apt-get install docker.io docker-compose
    sudo chmod -R o+r /usr/local/lib/python3.8/dist-packages/
    sudo chown -R $USER:$USER /usr/local/lib/python3.8/dist-packages/
将当前用户加入 docker 组：
    sudo usermod -aG docker $USER
    newgrp docker
    sudo systemctl daemon-reload
	sudo systemctl restart docker
查看版本命令：
	docker --version
	docker-compose --version
配置镜像源：
	{
    "registry-mirrors": [
        "https://jockerhub.com/",
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
        "https://docker.registry.cyou"
    ],
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    }
}
重启docker：
	sudo systemctl daemon-reload
	sudo systemctl restart docker
```

### 二、镜像拉取

```
1.拉取支持cuda的镜像环境
	docker pull nvcr.io/nvidia/l4t-base:35.4.1
2.生成容器
    docker run -it --runtime=nvidia --name=video_arm64 nvcr.io/nvidia/l4t-base:35.4.1 bash
3.进入容器
	docker exec -it video_arm64 bash
```

### 三、环境搭建

#### 1.cmake源码编译

```
卸载旧版本 CMake
    apt remove --purge cmake
    apt autoremove
准备编译环境
    apt update
    apt install build-essential libssl-dev
下载 CMake 源码
	wget https://github.com/Kitware/CMake/releases/download/v3.27.7/cmake-3.27.7.tar.gz
解压源码包，并进入源码目录
	unzip CMake-3.27.7.zip
	cd CMake-3.27.7
配置编译选项
	./bootstrap --prefix=/usr/local/cmake-3.27.7    // 15min左右
编译和安装源码
	make -j$(nproc)  //10min左右
	make install
配置环境变量
    echo 'export PATH=/usr/local/cmake-3.27.7/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
```

#### 2.cuda安装

```
cuda,cudnn和tensorrt安装：
	apt install cuda
	apt install libcudnn8-dev
	apt install tensorrt
配置环境：
	echo "export PATH=$PATH:/usr/local/cuda/bin" >> ~/.bashrc
	echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
	source ~/.bashrc
版本查看：
	nvcc -V
	dpkg -l libcudnn8
	dpkg -l tensorrt
```

#### 3.ffmpeg 源码编译

```
1.环境准备和依赖安装
	# 将主机环境的jetson_multimedia_api复制到docker容器中，不然编译会报错
	docker cp /usr/src/jetson_multimedia_api 3f49cf1fc353:/usr/src/jetson_multimedia_api 
	apt install libx264-dev libx265-dev
2.编译 jetson-ffmpeg
	sudo apt install -y build-essential checkinstall pkg-config yasm git gfortran
    git clone https://github.com/Keylost/jetson-ffmpeg.git
	cd jetson-ffmpeg && mkdir build && cd build
	cmake ..
    make -j$(nproc)
    make install
    ldconfig
3.编译 ffmpeg
	git clone git://source.ffmpeg.org/ffmpeg.git -b release/7.1 --depth=1
    cd jetson-ffmpeg
    ./ffpatch.sh ../ffmpeg
    cd ../ffmpeg
    
	./configure --enable-nonfree --enable-gpl --enable-cuda-nvcc --enable-nvmpi --enable-libx264 --enable-libx265 --extra-cflags="-I/usr/local/cuda/include -fPIC" --extra-ldflags="-L/usr/local/cuda/lib64" --nvcc="/usr/local/cuda/bin/nvcc" --enable-shared
	
	make -j$(nproc)
	make install
	ldconfig
4.版本查看：
	ffmpeg -version
```

#### 4.opencv 源码编译

```
1.卸载opencv：
    apt purge libopencv*
    apt autoremove
    apt update
2.安装依赖：
	apt update
    apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
    apt install -y software-properties-common
    apt install -y libjasper1 libjasper-dev
    apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev libtbb-dev libatlas-base-dev libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev libxvidcore-dev libopencore-amrnb-dev libopencore-amrwb-dev x264 v4l-utils
    apt install -y python3-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
3.文件解压：
    unzip opencv-4.6.0.zip
    unzip opencv_contrib-4.6.0.zip
    mv opencv_contrib-4.6.0 ./opencv-4.6.0
    cd opencv-4.6.0 && mkdir build && cd build
4.编译
	cmake \
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
5.修改配置文件“ffmpeg_codecs.hpp”
	apt install vim
	vim /tmp/opencv-4.6.0/modules/videoio/src/ffmpeg_codecs.hpp
	注释一下代码：
		// #if (LIBAVCODEC_VERSION_INT <= AV_VERSION_INT(54, 51, 100))
        // #define AV_CODEC_ID_H264 CODEC_ID_H264
        // #define AV_CODEC_ID_H263 CODEC_ID_H263
        // #define AV_CODEC_ID_H263P CODEC_ID_H263P
        // #define AV_CODEC_ID_H263I CODEC_ID_H263I
        // #define AV_CODEC_ID_H261 CODEC_ID_H261
        // #define AV_CODEC_ID_MPEG4 CODEC_ID_MPEG4
        // #define AV_CODEC_ID_MSMPEG4V3 CODEC_ID_MSMPEG4V3
        // #define AV_CODEC_ID_MSMPEG4V2 CODEC_ID_MSMPEG4V2
        // #define AV_CODEC_ID_MSMPEG4V1 CODEC_ID_MSMPEG4V1
        // #define AV_CODEC_ID_WMV1 CODEC_ID_WMV1
        // #define AV_CODEC_ID_WMV2 CODEC_ID_WMV1
        // #define AV_CODEC_ID_DVVIDEO CODEC_ID_DVVIDEO
        // #define AV_CODEC_ID_MPEG1VIDEO CODEC_ID_MPEG1VIDEO
        // #define AV_CODEC_ID_MPEG2VIDEO CODEC_ID_MPEG2VIDEO
        // #define AV_CODEC_ID_MJPEG CODEC_ID_MJPEG
        // #define AV_CODEC_ID_LJPEG CODEC_ID_LJPEG
        // #define AV_CODEC_ID_HUFFYUV CODEC_ID_HUFFYUV
        // #define AV_CODEC_ID_FFVHUFF CODEC_ID_FFVHUFF
        // #define AV_CODEC_ID_CYUV CODEC_ID_CYUV
        // #define AV_CODEC_ID_RAWVIDEO CODEC_ID_RAWVIDEO
        // #define AV_CODEC_ID_INDEO3 CODEC_ID_INDEO3
        // #define AV_CODEC_ID_VP3 CODEC_ID_VP3
        // #define AV_CODEC_ID_ASV1 CODEC_ID_ASV1
        // #define AV_CODEC_ID_ASV2 CODEC_ID_ASV2
        // #define AV_CODEC_ID_VCR1 CODEC_ID_VCR1
        // #define AV_CODEC_ID_FFV1 CODEC_ID_FFV1
        // #define AV_CODEC_ID_XAN_WC4 CODEC_ID_XAN_WC4
        // #define AV_CODEC_ID_MSRLE CODEC_ID_MSRLE
        // #define AV_CODEC_ID_MSVIDEO1 CODEC_ID_MSVIDEO1
        // #define AV_CODEC_ID_CINEPAK CODEC_ID_CINEPAK
        // #define AV_CODEC_ID_TRUEMOTION1 CODEC_ID_TRUEMOTION1
        // #define AV_CODEC_ID_MSZH CODEC_ID_MSZH
        // #define AV_CODEC_ID_ZLIB CODEC_ID_ZLIB
        // #define AV_CODEC_ID_SNOW CODEC_ID_SNOW
        // #define AV_CODEC_ID_4XM CODEC_ID_4XM
        // #define AV_CODEC_ID_FLV1 CODEC_ID_FLV1
        // #define AV_CODEC_ID_SVQ1 CODEC_ID_SVQ1
        // #define AV_CODEC_ID_TSCC CODEC_ID_TSCC
        // #define AV_CODEC_ID_ULTI CODEC_ID_ULTI
        // #define AV_CODEC_ID_VIXL CODEC_ID_VIXL
        // #define AV_CODEC_ID_QPEG CODEC_ID_QPEG
        // #define AV_CODEC_ID_WMV3 CODEC_ID_WMV3
        // #define AV_CODEC_ID_LOCO CODEC_ID_LOCO
        // #define AV_CODEC_ID_THEORA CODEC_ID_THEORA
        // #define AV_CODEC_ID_WNV1 CODEC_ID_WNV1
        // #define AV_CODEC_ID_AASC CODEC_ID_AASC
        // #define AV_CODEC_ID_INDEO2 CODEC_ID_INDEO2
        // #define AV_CODEC_ID_FRAPS CODEC_ID_FRAPS
        // #define AV_CODEC_ID_TRUEMOTION2 CODEC_ID_TRUEMOTION2
        // #define AV_CODEC_ID_FLASHSV CODEC_ID_FLASHSV
        // #define AV_CODEC_ID_JPEGLS CODEC_ID_JPEGLS
        // #define AV_CODEC_ID_VC1 CODEC_ID_VC1
        // #define AV_CODEC_ID_CSCD CODEC_ID_CSCD
        // #define AV_CODEC_ID_ZMBV CODEC_ID_ZMBV
        // #define AV_CODEC_ID_KMVC CODEC_ID_KMVC
        // #define AV_CODEC_ID_VP5 CODEC_ID_VP5
        // #define AV_CODEC_ID_VP6 CODEC_ID_VP6
        // #define AV_CODEC_ID_VP6F CODEC_ID_VP6F
        // #define AV_CODEC_ID_JPEG2000 CODEC_ID_JPEG2000
        // #define AV_CODEC_ID_VMNC CODEC_ID_VMNC
        // #define AV_CODEC_ID_TARGA CODEC_ID_TARGA
        // #define AV_CODEC_ID_NONE CODEC_ID_NONE
        // #endif
6.编译
	make -j$(nproc) && make install
7.查看版本
    # 检查库文件是否存在
    ls /usr/local/lib/libopencv_*
    # 检查头文件
    ls /usr/local/include/opencv4/
    # 验证版本
    opencv_version
```

#### 5..**安装**DeepStream

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

#### 6.安装mysql

6.1 客户端的搭建

```
apt install libmysqlcppconn-dev
```

6.2 服务器的搭建

```
更新：
    sudo apt update
    sudo apt upgrade -y
安装：
	sudo apt install mysql-server -y
启动并设置开机自启：
    sudo systemctl start mysql
    sudo systemctl enable mysql
验证 MySQL 服务状态：
	sudo systemctl status mysql
验证 MySQL 服务状态：
	sudo mysql_secure_installation
登录 MySQL：
	sudo mysql -u root -p
修改密码策略：
	-- 设置密码策略为 LOW
    SET GLOBAL validate_password.policy = LOW;
    -- 设置密码最小长度为 4
    SET GLOBAL validate_password.length = 4;
创建用户：
	CREATE USER 'sysadmin'@'%' IDENTIFIED BY 'adminsys';
授予用户权限：
	GRANT ALL PRIVILEGES ON icms.* TO 'sysadmin'@'%';
修改MySQL 监听地址配置：
	# 编辑 MySQL 配置文件 mysqld.cnf，一般路径为 /etc/mysql/mysql.conf.d/mysqld.cnf，找到 bind-address 这一行，将其修改为 0.0.0.0；
	bind-address = 0.0.0.0
再次修改用户密码：
	ALTER USER 'sysadmin'@'%' IDENTIFIED WITH mysql_native_password BY 'adminsys';
	FLUSH PRIVILEGES;
重启 MySQL 服务：
	sudo systemctl restart mysql
刷新权限使设置生效：
	FLUSH PRIVILEGES;
查看当前密码策略：
	SHOW VARIABLES LIKE 'validate_password%';
```

#### 7.安装 nlohmann/json 库

```
apt install nlohmann-json3-dev
```

#### 8.安装 Eigen3

```
apt install libeigen3-dev
```

### 四、算法运行









