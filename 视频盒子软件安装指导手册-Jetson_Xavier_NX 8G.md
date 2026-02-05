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
	sudo systemctl restart jtop.service
	sudo jtop        # 如果启动出现错误的话，请重启一下 Jetson Orin 让这个服务完整启动。
```

### 三、**安装 **DeepStream

#### 3.1 glib 安装

```
sudo pip3 install meson
sudo pip3 install ninja
mkdir project && cd project/

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
	https://developer.nvidia.com/downloads/deepstream-62-620-1-arm64-deb
下载：
	deepstream-6.2_6.2.0-1_amd64.deb
安装：
	sudo apt-get install ./deepstream-6.2_6.2.0-1_amd64.deb

方式二：
	sudo tar -xvf deepstream_sdk_v6.3.0_jetson.tbz2 -C /
    cd /opt/nvidia/deepstream/deepstream-6.3
    sudo ./install.sh
    sudo ldconfig

验证：
	deepstream-app --version-all
```

### 四、deepstream项目docker部署

#### 4.1 docker安装

```
# 添加官方秘钥：Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 添加 Docker 官方软件仓库到 APT 源列表：Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl status docker
sudo systemctl start docker

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
sudo systemctl is-enabled docker
```

#### 4.2 nvidia-container-toolkit安装

**说明：**

​	NVIDIA Container Toolkit 是 **Docker 容器调用 NVIDIA GPU 时的必备工具**，只有安装它，才能实现：

- 在 Docker 容器内部访问主机的 NVIDIA 显卡（如运行 GPU 加速的程序）。
- 容器内正常使用 CUDA、cuDNN 等 GPU 计算库。

```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
export NVIDIA_CONTAINER_TOOLKIT_VERSION=1.17.8-1
sudo apt-get install -y \
  nvidia-container-toolkit=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  nvidia-container-toolkit-base=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  libnvidia-container-tools=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  libnvidia-container1=${NVIDIA_CONTAINER_TOOLKIT_VERSION}
```

#### 4.3 如何实现deepstream镜像拉取

```
1.注册NGC账号
2.登录进去：
	点击页面右上角的用户名，在下拉菜单中选择 “Setup”。
    在 “Setup” 页面中，点击 “Get API Key” 选项。
    进入生成 API Key 的页面后，点击 “Generate API Key” 按钮。
    系统会弹出确认对话框，点击 “Confirm” 按钮。
    此时页面会显示生成的 API Key，它会在 “Password” 处显示一连串字符，这个字符就是你的 NGC API Key。
3.复制 API Key
	7c91ecc5-5cde-4ee7-9059-95d813be434b
4.执行以下命令：
	docker login nvcr.io
	Username: $oauthtoken
	Password: 7c91ecc5-5cde-4ee7-9059-95d813be434b
5.拉取deepstream镜像
	# 基础镜像：仅包含运行时库和GStreamer插件。可用作构建DeepStream应用程序自定义docker的基础
    docker pull nvcr.io/nvidia/deepstream:6.2-base
    # 开发镜像：包含整个SDK以及用于构建DeepStream应用程序和图形编辑器的开发环境
    docker pull nvcr.io/nvidia/deepstream:6.2-devel
    # 可选：安装了Triton Influence Server和依赖项，以及用于构建DeepStream应用程序的开发环境
    docker pull nvcr.io/nvidia/deepstream:6.2-triton
	
```

### 五、其他软件安装

```
sudo apt update
sudo apt install -y libmysqlcppconn-dev nlohmann-json3-dev libeigen3-dev mysql-server cmake 
sudo systemctl start mysql
sudo systemctl enable mysql
```

```
sudo mysql -u root -p
CREATE DATABASE icms;

-- 创建允许任何 IP 连接的用户（使用 '%' 通配符）
CREATE USER 'sysadmin'@'%' IDENTIFIED BY 'adminsys';

-- 授予必要的权限
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP ON icms.* TO 'sysadmin'@'%';

修改MySQL 监听地址配置：
	# 编辑 MySQL 配置文件 mysqld.cnf，一般路径为 /etc/mysql/mysql.conf.d/mysqld.cnf，找到 bind-address 这一行，将其修改为 0.0.0.0；
	bind-address = 0.0.0.0
	
-- 刷新权限
FLUSH PRIVILEGES;

-- 验证用户权限
SELECT user, host FROM mysql.user WHERE user = 'sysadmin';
SHOW GRANTS FOR 'sysadmin'@'%';
```

### 六、开机自启

```
1.创建配置文件
	sudo vim /etc/systemd/system/video-analysis.service
    配置文件内容：
        [Unit]
        Description=Video Analysis Service
        After=network.target mysql.service
        Wants=network.target mysql.service

        [Service]
        Type=simple
        User=orin
        Group=orin
        WorkingDirectory=/home/orin/project/video_analysis/build
        ExecStart=/home/orin/project/video_analysis/build/video_analysis
        ExecStop=/bin/kill -TERM $MAINPID
        Restart=always
        RestartSec=10
        StandardOutput=append:/home/orin/project/video_analysis/logs/video_analysis.log
        StandardError=append:/home/orin/project/video_analysis/logs/video_analysis.log

        # 仅保留必要的 GPU 环境变量
        Environment=LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/lib/aarch64-linux-gnu
        Environment=NVIDIA_DRIVER_CAPABILITIES=compute,utility,video,graphics

        # 资源限制
        LimitCORE=infinity
        LimitNOFILE=65536
        LimitMEMLOCK=infinity

        # 生产环境优化
        Nice=-5
        OOMScoreAdjust=-500

        [Install]
        WantedBy=multi-user.target

2.启动服务
sudo systemctl daemon-reload
sudo systemctl start video-analysis

# 停止服务
sudo systemctl stop video-analysis

# 重启服务
sudo systemctl restart video-analysis

# 查看服务状态
sudo systemctl status video-analysis

# 查看服务日志
sudo journalctl -u video-analysis -f

# 禁用开机自启
sudo systemctl disable video-analysis

# 启用开机自启
sudo systemctl enable video-analysis
```

