## NTP服务同步

#### 一、ntp服务器

```
1. 安装ntp
	# 先确保systemd-timesyncd已关闭
    sudo timedatectl set-ntp off

    # 安装ntp
    sudo apt update
    sudo apt install ntp -y
2.配置NTP服务器
	sudo vim /etc/ntp.conf
	添加内容：
		restrict 172.20.0.0 mask 255.255.255.0 nomodify notrap
3.启动并验证服务
	# 重启ntp服务
    sudo systemctl restart ntp

    # 设置开机自启
    sudo systemctl enable ntp

    # 检查服务状态
    sudo systemctl status ntp

    # 查看上游服务器同步状态
    ntpq -p

    # 查看服务器是否在监听
    netstat -ulnp | grep 123
```

#### 二、客户端

```
1.修改配置文件：
	sudo vim /etc/systemd/timesyncd.conf
	修改内容：
		[Time]
         # 设置你要同步的NTP服务器
         NTP=172.20.31.9
         # 可以设置备用服务器
         FallbackNTP=ntp.ubuntu.com
 2.重启服务
 	sudo systemctl restart systemd-timesyncd
 3.验证同步状态
 	timedatectl timesync-status
 	timedatectl status
 	
 	orin@eis200r:~/project/video_analysis/build$ timedatectl timesync-status
           Server: 172.20.31.9 (172.20.31.9)        
    Poll interval: 17min 4s (min: 32s; max 34min 8s)
             Leap: normal                           
          Version: 4                                
          Stratum: 2                                
        Reference: D21C8204                         
        Precision: 1us (-22)                        
    Root distance: 16.288ms (max: 5s)               
           Offset: -673us                           
            Delay: 619us                            
           Jitter: 3.841ms                          
     Packet count: 6                                
        Frequency: +27.134ppm                       
    orin@eis200r:~/project/video_analysis/build$ timedatectl status
                   Local time: Fri 2026-03-20 10:50:29 CST
               Universal time: Fri 2026-03-20 02:50:29 UTC
                     RTC time: Fri 2026-03-20 02:50:44    
                    Time zone: Asia/Shanghai (CST, +0800) 
    System clock synchronized: yes                        
                  NTP service: active                     
              RTC in local TZ: no
    注意：出现以上信息，代表同步成功
```