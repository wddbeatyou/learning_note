## 统信操作系统

### 一、驱动和固件的安装

```
下载网址：https://www.hiascend.com/hardware/firmware-drivers/community?product=2&model=16&cann=8.5.0&driver=Ascend+HDK+25.5.1
安装网址：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0005.html?Mode=PmIns&InstallType=local&OS=openEuler&Software=cannToolKit

安装步骤：
	chmod +x Ascend-hdk-310p-npu-driver_25.5.1_linux-aarch64.run
	chmod +x Ascend-hdk-310p-npu-firmware_7.8.0.6.201.run
	
	./Ascend-hdk-310p-npu-driver_25.5.1_linux-aarch64.run --full --install-for-all
	./Ascend-hdk-310p-npu-firmware_7.8.0.6.201.run --full

    reboot
    npu-smi info
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20260514201558685.png" alt="image-20260514201558685" style="zoom:50%;" />

### 二、Toolkit开发套件包的安装

```
下载网址：https://www.hiascend.com/developer/download/community/result?module=sdk+cann&sdk=7.2.RC1&cann=8.3.RC1
安装网址：https://www.hiascend.com/document/detail/zh/canncommercial/83RC1/softwareinst/instg/instg_0008.html?Mode=PmIns&InstallType=local&OS=Debian&Software=cannToolKit

安装步骤：
	chmod +x /home/alg/software/Ascend-cann-toolkit_8.3.RC1_linux-aarch64.run
	./Ascend-cann-toolkit_8.3.RC1_linux-aarch64.run --install
添加环境变量：
	vim ~/.bashrc （在文件中添加：source ${HOME}/Ascend/ascend-toolkit/set_env.sh）
	source ~/.bashrc
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20260514202305390.png" alt="image-20260514202305390" style="zoom: 50%;" />

### 三、依赖安装

```
安装网址：https://www.hiascend.com/document/detail/zh/mindsdk/72rc1/vision/visionug/mxvisionug_0008.html
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20260515092236465.png" alt="image-20260515092236465" style="zoom:50%;" />

### 四、安装Vision SDK

```
下载网址：https://www.hiascend.com/developer/download/community/result?module=sdk+cann&sdk=7.2.RC1&cann=8.3.RC1
安装网址：https://www.hiascend.com/document/detail/zh/mindsdk/72rc1/vision/visionug/mxvisionug_0012.html

安装步骤：
	chmod +x /home/alg/software/Ascend-mindxsdk-mxvision_7.2.RC1_linux-aarch64.run
	./Ascend-mindxsdk-mxvision_7.2.RC1_linux-aarch64.run --install --install-path=/home/alg/software/Mind_SDK
添加环境变量：
	vim ~/.bashrc （在文件中添加：source /home/alg/software/Mind_SDK/mxVision/set_env.sh）
	source ~/.bashrc
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20260514202129566.png" alt="image-20260514202129566" style="zoom:50%;" />



```
dnf install -y eigen3-devel
yum install mysql-server -y
yum install mysql-devel -y
```



























