## VScode连接ubuntu服务器--C++模式

### 前言：

```
参考网址：
	https://blog.csdn.net/weixin_52159554/article/details/134406628
```

### 一、下载和安装：

```
下载：
	https://code.visualstudio.com/
安装：
	略
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311185320045.png" alt="image-20250311185320045" style="zoom: 33%;" />

### 二、配置C++环境

```
c_cpp_properties.json：
	该文件主要用于配置 C/C++ 编译器的相关属性，帮助 VS Code 了解项目的编译环境，从而提供准确的代码智能提示、语法检查和代码导航等功能。
注意：
	主要用于配置 C/C++ 语言的编译环境和 IntelliSense（智能感知）功能，帮助 VS Code 更好地理解和处理 C/C++ 代码；可选
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311190221864.png" alt="image-20250311190221864" style="zoom:50%;" />

```
launch.json：
	该文件用于配置调试器的启动参数，定义了如何启动和调试程序。当你在 VS Code 中启动调试会话时，会根据这个文件中的配置来运行程序并连接调试器。
注意：
	调试程序时必须配置；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311190205721.png" alt="image-20250311190205721" style="zoom:50%;" />

```
tasks.json：
	该文件用于配置自定义任务，例如编译程序、运行脚本等。在 VS Code 中，你可以通过命令面板（Ctrl + Shift + P 或 Cmd + Shift + P）执行这些任务。
注意：
	运行程序时必须配置
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311185900060.png" alt="image-20250311185900060" style="zoom:50%;" />

### 三、依赖安装

#### 3.1 安装C/C++插件

```
作用：
	不参与代码的编译，至提供代码编辑与智能提示；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311190852980.png" alt="image-20250311190852980" style="zoom: 50%;" />

#### 3.2 下载 MinGW-w64

```
作用：
	编译C++代码，生成可执行文件；
下载地址：
	https://sourceforge.net/projects/mingw-w64/files/
安装：
	直接解压，存放在英文目录，切记，再添加环境变量；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311192231351.png" alt="image-20250311192231351" style="zoom:50%;" />

#### 3.3 安装Remote-SSH插件(可选)

```
作用：
	保证vscode等远程登录服务器终端；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311193043269.png" alt="image-20250311193043269" style="zoom:50%;" />

```
参考网址：
	https://zhuanlan.zhihu.com/p/699293658
配置：
	第一步：
		按住“Ctrl + Shift + p”，输入“Remote-SSH”;
	第二步：
		选择“Remote-SsH: 打开 SSH 配置文件...”，再选择“C:\Users\DELLl.sshlconfig”；
	第三步：
		配置下列信息：
			Host 172.20.31.102
                HostName 172.20.31.102
                User orin
                ForwardX11 yes
                ForwardX11Trusted yes
                ForwardAgent yes
	第四步：
        找到本地winows下文件夹：C:\Users\DELL\.ssh，打开文件id_rsa.pub，后续需要复制到远程服务器中；如果没有文件id_rsa.pub，则输入以下命令：“ssh-keygen -t rsa”，便可生成；
	第五步：
		通过终端或其他方式进入远程服务器，创建文件“/home/orin/.ssh/authorized_keys”,将文件id_rsa.pub中内容复制过去即可；
		mkdir /home/orin/.ssh
		chmod 700 /home/orin/.ssh
		cd /home/orin/.ssh && vim authorized_keys
		chmod 600 /home/orin/.ssh/authorized_keys
	第六步：
		使用vscode连接远程服务器，将本机的文件，直接拖入vscode的目录栏中，即可实现文件的上传，无需繁琐的scp命令进行上传；要从服务器下载文件到本机的话，暂不支持拖拽下载。但是，在文件上点击右键，然后点击下载，也能实现快捷的下载功能。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311193447901.png" alt="image-20250311193447901" style="zoom: 50%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311193714276.png" alt="image-20250311193714276" style="zoom:67%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311193835883.png" alt="image-20250311193835883" style="zoom:50%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311194032327.png" alt="image-20250311194032327" style="zoom:50%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311195645843.png" alt="image-20250311195645843" style="zoom:50%;" />

#### 3.4 下载 Xming-6-9-0-31-setup.exe(可选)

```
参考网址：
	https://blog.csdn.net/Mario_z/article/details/121250331
作用：
	实现图形界面远程显示，允许用户在 Windows 系统中远程连接到 UNIX 或 Linux 服务器，并在本地显示服务器上的图形化应用程序界面。比如，用户在 Windows 电脑上通过 Xming 连接到 Linux 服务器后，可以在本地打开服务器上的 GIMP 图像编辑软件、OpenOffice 办公软件等，就像在本地运行一样，方便用户操作和使用服务器上的各种图形化工具；
下载：
	https://sourceforge.net/projects/xming/files/latest/download
配置：
	按以下方式进行配置，配置完成后运行代码报错，可能还需进行opencv源码编译；
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311200100817.png" alt="image-20250311200100817" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311200151283.png" alt="image-20250311200151283" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311200223633.png" alt="image-20250311200223633" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311200254450.png" alt="image-20250311200254450" style="zoom: 80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311200354725.png" alt="image-20250311200354725" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250311200546429.png" alt="image-20250311200546429" style="zoom:50%;" />

**重新安装OpenCV**

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
6.安装：
	sudo make -j$(nproc) && sudo make install 
注意：
	后续可能遇到opencv4.pc的修改问题；
	sudo mv /usr/lib/aarch64-linux-gnu/pkgconfig/opencv4.pc /usr/lib/aarch64-linux-gnu/pkgconfig/opencv4.pc.bak
	sudo rm /usr/lib/aarch64-linux-gnu/pkgconfig/opencv4.pc
	pkg-config --modversion opencv4
	sudo chmod 755 /usr/local/lib/pkgconfig
	echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH' >> ~/.bashrc
	source ~/.bashrc
	pkg-config --modversion opencv4
```

### 四、运行C++图片展示（远程图片在本地展示）

```
#include <opencv2/opencv.hpp>
#include <iostream>

int main()
{
    // 读取图片
    cv::Mat image = cv::imread("/home/orin/project/c_project/dianchui.jpg", cv::IMREAD_COLOR);
    // 检查图片是否成功读取
    if (image.empty())
    {
        std::cout << "Could not open or find the image" << std::endl;
        return -1;
    }
    // 创建一个窗口并显示图片
    // cv::setWindowProperty("Display window", cv::WND_PROP_FULLSCREEN, cv::WINDOW_FULLSCREEN);
    cv::namedWindow("Display window", cv::WINDOW_AUTOSIZE);
    cv::imshow("Display window", image);
    // 等待用户按键
    cv::waitKey(0);
    return 0;
}
```

五、待定



























