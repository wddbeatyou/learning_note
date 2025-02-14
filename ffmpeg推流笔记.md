## ffmpeg的推流原理

### 一、简介

```
一、subprocess模块
    功能：subprocess是Python的一个标准库，用于生成新的进程，连接它们的输入/输出/错误管道，并获得它们的返回码。它允许你在Python脚本中执行系统命令，包括FFmpeg命令。
    安装：由于subprocess是Python的标准库，因此无需额外安装。
    灵活性：使用subprocess，你可以执行任何FFmpeg命令，只需将其作为字符串传递给subprocess.run或类似函数。这使得它非常灵活，因为你可以完全控制FFmpeg的行为。
    复杂性：然而，使用subprocess需要你对FFmpeg命令有一定的了解，并且需要手动构建命令字符串。这可能会增加代码的复杂性和出错的可能性。
```

```
二、ffmpeg-python库
    功能：ffmpeg-python是一个用于在Python中轻松调用FFmpeg的库。它提供了一个高级API，使你可以以更Pythonic的方式使用FFmpeg。
    安装：pip install ffmpeg-python
    易用性：与subprocess相比，ffmpeg-python提供了更简洁、更易于理解的API。你可以使用链式调用来构建FFmpeg命令，而无需担心命令字符串的格式或转义字符。
    功能限制：虽然ffmpeg-python提供了许多常用功能，但它可能无法覆盖FFmpeg的所有功能。如果你需要使用FFmpeg的某些高级或不太常用的功能，你可能仍然需要使用subprocess或直接调用FFmpeg命令。
```

```
总结:
    如果你对FFmpeg命令非常熟悉，并且希望保持最大的灵活性，那么subprocess可能是一个更好的选择。
    如果你希望以更简洁、更Pythonic的方式使用FFmpeg，并且不需要访问其所有功能，那么ffmpeg-python可能更适合你。
```

### 二、ffmpeg-python与FFmpeg

```
	ffmpeg-python是一个Python库，它提供了对FFmpeg命令行工具的访问。这个库的主要作用是简化FFmpeg命令的生成和执行，使Python开发者能够更容易地在脚本中调用FFmpeg的功能。ffmpeg-python并不包含FFmpeg的实际处理逻辑或算法，它只是生成并传递命令给FFmpeg执行。
```

```
	FFmpeg是一个开源的多媒体框架，用于处理音频、视频和其他多媒体文件和流。它包含了丰富的编解码器、过滤器、复用器等组件，
能够执行视频转换、音频处理、流媒体传输等多种任务。在拉流和推流的场景中，FFmpeg负责实际的音视频数据处理工作。
```

```
ffmpeg-python与ffmpeg的关系：
        ffmpeg-python库依赖于系统上已经安装的FFmpeg软件。当在Python脚本中调用ffmpeg-python的函数时，这些函数会生成相应的FFmpeg命令行参数，并将其传递给系统上的FFmpeg可执行文件进行处理。因此，如果没有安装FFmpeg，ffmpeg-python将无法执行任何音视频处理任务。
```

### 三、案例

```
import cv2
import subprocess

# RTSP 摄像头的 URL
rtsp_url = "rtsp://admin:HuaWei123@172.20.31.91:554/LiveMedia/ch1/Media1/tracklD=1"

# 推流地址 (RTMP 或 RTSP)
rtsp_url = "rtsp://172.20.31.57:10020/live/stream"

# 打开远程摄像头
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# 获取视频的宽度、高度和帧率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 设置 FFmpeg 推流命令
ffmpeg_command = [
    'ffmpeg',
    '-y',  # 覆盖输出文件
    '-f', 'rawvideo',  # 输入格式为原始视频
    '-pix_fmt', 'bgr24',  # 像素格式为 BGR（OpenCV 默认格式）
    '-s', f'{width}x{height}',  # 视频分辨率
    '-r', "25",  # 帧率
    '-i', '-',  # 从标准输入读取数据
    '-c:v', 'libx264',  # 视频编码器
    '-pix_fmt', 'yuv420p',  # 输出像素格式
    '-preset', 'ultrafast',  # 编码速度
    '-f', 'flv',  # 输出格式为 FLV（RTMP 推流）
    rtsp_url
]

# 启动 FFmpeg 进程
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame.")
            break
        # frame = cv2.resize(frame,(540,360))
        # 在这里对帧进行处理（例如：灰度化、目标检测等）
        # processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 示例：将帧转换为灰度图
        # processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)  # 转换回 BGR 格式
        # 显示处理后的帧（可选）
        cv2.imshow('Processed Frame', frame)
        # 将处理后的帧写入 FFmpeg 的标准输入
        ffmpeg_process.stdin.write(frame.tobytes())
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 退出
            break
except KeyboardInterrupt:
    print("Streaming stopped by user.")
finally:
    # 释放资源
    cap.release()
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
    cv2.destroyAllWindows()
```

```
注意：
	ffmpeg_command中有个参数“flv”指的是rtmp流，如果使用rtsp推流，需修改成“rtsp”;
```