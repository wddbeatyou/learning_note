## 视频盒子软件安装指导手册-Jetson_orin_nano

### 一、安装JetPack

```
第一步：sudo apt update
第二步：sudo apt install nvidia-jetpack -y    # 安装JetPack开发环境
第三步：sudo vim ~/.bashrc                 # 修改cuda的环境变量
       添加内容：
            export CUDA_HOME=/usr/local/cuda-11.4
            export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH
            export PATH=/usr/local/cuda-11.4/bin:/usr/local/bin/cmake:$PATH
第四步：source ~/.bashrc                   # 保存退出，更新环境变量
第五步：查看
	nvcc -V
	dpkg -l libcudnn8
	dpkg -l tensorrt
```

### 二、安装 jtop 系统监控工具

```
执行以下安装命令：
    sudo apt install python3-pip
    sudo -H pip3 install -U pip
    sudo -H pip install jetson-stats
开启这个监控工具：
	sudo jtop        # 如果启动出现错误的话，请重启一下 Jetson Orin 让这个服务完整启动。
```

### 三、**安装 **DeepStream

#### 3.1 glib 安装

```
sudo pip3 install meson
sudo pip3 install ninja
mkdir software && cd software/

git clone https://github.com/GNOME/glib.git
cd glib
git checkout 2.76.6
sudo meson build --prefix=/usr
sudo ninja -C build/
cd build/
sudo ninja install
pkg-config --modversion glib-2.0
```

#### 3.2 依赖安装

```
sudo apt install \
libssl1.1 \
libssl-dev \
libgstreamer1.0-0 \
libgstrtspserver-1.0-dev \
gstreamer1.0-tools \
gstreamer1.0-plugins-good \
gstreamer1.0-plugins-bad \
gstreamer1.0-plugins-ugly \
gstreamer1.0-libav \
libgstreamer-plugins-base1.0-dev \
libgstrtspserver-1.0-0 \
libjansson4 \
libyaml-cpp-dev
```

#### 3.3 安装librdkafka

```
git clone https://github.com/confluentinc/librdkafka.git
cd librdkafka
git checkout tags/v2.2.0
./configure --enable-ssl
make -j6
sudo make install

sudo mkdir -p /opt/nvidia/deepstream/deepstream/lib
sudo cp /usr/local/lib/librdkafka* /opt/nvidia/deepstream/deepstream/lib
sudo ldconfig
```

#### 3.4 deepstream安装

```
方式一：
网址： 
	https://catalog.ngc.nvidia.com/orgs/nvidia/resources/deepstream/files?version=6.3
下载：
	deepstream-6.3_6.3.0-1_arm64.deb
安装：
	sudo apt-get install ./deepstream-6.3_6.3.0-1_arm64.deb

方式二：
	sudo tar -xvf deepstream_sdk_v6.3.0_jetson.tbz2 -C /
    cd /opt/nvidia/deepstream/deepstream-6.3
    sudo ./install.sh
    sudo ldconfig

验证：
	deepstream-app --version-all
```

### 四、其他软件安装

```
sudo apt update
sudo apt install -y libmysqlcppconn-dev nlohmann-json3-dev libeigen3-dev mysql-server cmake 
```
