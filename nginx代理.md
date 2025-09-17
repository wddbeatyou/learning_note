## 如何通过网页方式访问目录中文件

### 一、拉取镜像

```
docker pull nginx:latest
```

### 二、创建自定义 Nginx 配置文件

```
mkdir /home/supcon/alg/wdd/nginx_server -p
cd /home/supcon/alg/wdd/nginx_server
touch image_compare_server.conf
在文件image_compare_server.conf中添加以下内容：
    server {
        listen       8080; # 容器内 Nginx 监听的端口
        server_name  image_compare_nginx;

        # 设置你要在网页中显示的目录的路径，这个路径是容器内的路径，待会儿我们会通过挂载将主机目录映射到这里
        location / {
            root   /usr/share/nginx/html;
            autoindex on; # 最关键的一行：开启目录列表显示
            autoindex_exact_size off; # 显示文件大小时使用可读格式（K, M, G）
            autoindex_localtime on; # 显示文件修改时间为服务器本地时间
            charset utf-8; # 避免中文文件名乱码
        }
        location /download {
            alias /usr/share/nginx/download/;  # 使用alias而不是root
            autoindex on;
            autoindex_exact_size off;
            autoindex_localtime on;
            charset utf-8;
        }
    }

注释：
    root /usr/share/nginx/html;: 这指定了 Nginx 在容器内寻找文件的根目录。
    autoindex on;: 这是实现目录列表功能的核心指令。
```

### 三、docker部署

#### 3.1 命令行方式

```
docker run -d \
  --name my-nginx-server \
  -p 10026:8080 \
  -v /home/supcon/alg/wdd/image_compare_server_ubuntu2204/image_library:/usr/share/nginx/html:ro \
  -v /home/supcon/alg/wdd/image_compare_server_ubuntu2204/download_image:/usr/share/nginx/download:ro \
  -v /home/supcon/alg/wdd/nginx_server/image_compare_server.conf:/etc/nginx/conf.d/default.conf:ro  \
  nginx:latest
```

#### 3.2 docker-compose方式

```
version: "3"  #版本号

services:
  image-compare-service:  #服务名
    image: image_compare:latest  # 镜像
    network_mode: host
    restart: always
    volumes:
      - ./:/app  #映射到镜像的路径
    working_dir: /app
    entrypoint: ./image_compare_server
    stop_signal: SIGINT # 默认为 SIGTERM 发送 SIGINT 模拟 ctrl + c
    environment:     #时区
      - TZ=Asia/Shanghai
    logging:
      options:
        max-size: "50m"
        max-file: "3"
  nginx-service:  #服务名
    image: nginx:latest  # 镜像
    restart: always
    ports:
      - "10026:8080"
    volumes:
      - /home/supcon/alg/wdd/image_compare_server_ubuntu2204/image_library:/usr/share/nginx/html:ro  #映射到镜像的路径
      - /home/supcon/alg/wdd/image_compare_server_ubuntu2204/download_image:/usr/share/nginx/download:ro
      - /home/supcon/alg/wdd/nginx_server/image_compare_server.conf:/etc/nginx/conf.d/default.conf:ro  #映射到镜像的路径
    environment:     #时区
      - TZ=Asia/Shanghai
    logging:
      options:
        max-size: "50m"
        max-file: "3"

```

### 四、访问网页

```
第一个目录：
	http://172.20.31.6:10026/               # 与image_compare_server.conf文件中location中的 “ / ” 相对应
第二个目录：
	http://172.20.31.6:10026/download/      # 与image_compare_server.conf文件中location中的 “ /download ” 相对应
```



