### 一、mqtt的安装

1.mqtt服务器的安装-EMQX

```
网址：https://www.emqx.com/zh/downloads/broker/v5.3.2
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216135907369.png" alt="image-20241216135907369" style="zoom: 50%;" />

2.mqtt客户端的安装-MQTTX

```
网址：https://mqttx.app/zh/downloads
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216140007074.png" alt="image-20241216140007074" style="zoom:33%;" />

### 二、mqtt服务器的使用

1.mqtt服务器的开启

```
第一步：
	打开cmd，并切换至mqtt安装目录：E:\MQTT\emqx-5.3.2-windows-amd64\bin；
第二步：
	执行命令：./emqx start
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216140605661.png" alt="image-20241216140605661" style="zoom: 80%;" />

2.mqttf服务器的登录

```
第一步：
	打开浏览器，访问网址：http://127.0.0.1:18083/
第二步：
	输入账号密码：
		账号：admin
		密码：public
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216140914144.png" alt="image-20241216140914144" style="zoom: 25%;" />

3.mqtt服务器的基本指令

```
后台启动 EMQ X Broker 
emqx start 
关闭 EMQ X Broker 
emqx stop 
重启 EMQ X Broker 
emqx restart 
使用控制台启动 EMQ X Broker
emqx console  
使用控制台启动 EMQ X Broker，与 emqx console 不同， emqx foreground 不支持输入 Erlang 命令 
emqx foreground 
emqx ping Ping EMQ X Broke  
```

4.mqtt服务器安装目录介绍

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216141452511.png" alt="image-20241216141452511" style="zoom:50%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216141516521.png" alt="image-20241216141516521" style="zoom:50%;" />

### 三、mqttx客户端的使用

参考网址：

```
https://mqttx.app/zh/docs/get-started
```

1.创建连接

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216141931591.png" alt="image-20241216141931591" style="zoom: 80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216142037482.png" alt="image-20241216142037482" style="zoom: 80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216142117159.png" alt="image-20241216142117159" style="zoom: 80%;" />

2.添加订阅

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216142321754.png" alt="image-20241216142321754" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216142356120.png" alt="image-20241216142356120" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216142441202.png" alt="image-20241216142441202" style="zoom: 80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216142518314.png" alt="image-20241216142518314" style="zoom:80%;" />

### 四、添加用户认证

参考网址：

```
https://blog.csdn.net/weixin_41542513/article/details/134328627?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-4-134328627-blog-135287165.235^v43^pc_blog_bottom_relevance_base6&spm=1001.2101.3001.4242.3&utm_relevant_index=6
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216150901936.png" alt="image-20241216150901936" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216150926494.png" alt="image-20241216150926494" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216150942124.png" alt="image-20241216150942124" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216151004383.png" alt="image-20241216151004383" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216151027171.png" alt="image-20241216151027171" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216151045968.png" alt="image-20241216151045968" style="zoom:80%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20241216151104429.png" alt="image-20241216151104429" style="zoom:80%;" />











