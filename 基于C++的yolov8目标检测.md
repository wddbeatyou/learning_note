## 基于C++的目标检测流程

### 一、搭建环境

#### 1.1 python环境

```
命令：
	pip install -r requirements.txt
requirements.txt里面的内容：
    numpy<=1.23.5
    onnx
    onnxsim
    torch
    torchvision
    ultralytics
```

#### 1.2 cuda环境

```
略
```

### 二、训练模型

```
from ultralytics import YOLO
import torch

# 检查 GPU 是否可用
if torch.cuda.is_available():
    device = torch.device('cuda')
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device('cpu')
    print("Using CPU")
# 加载模型并移至 GPU
model = YOLO('yolov8n.pt').to(device)
if __name__ == '__main__':
    model.train(
        data="/home/supcon/alg/wdd/tools_test/config/myconfig.yaml",
        batch=4,       # 根据显存调整（RTX 4060 可尝试 4-8）
        workers=2,      # 根据 CPU 核心数调整
        epochs=300,
        device=device,  # 自动选择 GPU/CPU
        half=True,      # 启用 FP16 加速（RTX 40 系支持）
        patience=50,    # 早停防止过拟合
        optimizer="auto",  # 推荐使用 AdamW
    )
```

### 三、转化模型

#### 3.1 pt 模型 转化 onnx 模型

```
项目位置：
	D:\company_project\algorithm_mode\yolov8\pt_to_onnx
CPU环境：
	python export-det.py --weights "./best.pt" --iou-thres 0.65 --conf-thres 0.25 --topk 100 --opset 11 --sim --input-shape 1 3 640 640
GPU环境：
	python export-det.py --weights "./best.pt" --iou-thres 0.65 --conf-thres 0.25 --topk 100 --opset 11 --sim --input-shape 1 3 640 640 --device cuda:0
```

#### 3.2 onnx 模型 转换 engine 模型

```
GPU环境：
	/usr/src/tensorrt/bin/trtexec --onnx=/home/orin/tool_recogine/tool.onnx --saveEngine=/home/orin/tool_recogine/tool.engine --fp16
```

### 四、推理

```
项目：https://github.com/triple-Mu/YOLOv8-TensorRT#

```





