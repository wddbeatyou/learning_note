# Deepstream-jetson_orin_nano插件中属性讲解

## 1.nvstreammux

### 1.1 插件介绍

```
nvstreammux是一个流复用器，主要功能是：
    1) 多路合一：将多个输入源（如RTSP流、视频文件、摄像头）汇聚成一个批量数据块。
    2) 批量处理：为下游的 AI 模型（如 nvinfer）准备批量数据，这是实现高性能推理的关键。
    3) 尺寸统一：将所有输入帧缩放/填充到统一的输出分辨率。
    4) 时间戳管理：处理来自不同源的帧的时间戳，确保下游同步。
```

### 1.2 命令查看

```
命令：
	gst-inspect-1.0 nvstreammux
	
输出：
Factory Details:
  Rank                     primary (256)
  Long-name                Stream multiplexer
  Klass                    Generic
  Description              N-to-1 pipe stream multiplexing
  Author                   NVIDIA Corporation. Post on Deepstream for Tesla forum for any queries @ https://devtalk.nvidia.com/default/board/209/

Plugin Details:
  Name                     nvdsgst_multistream
  Description              NVIDIA Multistream mux/demux plugin
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/deepstream/libnvdsgst_multistream.so
  Version                  6.3.0
  License                  Proprietary
  Source module            nvmultistream
  Binary package           NVIDIA Multistream Plugins
  Origin URL               http://nvidia.com/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstNvStreamMux

Pad Templates:
  SINK template: 'sink_%u'
    Availability: On request
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA, (string)I420 }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
  
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA, (string)I420 }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  async-process       : Boolean property to enable/disable asynchronous processing of input frames for performance.
                        flags: readable, writable
                        Boolean. Default: true
  attach-sys-ts       : If set to TRUE, system timestamp will be attached as ntp timestamp.
                        If set to FALSE, ntp timestamp from rtspsrc, if available, will be attached.
                        flags: readable, writable
                        Boolean. Default: true
  batch-size          : Maximum number of buffers in a batch
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 1024 Default: 0 
  batched-push-timeout: Timeout in microseconds to wait after the first buffer is available
                        to push the batch even if the complete batch is not formed.
                        Set to -1 to wait infinitely
                        flags: readable, writable
                        Integer. Range: -1 - 2147483647 Default: -1 
  buffer-pool-size    : Maximum number of buffers from muxer's output pool
                        flags: readable, writable
                        Unsigned Integer. Range: 4 - 1024 Default: 4 
  compute-hw          : Compute Scaling HW
                        flags: readable, writable, controllable
                        Enum "GstNvComputeHWType" Default: 0, "Default"
                           (0): Default          - Default, GPU for Tesla, VIC for Jetson
                           (1): GPU              - GPU
                           (2): VIC              - VIC
  drop-pipeline-eos   : Boolean property so that EOS is not propagated downstream when all the sink pads are at EOS. (Experimental)
                        flags: readable, writable
                        Boolean. Default: false
  enable-padding      : Maintain input aspect ratio when scaling by padding with black bands.
                        flags: readable, writable
                        Boolean. Default: false
  frame-duration      : Duration of input frames in milliseconds for use in NTP timestamp correction based on frame rate.
                        If set to 0, frame duration is inferred automatically from PTS values.
                        If set to -1, disables frame rate based NTP timestamp correction. (default)
                        flags: readable, writable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 18446744073709 
  frame-num-reset-on-eos: Reset frame numbers to 0 for a source from which EOS is received (For debugging purpose only)
                        flags: readable, writable
                        Boolean. Default: false
  frame-num-reset-on-stream-reset: Reset frame numbers to 0 for a source which needs to be reset. (For debugging purpose only)
Needs to be paired with tracking-id-reset-mode=1 in the tracker config.
                        flags: readable, writable
                        Boolean. Default: false
  gpu-id              : Set GPU Device ID
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  height              : Height of each frame in output batched buffer. This property MUST be set.
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  interpolation-method: Set interpolation methods
                        flags: readable, writable, controllable
                        Enum "GstNvInterpolationMethod" Default: 1, "Bilinear"
                           (0): Nearest          - Nearest
                           (1): Bilinear         - Bilinear
                           (2): Algo-1           - GPU - Cubic, VIC - 5 Tap
                           (3): Algo-2           - GPU - Super, VIC - 10 Tap
                           (4): Algo-3           - GPU - LanzoS, VIC - Smart
                           (5): Algo-4           - GPU - Ignored, VIC - Nicest
                           (6): Default          - GPU - Nearest, VIC - Nearest
  live-source         : Boolean property to inform muxer that sources are live.
                        flags: readable, writable
                        Boolean. Default: false
  max-latency         : Additional latency in live mode to allow upstream to take longer to produce buffers for the current position
 (in nanoseconds)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "nvstreammux0"
  num-surfaces-per-frame: Max number of surfaces per frame
                        flags: readable, writable
                        Unsigned Integer. Range: 1 - 4 Default: 1 
  nvbuf-memory-type   : Type of NvBufSurface Memory to be allocated for output buffers
                        flags: readable, writable, changeable only in NULL or READY state
                        Enum "GstNvBufMemoryType" Default: 0, "nvbuf-mem-default"
                           (0): nvbuf-mem-default - Default memory allocated, specific to particular platform
                           (1): nvbuf-mem-cuda-pinned - Allocate Pinned/Host cuda memory
                           (2): nvbuf-mem-cuda-device - Allocate Device cuda memory
                           (3): nvbuf-mem-cuda-unified - Allocate Unified cuda memory
                           (4): nvbuf-mem-surface-array - Allocate Surface Array memory, applicable for Jetson
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  sync-inputs         : Boolean property to force sychronization of input frames.
                        flags: readable, writable
                        Boolean. Default: false
  width               : Width of each frame in output batched buffer. This property MUST be set.
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0
```

### 1.3 参数讲解

#### 1.3.1 **`async-process`**

```
含义：
	控制是否启用输入帧的异步处理，以提升性能。
默认值：
	true（启用）。
不同值的效果：
    true：帧处理在后台异步进行，不阻塞上游插件（如摄像头源），可提高 pipeline 吞吐量（尤其多路流场景）。
    false：帧处理同步执行，上游需等待当前帧处理完成才会推送新帧，可能导致延迟增加，但可保证帧处理的严格顺序。
优缺点：
    启用（true）：提升性能，适合高并发场景；但可能引入帧顺序轻微错乱（通常不影响实际使用）。
    禁用（false）：保证顺序性，适合对帧顺序敏感的场景；但性能较低。
```

#### 1.3.2 **`attach-sys-ts`**

```
含义：
	控制附加到帧的时间戳类型（系统时间戳 vs RTSP 源自带的 NTP 时间戳）。
默认值：
	true（使用系统时间戳）。
不同值的效果：
    true：强制使用系统当前时间作为帧的 NTP 时间戳，忽略上游（如 rtspsrc）自带的时间戳。
    false：优先使用上游（如 RTSP 摄像头）提供的 NTP 时间戳（若存在），否则 fallback 到系统时间戳。
优缺点：
    true：时间戳统一（基于本地系统），适合多路流时间同步；但可能与源设备实际时间偏差。
    false：保留源设备原始时间戳，适合需要精确溯源的场景；但多路流时间可能不同步（如不同摄像头时区差异）。
```

```
系统时间：
    是什么：指的是运行 DeepStream 流水线的 本地机器（服务器/Jetson设备） 的当前时钟时间。
    来源：由本地机器的操作系统时钟提供。这个时钟可能通过网络时间协议（NTP）与时间服务器同步，也可能只是设备自身维护的一个本地时间。
    在DeepStream中的行为：当 attach-sys-ts=true 时，nvstreammux 会在它处理每一帧的 那个瞬间，读取本地系统时钟，并将这个时间值作为该帧的 NTP 时间戳附加到帧上。

源时间：
    是什么：指的是 生成视频流的源头设备（如网络摄像头、RTSP 摄像头、视频文件等）在捕获该帧时所记录的时间。
    来源：对于RTSP摄像头：一个专业的IP摄像头通常有自己的系统时钟。当它捕获一帧图像时，它会将自己的当前时间作为一个 RTP时间戳 或 NTP时间戳（如果服务器支持）嵌入到视频流中。rtspsrc 组件在接收流时会解析这个时间戳。对于视频文件：文件中的每一帧通常都有一个 呈现时间戳（PTS），这个时间戳是相对于文件开始的相对时间。
    在DeepStream中的行为：当 attach-sys-ts=false 时，nvstreammux 会尝试使用上游（如 rtspsrc）提供的这个“原始”时间戳。如果上游没有提供有效的时间戳，它才会回退到使用系统时间。
```

```
 为什么会出现不一致？（不一致的根源），系统时间和源时间不一致是常态，而不是例外。主要原因如下：

a) 时钟不同步
    这是最根本的原因。源设备（摄像头） 和 接收设备（你的DeepStream服务器） 是两个独立的物理设备，它们各有各的时钟晶振。
    时钟漂移：任何物理时钟都存在微小的误差，有的走得快一点，有的走得慢一点。长时间运行后，两个设备的时间差会逐渐累积，从几毫秒到几秒甚至几分钟。
    未校准：很多消费级或安防摄像头没有配置NTP同步，它们使用出厂时设置的默认时间，或者依赖内部不精确的时钟。如果你的服务器通过NTP校准了，而摄像头没有，
    	   那么它们的时间基准从一开始就是不同的。

b) 网络传输延迟
    即使两个设备的时钟完全同步，帧从源设备传输到DeepStream服务器也需要时间。
    过程：摄像头捕获帧 (T_capture) -> 编码打包 -> 网络传输 -> 服务器接收解码 (T_receive)，T_receive 永远晚于 T_capture。这个延迟包括： 固定延迟：
         编码/解码时间。可变延迟（抖动）：网络拥堵、路由变化等导致的延迟波动。当你使用 系统时间（T_system） 时，你记录的是 T_receive 时刻，
         而不是 T_capture 时刻。T_system 和 T_capture 之间始终存在一个正的、且不断变化的延迟差。

c) 处理流水线延迟
    在DeepStream流水线内部，帧需要经过多个组件（解复用、解码、muxer、推理、渲染等），每个组件都会占用一些处理时间。系统时间戳是在 
    nvstreammux 处理时打上的，这已经比 rtspsrc 接收到数据包的时间点更晚了。
```

#### 1.3.3 **`batch-size`**

```
含义：
	批量帧中最多包含的缓冲区（帧）数量，即最大支持的并发流数量。
默认值：
	0（需手动设置，否则 pipeline 无法启动）。
范围：
	0~1024。
不同值的效果：
    需设置为大于等于实际接入的流数量（如 4 路摄像头需 batch-size≥4），否则部分流无法处理。
    若设置过大（如 1024 但实际仅 4 路流），会浪费 GPU 内存（批量帧缓冲区按最大容量分配）。
优缺点：
    过小：无法支持足够的流数量，导致错误。
    过大：占用更多内存，降低资源利用率。
建议：设置为实际流数量（或略大，预留扩展空间）。
```

#### 1.3.4 **`batched-push-timeout`**

```
含义：
	组装批量帧的超时时间（微秒）。当收到第一帧后，若超时仍未收集满 batch-size 帧，则推送已有的帧。
默认值：-1（无限等待，直到收集满 batch-size 帧）。
范围：-1~2147483647（-1 表示无限等待）。
不同值的效果：
    -1：必须收集满 batch-size 帧才推送，适合流帧率稳定的场景（如 4 路 30fps 摄像头），GPU 处理效率最高，但某路流卡顿会导致整体延迟飙升。
    0：收到任意数量的帧立即推送，无延迟，适合实时性优先场景（如监控），但 GPU 处理零散帧效率低。
    10000（10 毫秒）：平衡延迟与效率，多数场景下推荐，避免过长等待。
优缺点：
    超时过长：延迟增加，可能导致画面卡顿。
    超时过短：批量帧不完整，GPU 效率低。
```

#### 1.3.5 **`buffer-pool-size`**

```
含义：
	nvstreammux 输出缓冲区池的最大容量（预分配的批量帧缓冲区数量）。
默认值：4。
范围：4~1024。
不同值的效果：
    过小（如 4）：缓冲区不足时，上游插件需等待缓冲区释放，可能导致帧率下降。
    过大（如 1024）：占用更多 GPU 内存，但可应对突发流量（如瞬间高帧率）。
建议：根据流数量和帧率调整，多路高帧率场景可适当增大（如 8~16）。
```

#### 1.3.6 **`compute-hw`**

```
含义：
	指定用于缩放（Scaling）的硬件（GPU 或 VIC）。
默认值：
	0（Default，Tesla 用 GPU，Jetson 用 VIC）。
枚举值：
    0（Default）：自动选择（推荐，适配硬件）。
    1（GPU）：强制用 GPU 缩放，适合需要高精度缩放的场景（如复杂算法）。
    2（VIC）：强制用 VIC（Jetson 专用硬件加速器），适合低功耗、高吞吐量的简单缩放。
优缺点：
    GPU：精度高，支持复杂算法；但功耗高，占用 GPU 算力。
    VIC（Jetson）：低功耗，效率高；但功能有限，仅支持基础缩放。
```

#### 1.3.7 **`drop-pipeline-eos`**

```
含义：
	控制是否在所有输入流结束（EOS）时向下游传播 EOS 信号（实验性属性）。
默认值：false（传播 EOS）。
不同值的效果：
    true：忽略 EOS，pipeline 继续运行（即使所有流已结束），适合需要手动控制 pipeline 生命周期的场景。
    false：正常传播 EOS，触发下游插件结束处理（如推理引擎停止）。
注意：实验性属性，可能不稳定，谨慎使用。
```

#### 1.3.8 **`enable-padding`**

```
含义：
	缩放时是否保持输入帧的宽高比，不足部分用黑边填充。
默认值：false（不填充，直接拉伸至输出尺寸）。
不同值的效果：
    true：画面不变形（如 16:9 源缩放至 4:3 输出时，上下加黑边），适合对画面比例敏感的场景（如人脸识别）。
    false：强制拉伸至输出尺寸（宽高比可能改变），适合对画面内容完整性要求高于比例的场景（如全景监控）。
```

#### 1.3.9 **`frame-duration`**

```
含义：
	基于帧率的 NTP 时间戳校正参数（毫秒），用于修正时间戳偏差。
默认值：18446744073709551615（即 -1，禁用校正）。
不同值的效果：
    0：自动从 PTS（Presentation Time Stamp）推断帧间隔（适合帧率稳定的流）。
    -1：禁用校正，直接使用原始时间戳（适合帧率不稳定的流）。
    其他值（如 33 对应～30fps）：强制指定帧间隔，用于时间戳异常的流校正。
建议：默认禁用（-1），若时间戳混乱可尝试 0 或手动设置。
```

#### 1.3.10 **`frame-num-reset-on-eos / frame-num-reset-on-stream-reset`**

```
含义：调试用属性，控制流结束（EOS）或重置时，是否将帧序号重置为 0。
默认值：均为 false（不重置）。
效果：仅用于调试（如跟踪帧序号变化），生产环境建议保持默认（避免序号跳变影响下游处理）。
```

#### 1.3.11 **`gpu-id`**

```
含义：指定使用的 GPU 设备 ID（多 GPU 系统中生效）。
默认值：0（默认使用第一块 GPU）。
范围：0~4294967295。
效果：在多 GPU 服务器上，可指定特定 GPU 处理（如 gpu-id=1 表示第二块 GPU），用于负载均衡。
```

#### 1.3.12 **`width` 和 `height`**

```
含义：输出批量帧中每路流的帧高 / 宽（必须设置，否则 pipeline 无法启动）。
默认值：0（需手动设置）。
效果：所有输入流会被缩放至该尺寸后打包成批量帧，需与输入流的宽高比适配（或配合 enable-padding 保持比例）。
注意：设置过大（如 4K）会增加 GPU 内存占用和处理耗时；过小则可能丢失细节（如影响推理精度）。
```

#### 1.3.13 **`interpolation-method` **

```
含义：缩放时使用的插值算法，影响画面质量。
默认值：1（Bilinear，双线性插值）。
枚举值：
    0（Nearest）：最近邻插值，速度快但画质差（有锯齿）。
    1（Bilinear）：双线性插值，平衡速度与画质（推荐默认）。
    2~5：更高质量算法（如 Cubic、LanzoS），画质更好但计算耗时增加。
建议：普通场景用 Bilinear；对画质要求高（如高清视频分析）用 Algo-2 或 Algo-3。
```

#### 1.3.14 **`live-source` **

```
含义：告知 nvstreammux 输入源是实时流（如摄像头、RTSP）还是文件流。
默认值：false（非实时）。
不同值的效果：
    true：启用实时模式，优化延迟（如忽略过时帧），适合摄像头 / RTSP 等实时源。
    false：按文件流处理（严格按时间戳顺序），适合本地视频文件。
```

#### 1.3.15 **`max-latency` **

```
含义：实时模式下允许的最大额外延迟（纳秒），用于容忍上游源的临时卡顿。
默认值：0（无额外延迟）。
效果：设置过大（如 1e6 纳秒 = 1 毫秒）可减少因上游短暂卡顿导致的丢帧，但会增加整体延迟；设置过小则可能频繁丢帧。
```

#### 1.3.16 **`name` **

```
含义：插件实例的名称（用于 pipeline 中标识该插件）。
默认值："nvstreammux0"。
效果：可自定义名称（如 "muxer1"），方便在调试或多实例场景中区分。
```

#### 1.3.17 **`num-surfaces-per-frame` **

```
含义：每帧包含的表面（Surface）数量（用于多平面格式，如 YUV420 有 Y/U/V 三个平面）。
默认值：1（单平面，适合多数场景）。
范围：1~4。
效果：仅在处理特殊多平面格式时需要调整（如某些高动态范围视频），默认值通常适用。
```

#### 1.3.18 **`nvbuf-memory-type`**

```
含义：指定输出缓冲区（NvBufSurface）的内存类型。
默认值：0（nvbuf-mem-default，自动选择，推荐）。
枚举值：
    0（default）：按平台自动选择（如 Jetson 用共享内存，Tesla 用 CUDA 内存）。
    1（cuda-pinned）：主机端 pinned 内存（CPU/GPU 均可访问，适合数据频繁传输）。
    2（cuda-device）：GPU 设备内存（仅 GPU 访问，速度快，适合纯 GPU 处理）。
    3（cuda-unified）：统一内存（CPU/GPU 自动映射，适合异构计算）。
    4（surface-array）：Jetson 专用表面数组内存（适合硬件加速器如 VIC）。
建议：默认值即可，特殊场景（如 CPU 需频繁访问帧数据）可手动选择。
```

#### 1.3.19 **`parent`**

```
含义：指定插件的父对象（GstObject），用于 GST 框架内部的对象管理。
效果：通常无需手动设置，由框架自动处理。
```

#### 1.3.20 **`sync-inputs`**

```
含义：强制同步所有输入流的帧（按时间戳对齐）。
默认值：false（不同步）。
不同值的效果：
    true：所有流的帧按时间戳对齐后再打包，适合多路流时间同步场景（如多摄像头拼接），但可能因某路流延迟导致整体卡顿。
    false：按接收顺序打包，延迟低但多路流时间可能不同步。
```

### 1.4 总结

```
nvstreammux 的属性需根据流数量、实时性要求、硬件类型（Jetson/Tesla）、画质需求等场景灵活配置：
    核心必设属性：batch-size、width、height。
    实时性优先：batched-push-timeout=0、live-source=true、async-process=true。
    效率优先：batched-push-timeout=10000、sync-inputs=true（若需同步）。
    资源优化：buffer-pool-size 按需调整，nvbuf-memory-type 保持默认。
```

## 2.nvinfer

### 2.1 插件介绍

```
nvinfer是 DeepStream 中用于集成 TensorRT 进行模型推理的核心插件，负责加载深度学习模型、执行推理并将结果（如目标检测框、分类结果）附加到元数据中。
```

### 2.2 命令查看

```
命令：
	gst-inspect-1.0 nvinfer
输出：
Factory Details:
  Rank                     primary (256)
  Long-name                NvInfer plugin
  Klass                    NvInfer Plugin
  Description              Nvidia DeepStreamSDK TensorRT plugin
  Author                   NVIDIA Corporation. Deepstream for Tesla forum: https://devtalk.nvidia.com/default/board/209

Plugin Details:
  Name                     nvdsgst_infer
  Description              NVIDIA DeepStreamSDK TensorRT plugin
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/deepstream/libnvdsgst_infer.so
  Version                  6.3.0
  License                  Proprietary
  Source module            nvinfer
  Binary package           NVIDIA DeepStreamSDK TensorRT plugin
  Origin URL               http://nvidia.com/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseTransform
                         +----GstNvInfer

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
  
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  batch-size          : Maximum batch size for inference
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 1 - 1024 Default: 1 
  clip-object-outside-roi: Clip the object bounding-box which lies outside the roi specified by nvdspreprosess plugin
                        flags: readable, writable, changeable only in NULL or READY state
                        Boolean. Default: true
  config-file-path    : Path to the configuration file for this instance of nvinfer
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                        String. Default: ""
  crop-objects-to-roi-boundary: Clip the object bounding-box which lies outside the roi boundary
                        flags: readable, writable, changeable only in NULL or READY state
                        Boolean. Default: false
  filter-out-class-ids: Ignore metadata for objects of specified class ids
                        Use string with values of class ids in ClassID (int) to set the property.
                         e.g. 0;2;3
                        flags: readable, writable, changeable only in NULL or READY state
                        String. Default: ""
  gpu-id              : Set GPU Device ID
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  infer-on-class-ids  : Operate on objects with specified class ids
                        Use string with values of class ids in ClassID (int) to set the property.
                         e.g. 0:2:3
                        flags: readable, writable, changeable only in NULL or READY state
                        String. Default: ""
  infer-on-gie-id     : Infer on metadata generated by GIE with this unique ID.
                        Set to -1 to infer on all metadata.
                        flags: readable, writable, changeable only in NULL or READY state
                        Integer. Range: -1 - 2147483647 Default: -1 
  input-tensor-meta   : Use preprocessed input tensors attached as metadata instead of preprocessing inside the plugin
                        flags: readable, writable, changeable only in NULL or READY state
                        Boolean. Default: false
  interval            : Specifies number of consecutive batches to be skipped for inference
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 2147483647 Default: 0 
  model-engine-file   : Absolute path to the pre-generated serialized engine file for the model
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                        String. Default: ""
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "nvinfer0"
  output-instance-mask: Instance mask expected in network output and attach it to metadata
                        flags: readable, writable, changeable only in NULL or READY state
                        Boolean. Default: false
  output-tensor-meta  : Attach inference tensor outputs as buffer metadata
                        flags: readable, writable, changeable only in NULL or READY state
                        Boolean. Default: false
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  process-mode        : Infer processing mode
                        flags: readable, writable, changeable only in NULL or READY state
                        Enum "GstNvInferProcessModeType" Default: 1, "primary"
                           (1): primary          - Primary (Full Frame)
                           (2): secondary        - Secondary (Objects)
  qos                 : Handle Quality-of-Service events
                        flags: readable, writable
                        Boolean. Default: false
  raw-output-file-write: Write raw inference output to file
                        flags: readable, writable, changeable only in NULL or READY state
                        Boolean. Default: false
  raw-output-generated-callback: Pointer to the raw output generated callback funtion
                        (type: gst_nvinfer_raw_output_generated_callback in 'gstnvdsinfer.h')
                        flags: readable, writable, changeable only in NULL or READY state
                        Pointer.
  raw-output-generated-userdata: Pointer to the userdata to be supplied with raw output generated callback
                        flags: readable, writable, changeable only in NULL or READY state
                        Pointer.
  unique-id           : Unique ID for the element. Can be used to identify output of the element
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 15 

Element Signals:
  "model-updated" :  void user_function (GstElement* object,
                                         gint arg0,
                                         gchararray arg1,
                                         gpointer user_data);
```

### 2.3 参数讲解

#### 2.3.1 **batch-size**

```
含义：推理时使用的最大批量大小（一次推理处理的帧 / 目标数量）。
默认值：1
范围：1~1024
限制：仅在插件处于 NULL 或 READY 状态时可修改。
不同值的效果：
    增大值（如 4）：提高 GPU 利用率（批量推理效率更高），适合多路流或高帧率场景，但需更多 GPU 显存。
    减小值（如 1）：降低显存占用，适合显存有限的设备（如 Jetson Orin Nano），但推理效率较低。
注意：需与上游 nvstreammux 的 batch-size 匹配（通常设为相同值），否则可能导致性能瓶颈。
```

#### 2.3.2 **clip-object-outside-roi**

```
含义：是否裁剪超出 nvdspreprocess 插件指定 ROI（感兴趣区域）的目标边界框。
默认值：true（裁剪）
限制：仅在 NULL 或 READY 状态时可修改。
效果：
    true：超出 ROI 的目标部分会被裁剪（边界框仅保留 ROI 内区域），适合只关注特定区域的场景（如监控画面中的特定区域）。
    false：保留完整边界框（即使部分在 ROI 外），适合需要完整目标信息的场景。
```

#### 2.3.3 **config-file-path**

```
含义：nvinfer 实例的配置文件路径（必填，用于定义模型路径、输入输出尺寸、类别等参数）。
默认值：空字符串（需手动设置）
可修改时机：在 NULL、READY、PAUSED、PLAYING 状态均可修改（动态更新配置）。
作用：
	配置文件（如 dstest_pgie_config.txt）是 nvinfer 的核心参数来源，包含模型路径（model-path）、输入尺寸（input-dims）、
	类别名称（class-names）等关键信息，不设置则无法加载模型。
```

#### 2.3.4 **crop-objects-to-roi-boundary**

```
含义：是否将目标边界框裁剪至 ROI 边界（与 clip-object-outside-roi 类似，但更严格）。
默认值：false（不裁剪）
限制：仅在 NULL 或 READY 状态时可修改。
与 clip-object-outside-roi 的区别：
	若 clip-object-outside-roi 为 true，仅裁剪边界框坐标；crop-objects-to-roi-boundary 为 true 时，会直接裁剪目标像素（更彻底）。
适用场景：需要严格限制推理区域内像素的场景（如隐私保护）。
```

#### 2.3.5 **filter-out-class-ids**

```
含义：忽略指定类别 ID 的目标元数据（过滤掉不需要的类别）。
默认值：空字符串（不过滤）
格式：用分号分隔的类别 ID 字符串（如 "0;2;3" 表示过滤 ID 为 0、2、3 的类别）。
限制：仅在 NULL 或 READY 状态时可修改。
效果：下游插件（如跟踪、显示）不会处理被过滤的类别，适合只关注特定类别的场景（如只检测 “人”，过滤 “车”）。
```

#### 2.3.6 **gpu-id**

```
含义：指定用于推理的 GPU 设备 ID（多 GPU 系统中生效）。
默认值：0（默认使用第一块 GPU）
范围：0~4294967295
限制：仅在 NULL 或 READY 状态时可修改。
效果：在多 GPU 服务器上，可指定特定 GPU 执行推理（如 gpu-id=1 用于负载均衡），避免单 GPU 过载。
```

#### 2.3.7 **infer-on-class-ids**

```
含义：仅对指定类别 ID 的目标执行推理（常用于二级推理）。
默认值：空字符串（对所有目标推理）
格式：用冒号分隔的类别 ID 字符串（如 "0:2:3" 表示仅对 ID 为 0、2、3 的目标推理）。
限制：仅在 NULL 或 READY 状态时可修改。
适用场景：二级推理（如先通过一级模型检测 “车”，再通过二级模型对 “车” 进行细分（轿车 / 卡车）），提高效率。
```

#### 2.3.8 **infer-on-gie-id**

```
含义：仅对指定 GIE（GstInferElement）ID 生成的元数据执行推理。
默认值：-1（对所有 GIE 元数据推理）
范围：-1~2147483647
限制：仅在 NULL 或 READY 状态时可修改。
效果：
	用于多阶段推理流水线（如多个 nvinfer 串联），指定当前插件只处理某个上游nvinfer输出的结果（如infer-on-gie-id=1表示只处理ID为1的nvinfer输出）。
```

#### 2.3.9  **input-tensor-meta**

```
含义：是否使用预处理后的输入张量元数据（而非插件内部预处理）。
默认值：false（使用插件内部预处理）
限制：仅在 NULL 或 READY 状态时可修改。
效果：
    true：依赖上游插件（如 nvdspreprocess）生成的预处理张量，适合自定义预处理逻辑的场景。
    false：由 nvinfer 内部完成预处理（如缩放、归一化），简化 pipeline 配置。
```

#### 2.3.10 **interval**

```
含义：推理间隔（每 interval+1 帧执行一次推理，跳过中间帧）。
默认值：0（每帧都推理）
范围：0~2147483647
限制：仅在 NULL 或 READY 状态时可修改。
效果：
    增大值（如 1）：每 2 帧推理一次，降低 GPU 负载，适合静态场景（如监控画面变化慢）。
    减小值（如 0）：每帧推理，保证实时性，适合动态场景（如高速移动目标）。
```

#### 2.3.11 **model-engine-file**

```
含义：预生成的 TensorRT 引擎文件（.engine）的绝对路径。
默认值：空字符串（需手动设置或由插件自动生成）
可修改时机：在 NULL、READY、PAUSED、PLAYING 状态均可修改。
作用：
    TensorRT 引擎是模型优化后的二进制文件，加载速度远快于原始模型（如 .onnx、.pb）。若指定路径，插件直接加载引擎；
    否则自动从原始模型生成（首次运行较慢）。
```

#### 2.3.12 **name**

```
含义：插件实例的名称（用于 pipeline 中标识该插件）。
默认值："nvinfer0"
效果：可自定义名称（如 "primary-gie"、"secondary-gie"），方便调试和多实例区分（如流水线中多个 nvinfer 插件）。
```

#### 2.3.13 **output-instance-mask**

```
含义：是否将网络输出的实例掩码（Instance Mask，如语义分割中的像素级掩码）附加到元数据。
默认值：false（不附加）
限制：仅在 NULL 或 READY 状态时可修改。
适用场景：语义分割或实例分割模型，需要获取目标像素级掩码时设置为 true（如分割 “行人” 的每一个像素）。
```

#### 2.3.14 **output-tensor-meta**

```
含义：是否将推理的原始张量输出（如模型最后一层的特征向量）附加到缓冲区元数据。
默认值：false（不附加）
限制：仅在 NULL 或 READY 状态时可修改。
适用场景：需要自定义后处理（如基于特征向量的跟踪、聚类）时设置为 true，下游插件可直接读取原始张量。
```

#### 2.3.15 **parent**

```
含义：指定插件的父对象（GstObject），用于 GStreamer 框架内部的对象管理。
效果：通常无需手动设置，由框架自动处理。
```

#### 2.3.16 **process-mode**

```
含义：推理处理模式（一级推理 / 二级推理）。
默认值：1（primary，一级推理）
枚举值：
    1（primary）：全帧推理（对完整图像执行推理，如目标检测）。
    2（secondary）：目标级推理（仅对上游检测到的目标区域执行推理，如目标分类、属性识别）。
限制：仅在 NULL 或 READY 状态时可修改。
```

#### 2.3.17 **qos**

```
含义：是否处理服务质量（QoS）事件（如丢帧、延迟）。
默认值：false（不处理）
效果：true 时插件会响应上游的 QoS 事件（如主动丢帧以降低延迟），适合对实时性要求高的场景，但可能影响推理完整性。
```

#### 2.3.18 **raw-output-file-write**

```
含义：是否将原始推理输出写入文件（调试用）。
默认值：false（不写入）
限制：仅在 NULL 或 READY 状态时可修改。
效果：true 时会将模型输出的原始张量数据（如边界框坐标、置信度）写入文件，用于调试模型输出是否正确。
```

#### 2.3.19 **raw-output-generated-callback / raw-output-generated-userdata**

```
含义：原始输出生成时的回调函数及用户数据（自定义后处理用）。
默认值：NULL（无回调）
限制：仅在 NULL 或 READY 状态时可修改。
效果：通过注册回调函数，可在推理完成后立即获取原始输出并执行自定义逻辑（如特殊格式解析、业务处理），userdata 用于传递自定义参数。
```

#### 2.3.20 **unique-id**

```
含义：插件实例的唯一 ID，用于标识其输出的元数据。
默认值：15
范围：0~4294967295
限制：仅在 NULL 或 READY 状态时可修改。
作用：在多 nvinfer 插件的流水线中，下游插件（如跟踪器、显示器）通过此 ID 区分不同推理结果的元数据（如区分一级检测和二级分类的结果）。
```

### 2.4 总结

```
nvinfer是DeepStream推理流水线的核心，其属性配置需结合模型类型（检测/分类/分割）、场景需求（实时性/精度）、硬件资源（GPU 显存/算力） 综合调整：
    必设属性：config-file-path（模型配置）、batch-size（批量大小）、process-mode（推理模式）。
    性能优化：interval（降低推理频率）、model-engine-file（预生成引擎加速加载）。
    功能定制：infer-on-class-ids（二级推理过滤）、output-tensor-meta（自定义后处理）。
合理配置可最大化利用 GPU 资源，同时满足场景对延迟和精度的要求。
```

## 3.nvtracker

### 3.1插件介绍

```
nvtracker 是 DeepStream 中负责目标跟踪的核心插件，用于在连续帧中关联同一目标并分配唯一跟踪 ID，支持多种跟踪算法（如 NvDCF、KLT 等）。
```

### 3.2命令查看

```
命令：
	gst-inspect-1.0 nvtracker
输出：
Factory Details:
  Rank                     primary (256)
  Long-name                NvTracker plugin
  Klass                    NvTracker functionality
  Description              Gstreamer object tracking element
  Author                   NVIDIA Corporation. Post on Deepstream SDK forum for any queries @ https://devtalk.nvidia.com/default/board/209/

Plugin Details:
  Name                     nvdsgst_tracker
  Description              Gstreamer plugin to track the objects
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/deepstream/libnvdsgst_tracker.so
  Version                  6.3.0
  License                  Proprietary
  Source module            nvtracker
  Binary package           GStreamer nvtracker Plugin
  Origin URL               http://nvidia.com/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseTransform
                         +----GstNvTracker

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)I420, (string)NV12, (string)RGBA }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
  
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)I420, (string)NV12, (string)RGBA }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  compute-hw          : Compute Scaling HW
                        flags: readable, writable, controllable
                        Enum "GstNvComputeHWType" Default: 0, "Default"
                           (0): Default          - Default, GPU for Tesla, VIC for Jetson
                           (1): GPU              - GPU
                           (2): VIC              - VIC
  display-tracking-id : Display tracking id in object text
                        flags: readable, writable
                        Boolean. Default: true
  gpu-id              : Set GPU Device ID
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  input-tensor-meta   : Use preprocess tensormeta if available for tensor-meta-gie-id
                        flags: readable, writable
                        Boolean. Default: false
  ll-config-file      : Low-level library config file path
                        flags: readable, writable
                        String. Default: null
  ll-lib-file         : Low-level library file path
                        flags: readable, writable
                        String. Default: null
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "nvtracker0"
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  qos                 : Handle Quality-of-Service events
                        flags: readable, writable
                        Boolean. Default: false
  tensor-meta-gie-id  : Tensor Meta GIE ID to be used, property valid only if input-tensor-meta is TRUE
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  tracker-height      : Frame height at which the tracker should operate, in pixels
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 544 
  tracker-width       : Frame width at which the tracker should operate, in pixels
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 960 
  tracking-id-reset-mode: Tracking ID reset mode when stream reset or EOS happens
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 3 Default: 1 
  tracking-surface-type: Set Tracking Surface Type, default is ALL,        (1) => SPOT Surface, (2) => AISLE Surface
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  user-meta-pool-size : Tracker user meta buffer pool size
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 1 - 4294967295 Default: 16
```

### 3.3 参数讲解

#### 3.3.1 **compute-hw**

```
含义：指定跟踪过程中用于缩放（如目标区域预处理）的硬件（GPU 或 VIC）。
默认值：0（Default，自动选择：Tesla 平台用 GPU，Jetson 平台用 VIC）。
枚举值：
    0（Default）：自动适配硬件，平衡性能与功耗（推荐默认）。
    1（GPU）：强制使用 GPU 进行缩放，适合需要高精度处理的场景（如复杂目标特征提取）。
    2（VIC）：强制使用 Jetson 专用的 VIC（视频图像 compositor），适合低功耗、高吞吐量的场景。
优缺点：
    GPU：精度高，支持复杂操作，但功耗高，占用 GPU 算力。
    VIC（Jetson）：效率高、功耗低，但功能有限，仅支持基础缩放。	
```

#### 3.3.2 **display-tracking-id**

```
含义：控制是否在目标的叠加文本中显示跟踪 ID。
默认值：true（显示）。
效果：
    true：在目标边界框旁显示跟踪 ID（如 “ID:123”），方便可视化跟踪结果（适合调试或监控场景）。
    false：不显示跟踪 ID，仅显示目标类别等信息（适合对画面简洁度要求高的场景）。
```

#### 3.3.3 **gpu-id**

```
含义：指定用于跟踪计算的 GPU 设备 ID（多 GPU 系统中生效）。
默认值：0（默认使用第一块 GPU）。
范围：0~4294967295。
限制：仅在插件处于 NULL 或 READY 状态时可修改。
效果：在多 GPU 服务器上，可指定特定 GPU 处理跟踪任务（如 gpu-id=1），实现负载均衡，避免单 GPU 过载。
```

#### 3.3.4 **input-tensor-meta**

```
含义：是否使用上游插件（如 nvinfer）生成的预处理张量元数据（而非跟踪器内部预处理）。
默认值：false（使用跟踪器内部预处理）。
效果：
    true：依赖上游提供的预处理张量（如目标特征向量），适合自定义特征提取的场景（需配合 tensor-meta-gie-id 指定来源）。
    false：跟踪器内部对目标区域进行预处理（如缩放、灰度化），简化 pipeline 配置。
```

#### 3.3.5 **ll-config-file**

```
含义：底层跟踪库（如 NvDCF、KLT）的配置文件路径（必填，用于定义跟踪算法参数）。
默认值：null（需手动设置）。
作用：配置文件（如 tracker_config.yml）包含跟踪算法的核心参数，例如：
	 跟踪器类型（tracker-type: NvDCF）、关联阈值（minMatchingScore）、最大跟踪丢失帧数（maxShadowTrackingAge）等。
注意：不设置会导致跟踪器无法初始化，需根据选用的底层库（ll-lib-file）匹配配置文件。
```

#### 3.3.6 **ll-lib-file**

```
含义：底层跟踪库的动态链接库（.so）路径（必填，指定使用的跟踪算法）。
默认值：null（需手动设置）。
常用库路径：
    DeepStream 内置库：/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiicp.so（多目标跟踪）。
效果：选择不同的库对应不同的跟踪算法（如 NvDCF 适合高精度跟踪，KLT 适合快速跟踪），需与 ll-config-file 配套使用。
```

#### 3.3.7 **name**

```
含义：插件实例的名称（用于 pipeline 中标识该跟踪器）。
默认值："nvtracker0"。
效果：可自定义名称（如 "primary-tracker"），方便在多跟踪器场景中区分（如不同区域使用不同跟踪器）。
```

#### 3.3.8 **parent**

```
含义：指定插件的父对象（GstObject），用于 GStreamer 框架内部的对象管理。
效果：通常无需手动设置，由框架自动处理。
```

#### 3.3.9 **qos**

```
含义：是否处理服务质量（QoS）事件（如丢帧、延迟）。
默认值：false（不处理）。
效果：
    true：跟踪器会响应上游的 QoS 事件（如主动丢弃过时帧以降低延迟），适合实时性要求高的场景，但可能导致跟踪连续性下降（目标 ID 跳变）。
    false：严格按帧顺序处理，保证跟踪连续性，但延迟可能增加。
```

#### 3.3.10 **tensor-meta-gie-id**

```
含义：当 input-tensor-meta=true 时，指定提供张量元数据的 nvinfer 插件的 unique-id。
默认值：0。
限制：仅在 NULL 或 READY 状态时可修改，且仅当 input-tensor-meta=true 时生效。
效果：明确跟踪器使用哪个推理插件的输出张量（如 tensor-meta-gie-id=1 表示使用 unique-id=1 的 nvinfer 生成的特征向量）。
```

#### 3.3.11 **tracker-height / tracker-width**

```
含义：跟踪器内部处理的帧高 / 宽（目标区域会被缩放到该尺寸进行跟踪计算）。
默认值：tracker-height=544，tracker-width=960。
范围：0~4294967295（实际需为正数，且与输入帧比例适配）。
限制：仅在 NULL 或 READY 状态时可修改。
不同值的效果：
    增大尺寸（如 1080x1920）：保留更多目标细节，提高跟踪精度，但增加计算量（GPU 负载上升）。
    减小尺寸（如 272x480）：降低计算量，提升速度，但可能丢失细节（如小目标跟踪精度下降）。
建议：根据目标大小和硬件性能调整，默认值（544x960）在多数场景下平衡精度与性能。
```

#### 3.3.12 **tracking-id-reset-mode**

```
含义：当流重置（如摄像头重启）或收到 EOS（流结束）时，跟踪 ID 的重置模式。
默认值：1（部分重置）。
范围：0~3（具体行为依赖底层库，通常定义如下）：
    0：不重置（跟踪 ID 持续递增，即使流中断）。
    1：流重置时重置（仅当前流的跟踪 ID 从 0 开始，其他流不受影响）。
    2：全局重置（所有流的跟踪 ID 均重置为 0）。
    3：自定义逻辑（由底层库实现特殊重置规则）。	
```

#### 3.3.13 **tracking-surface-type**

```
含义：指定跟踪的 “表面类型”（用于特殊场景的跟踪区域限制）。
默认值：0（ALL，无限制）。
范围：0~4294967295（通常定义如下）：
    0：ALL（跟踪所有区域的目标）。
    1：SPOT Surface（仅跟踪指定 “点区域” 内的目标）。
    2：AISLE Surface（仅跟踪指定 “通道区域” 内的目标）。
效果：用于限制跟踪范围（如只跟踪超市收银台区域的目标），减少无关计算，提高效率。
```

#### 3.3.14 **user-meta-pool-size**

```
含义：跟踪器用户元数据（user meta）缓冲区池的大小（预分配的元数据缓冲区数量）。
默认值：16。
范围：1~4294967295。
限制：仅在 NULL 或 READY 状态时可修改。
效果：
    过小（如 8）：元数据缓冲区不足时，跟踪结果可能无法及时附加到帧，导致丢失。
    过大（如 64）：占用更多内存，但可应对突发的多目标场景（如瞬间出现大量目标）。
建议：根据最大目标数量调整，多路高并发场景可适当增大。
```

### 3.4 总结

```
nvtracker 的配置核心在于平衡跟踪精度、速度和资源占用，关键属性需重点关注：
    必设属性：ll-lib-file（底层跟踪库）、ll-config-file（算法参数）。
    性能优化：tracker-width/tracker-height（缩小尺寸提速）、compute-hw（Jetson 用 VIC 降功耗）。
    功能定制：tracking-id-reset-mode（ID 管理）、tracking-surface-type（区域限制）。
需根据场景（如实时监控、高密度人群跟踪）和硬件（Jetson/Tesla）选择合适的跟踪算法（如 NvDCF 适合高精度，KLT 适合高速），并通过配置文件微调参数（如关联阈值、丢失容忍帧数）。
```

## 4.nvmultistreamtiler

### 4.1 插件介绍

```
nvmultistreamtiler 是 DeepStream 中用于将多路视频流拼接成单帧 tiled 画面的插件（如监控系统中常见的多画面分割显示），支持灵活配置布局和输出尺寸。
```

### 4.2 命令查看

```
命令：
	gst-inspect-1.0 nvmultistreamtiler
输出：
Factory Details:
  Rank                     primary (256)
  Long-name                Stream Tiler DS
  Klass                    Generic
  Description              Tile input multistream buffer into a 2D array
  Author                   NVIDIA Corporation. Post on Deepstream for Tesla forum for any queries @ https://devtalk.nvidia.com/default/board/209/

Plugin Details:
  Name                     nvdsgst_multistreamtiler
  Description              NVIDIA Multistream Tiler plugin
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/deepstream/libnvdsgst_multistreamtiler.so
  Version                  6.3.0
  License                  Proprietary
  Source module            nvmultistreamTiler
  Binary package           NVIDIA Multistream Plugins
  Origin URL               http://nvidia.com/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseTransform
                         +----GstNvMultiStreamTiler

Pad Templates:
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA, (string)I420 }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
  
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA, (string)I420 }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  buffer-pool-size    : nvtiler output buffer pool size
                        flags: readable, writable
                        Unsigned Integer. Range: 4 - 10 Default: 5 
  columns             : Number of columns in the Tiled 2D output
                        flags: readable, writable
                        Unsigned Integer. Range: 1 - 4294967295 Default: 1 
  compute-hw          : Compute Scaling HW
                        flags: readable, writable, controllable
                        Enum "GstNvComputeHWType" Default: 0, "Default"
                           (0): Default          - Default, GPU for Tesla, VIC for Jetson
                           (1): GPU              - GPU
                           (2): VIC              - VIC
  custom-tile-config  : Specifies individual tile resolution for all involved sources
                        flags: writable
                        Pointer. Write only
  gpu-id              : Set GPU Device ID
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  height              : Height of the tiled output in pixels
                        flags: readable, writable
                        Unsigned Integer. Range: 16 - 4294967295 Default: 1080 
  interpolation-method: Set interpolation methods
                        flags: readable, writable, controllable
                        Enum "GstNvInterpolationMethod" Default: 6, "Default"
                           (0): Nearest          - Nearest
                           (1): Bilinear         - Bilinear
                           (2): Algo-1           - GPU - Cubic, VIC - 5 Tap
                           (3): Algo-2           - GPU - Super, VIC - 10 Tap
                           (4): Algo-3           - GPU - LanzoS, VIC - Smart
                           (5): Algo-4           - GPU - Ignored, VIC - Nicest
                           (6): Default          - GPU - Nearest, VIC - Nearest
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "nvmultistreamtiler0"
  nvbuf-memory-type   : Type of NvBufSurface Memory to be allocated for output buffers
                        flags: readable, writable, changeable only in NULL or READY state
                        Enum "GstNvBufMemoryType" Default: 0, "nvbuf-mem-default"
                           (0): nvbuf-mem-default - Default memory allocated, specific to particular platform
                           (1): nvbuf-mem-cuda-pinned - Allocate Pinned/Host cuda memory
                           (2): nvbuf-mem-cuda-device - Allocate Device cuda memory
                           (3): nvbuf-mem-cuda-unified - Allocate Unified cuda memory
                           (4): nvbuf-mem-surface-array - Allocate Surface Array memory, applicable for Jetson
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  qos                 : Handle Quality-of-Service events
                        flags: readable, writable
                        Boolean. Default: false
  rows                : Number of rows in the Tiled 2D output
                        flags: readable, writable
                        Unsigned Integer. Range: 1 - 4294967295 Default: 1 
  show-source         : ID of the source to be shown. If -1 all the sources will be tiled else only a single source will be scaled i
nto the output buffer.
                        flags: readable, writable
                        Integer. Range: -1 - 2147483647 Default: -1 
  width               : Width of the tiled output in pixels
                        flags: readable, writable
                        Unsigned Integer. Range: 16 - 4294967295 Default: 1920
```

### 4.3 参数讲解

#### 4.3.1 **buffer-pool-size**

```
含义：nvmultistreamtiler 输出缓冲区池的大小（预分配的 tiled 帧缓冲区数量）。
默认值：5
范围：4~10
效果：
    过小（如 4）：缓冲区不足时，上游 插件需等待缓冲区释放，可能导致帧率下降或画面卡顿。
    过大（如 10）：占用更多 GPU 内存，但可应对突发的帧处理需求（如多路流同时推帧）。
建议：默认值 5 适用于多数场景，多路高帧率流可适当增大至 8~10。	
```

#### 4.3.2 **columns**

```
含义：tiled 输出画面的列数（控制多路流的横向布局）。
默认值：1（单列布局）
范围：1~4294967295
效果：与 rows 共同决定布局，例如：
    columns=2、rows=2：4 路流按 2x2 网格布局。
    columns=3、rows=1：3 路流按横向排列（单行 3 列）。
注意：总 tile 数量（rows×columns）需 ≥ 实际流数量，否则部分流可能无法显示（或被压缩）。
优缺点：
    列数过多（如 8 列）：单路流显示区域过小，细节模糊；但可同时显示更多路流。
    列数过少（如 1 列）：单路流清晰，但需滚动查看多路流。
```

#### 4.3.3  **compute-hw**

```
含义：指定用于缩放（将单路流缩放到 tile 尺寸）的硬件（GPU 或 VIC）。
默认值：0（Default，自动选择：Tesla 用 GPU，Jetson 用 VIC）。
枚举值：
    0（Default）：自动适配硬件，平衡性能与功耗（推荐默认）。
    1（GPU）：强制用 GPU 缩放，适合需要高精度缩放的场景（如高清画质要求）。
    2（VIC）：强制用 Jetson 专用 VIC 硬件，适合低功耗、高吞吐量场景。
优缺点：
    GPU：缩放精度高，支持复杂算法；但功耗高，占用 GPU 算力。
    VIC（Jetson）：效率高、功耗低；但功能有限，仅支持基础缩放。
```

#### 4.3.4 **custom-tile-config**

```
含义：自定义每个 tile（单路流）的分辨率（仅支持通过代码设置，命令行不可配置）。
类型：指针（Write only）
效果：
	默认情况下，所有tile按统一尺寸分配（根据width/height、rows/columns自动计算）；通过此属性可指定每路流的单独尺寸（如某路流占满一行，其他流小尺寸排列）。
适用场景：需要差异化布局的场景（如重点监控区域用大 tile，其他区域用小 tile）。
```

#### 4.3.5 **gpu-id**

```
含义：指定用于 tile 拼接和缩放的 GPU 设备 ID（多 GPU 系统中生效）。
默认值：0（默认使用第一块 GPU）。
范围：0~4294967295
效果：在多 GPU 服务器上，可指定特定 GPU 处理拼接任务（如 gpu-id=1），实现负载均衡。
```

#### 4.3.6 **height**

```
含义：tiled 输出画面的总高度（像素）。
默认值：1080（1080p）
范围：16~4294967295
效果：与 width 共同决定输出分辨率，例如 width=1920、height=1080 对应 1080p 输出。
优缺点：
    过大（如 2160 即 4K）：画质细腻，但占用更多带宽和显存，对下游显示设备要求高。
    过小（如 540）：节省资源，但画面模糊，细节丢失。
```

#### 4.3.7 **interpolation-method**

```
含义：缩放单路流到 tile 尺寸时使用的插值算法（影响画面质量）。
默认值：6（Default，GPU 用最近邻，VIC 用最近邻）。
枚举值：
    0（Nearest）：最近邻插值，速度快但画质差（有锯齿）。
    1（Bilinear）：双线性插值，平衡速度与画质（推荐）。
    2~5：更高质量算法（如 Cubic、LanzoS），画质更好但计算耗时增加。
    6（Default）：按硬件自动选择（GPU 用 Nearest，VIC 用 Nearest）。
建议：对画质要求高的场景（如高清监控）用 Bilinear 或 Algo-2；追求速度时用 Nearest。
```

#### 4.3.8 **name**

```
含义：插件实例的名称（用于 pipeline 中标识该 tiler）。
默认值："nvmultistreamtiler0"
效果：可自定义名称（如 "4x4-tiler"），方便在多 tiler 场景中区分（如不同布局的拼接器）。
```

#### 4.3.9 **nvbuf-memory-type**

```
含义：指定输出 tiled 帧的内存类型（NvBufSurface）。
默认值：0（nvbuf-mem-default，自动选择）。
枚举值：
    0（default）：按平台自动选择（Jetson 用共享内存，Tesla 用 CUDA 内存）。
    1（cuda-pinned）：主机端 pinned 内存（CPU/GPU 均可访问，适合频繁读写）。
    2（cuda-device）：GPU 设备内存（仅 GPU 访问，速度快）。
    3（cuda-unified）：统一内存（CPU/GPU 自动映射，适合异构计算）。
    4（surface-array）：Jetson 专用表面数组内存（适合 VIC 硬件）。
建议：默认值即可，特殊场景（如 CPU 需要读取 tiled 帧）可手动选择。
```

#### 4.3.10 **parent**

```
含义：指定插件的父对象（GstObject），用于 GStreamer 框架内部管理。
效果：通常无需手动设置，由框架自动处理。
```

#### 4.3.11 **qos**

```
含义：是否处理服务质量（QoS）事件（如丢帧、延迟）。
默认值：false（不处理）。
效果：
    true：响应上游 QoS 事件（如主动丢帧以降低延迟），适合实时性要求高的场景，但可能导致画面卡顿。
    false：严格按帧顺序处理，保证画面流畅，但延迟可能增加。
```

#### 4.3.12 **rows**

```
含义：tiled 输出画面的行数（控制多路流的纵向布局）。
默认值：1（单行布局）
范围：1~4294967295
效果：与 columns 配合决定布局，例如 rows=3、columns=2 支持 6 路流按 3x2 网格显示。
注意：总 tile 数量需 ≥ 实际流数量，否则超出的流可能被忽略或压缩显示。
```

#### 4.3.13 **show-source**

```
含义：指定单独显示某一路流（而非拼接多路）。
默认值：-1（显示所有流，即拼接模式）。
范围：-1~2147483647（-1 表示全部，其他值为源 ID）。
效果：
    show-source=0：仅显示 ID 为 0 的流（全屏缩放至 width×height）。
    show-source=-1：按 rows×columns 拼接所有流。
适用场景：需要切换显示单路流细节的场景（如监控中放大某一区域）。
```

#### 4.3.14 **width**

```
含义：tiled 输出画面的总宽度（像素）。
默认值：1920（1080p 对应宽度）。
范围：16~4294967295
效果：与 height 共同决定输出分辨率，例如 width=3840、height=2160 对应 4K 输出。
注意：需与下游显示设备的分辨率兼容（如显示器支持 1080p 则无需设置过高）。
```

### 4.4 总结

```
nvmultistreamtiler 的核心是控制多路流的拼接布局和输出质量，配置时需结合流数量、显示设备分辨率、画质需求综合调整：
    必调属性：rows/columns（布局）、width/height（输出分辨率）。
    画质优化：interpolation-method（用双线性插值提升清晰度）。
    性能优化：compute-hw（Jetson 用 VIC 降功耗）、buffer-pool-size（按需调整避免卡顿）。
    灵活显示：通过 show-source 切换单流 / 多流模式，适合交互场景。
合理配置可在保证画面清晰的同时，最大化利用硬件资源，适配不同的显示需求。
```

## 5.nvvideoconvert

### 5.1 插件介绍

```
nvvideoconvert 是 DeepStream 中用于视频格式转换、缩放、裁剪和翻转的核心插件，支持硬件加速（GPU/VIC），广泛用于处理不同格式的视频流以适配下游插件（如编码器、显示器）。
```

### 5.2 命令查看

```
命令：
	gst-inspect-1.0 nvvideoconvert
输出：
Factory Details:
  Rank                     primary (256)
  Long-name                NvVidConv Plugin
  Klass                    Filter/Converter/Video/Scaler
  Description              Converts video from one colorspace to another & Resizes
  Author                   NVIDIA Corporation. Post on Deepstream SDK forum for any queries @ https://devtalk.nvidia.com/default/board/209/

Plugin Details:
  Name                     nvvideoconvert
  Description              video Colorspace conversion & scaler
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/deepstream/libgstnvvideoconvert.so
  Version                  1.2.3
  License                  Proprietary
  Source module            nvvideoconvert
  Binary package           GStreamer nvvideoconvert Plugin
  Origin URL               http://nvidia.com/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseTransform
                         +----Gstnvvideoconvert

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)I420, (string)NV12, (string)P010_10LE, (string)I420_12LE, (string)BGRx, (string)RGBA, (string)GRAY8, (string)YUY2
, (string)UYVY, (string)YVYU, (string)Y42B, (string)BGR, (string)RGB, (string)BGR10A2_LE, (string)UYVP }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
      video/x-raw
                 format: { (string)I420, (string)NV12, (string)P010_10LE, (string)BGRx, (string)RGBA, (string)GRAY8, (string)YUY2, (string)UYVY, (st
ring)YVYU, (string)Y42B, (string)BGR, (string)RGB, (string)BGR10A2_LE, (string)UYVP }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
  
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)I420, (string)NV12, (string)P010_10LE, (string)I420_12LE, (string)BGRx, (string)RGBA, (string)GRAY8, (string)YUY2
, (string)UYVY, (string)YVYU, (string)Y42B, (string)RGB, (string)BGR, (string)BGR10A2_LE, (string)UYVP }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
      video/x-raw
                 format: { (string)I420, (string)NV12, (string)P010_10LE, (string)BGRx, (string)RGBA, (string)GRAY8, (string)YUY2, (string)UYVY, (st
ring)YVYU, (string)Y42B, (string)RGB, (string)BGR, (string)BGR10A2_LE, (string)UYVP }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  allow-odd-crop      : Allow the odd dimensions for source and destination crop rectangle
                        flags: readable, writable
                        Boolean. Default: true
  bl-output           : Blocklinear output, applicable only for memory:NVMM NV12 format output buffer
                        flags: readable, writable
                        Boolean. Default: false
  compute-hw          : Compute Scaling HW
                        flags: readable, writable, controllable
                        Enum "GstNvComputeHWType" Default: 0, "Default"
                           (0): Default          - Default, GPU for Tesla, VIC for Jetson
                           (1): GPU              - GPU
                           (2): VIC              - VIC
  contiguous-buffers  : Transformed output buffers in a batch are contiguous in memory.
                        flags: readable, writable
                        Boolean. Default: false
  copy-hw             : Select hardware used for surface copies.
                        flags: readable, writable, controllable
                        Enum "GstNvCopyHWType" Default: 1, "GPU"
                           (1): GPU              - GPU
                           (2): VIC              - VIC
  dest-crop           : Pixel location left:top:width:height
                        Use string with values of crop location to set the property.
                         e.g. 20:20:40:50
                        flags: readable, writable, changeable only in NULL or READY state
                        String. Default: "0:0:0:0"
  disable-passthrough : Disable passthrough mode at init time
                        flags: readable, writable
                        Boolean. Default: false
  flip-method         : video flip methods
                        flags: readable, writable, controllable
                        Enum "GstNvDsVideoFlipMethod" Default: 0, "none"
                           (0): none             - Identity (no rotation)
                           (1): counterclockwise - Rotate counter-clockwise 90 degrees
                           (2): rotate-180       - Rotate 180 degrees
                           (3): clockwise        - Rotate clockwise 90 degrees
                           (4): horizontal-flip  - Flip horizontally
                           (5): upper-right-diagonal - Flip across upper right/lower left diagonal
                           (6): vertical-flip    - Flip vertically
                           (7): upper-left-diagonal - Flip across upper left/lower right diagonal
  gpu-id              : Set GPU Device ID for operation
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  interpolation-method: Set interpolation methods
                        flags: readable, writable, controllable
                        Enum "GstNvInterpolationMethod" Default: 6, "Default"
                           (0): Nearest          - Nearest
                           (1): Bilinear         - Bilinear
                           (2): Algo-1           - GPU - Cubic, VIC - 5 Tap
                           (3): Algo-2           - GPU - Super, VIC - 10 Tap
                           (4): Algo-3           - GPU - LanzoS, VIC - Smart
                           (5): Algo-4           - GPU - Ignored, VIC - Nicest
                           (6): Default          - GPU - Nearest, VIC - Nearest
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "nvvideoconvert0"
  nvbuf-memory-type   : Type of NvBufSurface Memory to be allocated for output buffers
                        flags: readable, writable, changeable only in NULL or READY state
                        Enum "GstNvBufMemoryType" Default: 0, "nvbuf-mem-default"
                           (0): nvbuf-mem-default - Default memory allocated, specific to particular platform
                           (1): nvbuf-mem-cuda-pinned - Allocate Pinned/Host cuda memory
                           (2): nvbuf-mem-cuda-device - Allocate Device cuda memory
                           (3): nvbuf-mem-cuda-unified - Allocate Unified cuda memory
                           (4): nvbuf-mem-surface-array - Allocate Surface Array memory, applicable for Jetson
  output-buffers      : number of output buffers
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                        Unsigned Integer. Range: 1 - 4294967295 Default: 4 
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  qos                 : Handle Quality-of-Service events
                        flags: readable, writable
                        Boolean. Default: false
  silent              : Produce verbose output ?
                        flags: readable, writable
                        Boolean. Default: false
  src-crop            : Pixel location left:top:width:height
                        Use string with values of crop location to set the property.
                         e.g. 20:20:40:50
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                        String. Default: "0:0:0:0"
```

### 5.3 参数讲解

#### 5.3.1 **allow-odd-crop**

```
含义：允许源 / 目标裁剪区域的尺寸为奇数（如宽度或高度为 3、5 等奇数像素）。
默认值：true（允许）。
效果：
    true：支持奇数尺寸裁剪，灵活度高（如裁剪 101x201 区域）。
    false：限制裁剪区域尺寸为偶数，避免部分硬件（如 VIC）对奇数尺寸处理效率低的问题，但灵活性下降。
```

#### 5.3.2 **bl-output**

```
含义：是否输出 “块线性（Blocklinear）” 格式的 NVMM 内存缓冲区（仅适用于 memory:NVMM 且格式为 NV12 的输出）。
默认值：false（输出线性格式）。
背景：块线性是 Jetson 平台专用的内存布局，适合硬件加速器（如 VIC、编码器）直接访问，效率更高。
效果：
    true：输出块线性布局，提升下游硬件处理效率（如 Jetson 上的编码 / 显示）。
    false：输出线性布局，兼容性更好（适合 CPU 访问或通用处理）。
```

#### 5.3.3 **compute-hw**

```
含义：指定用于缩放和格式转换的硬件（GPU 或 VIC）。
默认值：0（Default，自动选择：Tesla 用 GPU，Jetson 用 VIC）。
枚举值：
    0（Default）：自动适配硬件，平衡性能与功耗（推荐默认）。
    1（GPU）：强制用 GPU 处理，支持更多格式和复杂算法（如高精度缩放）。
    2（VIC）：强制用 Jetson 专用 VIC 硬件，适合低功耗、高吞吐量的基础转换。
优缺点：
    GPU：功能全、精度高，但占用 GPU 算力，功耗高。
    VIC（Jetson）：效率高、功耗低，但支持的格式和算法有限。
```

#### 5.3.4 **contiguous-buffers**

```
含义：批处理（batch）中转换后的输出缓冲区是否在内存中连续存储。
默认值：false（不连续）。
效果：
    true：缓冲区连续存储，适合需要连续内存块的下游插件（如某些编码器），但可能增加内存分配开销。
    false：缓冲区分散存储，内存利用率高，适合多数场景。
```

#### 5.3.5 **copy-hw**

```
含义：选择用于表面（surface）复制的硬件（GPU 或 VIC）。
默认值：1（GPU）。
枚举值：
    1（GPU）：用 GPU 复制，适合跨内存类型（如 NVMM 到 CPU 内存）的复制，兼容性好。
    2（VIC）：用 VIC 复制，适合 Jetson 平台上的快速内存到内存复制，效率更高。
```

#### 5.3.6 **dest-crop**

```
含义：对转换后的输出帧进行裁剪，指定裁剪区域的左上角坐标和尺寸。
格式：字符串 "left:top:width:height"（如 "20:20:400:300" 表示从 (20,20) 开始裁剪 400x300 区域）。
默认值："0:0:0:0"（不裁剪）。
限制：仅在 NULL 或 READY 状态时可修改。
效果：在输出前进一步裁剪画面（如去除黑边），适合下游需要固定区域的场景。
```

#### 5.3.7 **disable-passthrough**

```
含义：初始化时禁用 “直通模式”（即输入输出格式 / 尺寸相同时直接转发，不处理）。
默认值：false（启用直通模式）。
效果：
    true：强制插件处理所有帧（即使格式 / 尺寸无需转换），适合需要统一处理流程的场景（如添加元数据），但增加开销。
    false：自动启用直通模式，减少不必要的处理，提升性能。
```

#### 5.3.8 **flip-method**

```
含义：视频翻转 / 旋转方式（如顺时针旋转 90 度、水平翻转等）。
默认值：0（none，无翻转）。
枚举值：
    0（none）：无旋转 / 翻转。
    1（counterclockwise）：逆时针旋转 90 度。
    2（rotate-180）：旋转 180 度。
    3（clockwise）：顺时针旋转 90 度。
    4（horizontal-flip）：水平翻转（左右颠倒）。
    5~7：对角线翻转等特殊模式（较少用）。
适用场景：纠正摄像头安装方向导致的画面颠倒（如倒挂的摄像头旋转 180 度）。
```

#### 5.3.9 **gpu-id**

```
含义：指定用于处理的 GPU 设备 ID（多 GPU 系统中生效）。
默认值：0（默认使用第一块 GPU）。
范围：0~4294967295。
限制：仅在 NULL 或 READY 状态时可修改。
效果：多 GPU 场景中分配特定 GPU 处理，实现负载均衡。
```

#### 5.3.10 **interpolation-method**

```
含义：缩放时使用的插值算法（影响画面质量）。
默认值：6（Default，GPU 用最近邻，VIC 用最近邻）。
枚举值：
    0（Nearest）：最近邻插值，速度快但画质差（有锯齿）。
    1（Bilinear）：双线性插值，平衡速度与画质（推荐）。
    2~5：更高质量算法（如 Cubic、LanzoS），画质更好但耗时增加。
    6（Default）：按硬件自动选择。
建议：对画质敏感的场景（如监控）用 Bilinear；追求速度用 Nearest。
```

#### 5.3.11 **name**

```
含义：插件实例名称，用于 pipeline 中标识该插件。
默认值："nvvideoconvert0"。
效果：自定义名称（如 "format-converter"）方便调试和多实例区分。
```

#### 5.3.12 **nvbuf-memory-type**

```
含义：输出缓冲区的内存类型（NvBufSurface）。
默认值：0（nvbuf-mem-default，自动选择）。
枚举值：
    0（default）：按平台自动选择（Jetson 用共享内存，Tesla 用 CUDA 内存）。
    1（cuda-pinned）：主机端 pinned 内存（CPU/GPU 均可访问，适合频繁读写）。
    2（cuda-device）：GPU 设备内存（仅 GPU 访问，速度快）。
    3（cuda-unified）：统一内存（CPU/GPU 自动映射）。
    4（surface-array）：Jetson 专用表面数组内存（适合 VIC）。
```

#### 5.3.13 **output-buffers**

```
含义：输出缓冲区的数量（预分配的缓冲区池大小）。
默认值：4。
范围：1~4294967295。
效果：
    过小（如 2）：缓冲区不足时导致上游阻塞，帧率下降。
    过大（如 16）：占用更多内存，但可应对突发帧处理需求。
```

#### 5.3.14 **parent**

```
含义：GStreamer 框架内部的父对象管理，通常无需手动设置。
```

#### 5.3.15 **qos**

```
含义：是否处理服务质量（QoS）事件（如丢帧、延迟）。
默认值：false（不处理）。
效果：
    true：响应上游 QoS 事件（如主动丢帧降延迟），适合实时场景，但可能影响画面完整性。
    false：按顺序处理所有帧，保证画面完整，但延迟可能增加。	
```

#### 5.3.16 **silent**

```
含义：是否禁用详细日志输出。
默认值：false（输出日志）。
效果：true 时减少日志打印，适合生产环境；false 保留日志，方便调试。
```

#### 5.3.17 **src-crop**

```
含义：对输入帧进行裁剪，指定裁剪区域的左上角坐标和尺寸（格式同 dest-crop）。
默认值："0:0:0:0"（不裁剪）。
可修改时机：在 NULL、READY、PAUSED、PLAYING 状态均可修改（支持动态调整）。
效果：预处理输入帧（如去除边缘无关区域），减少后续处理的计算量。
```

### 5.4 总结

```
nvvideoconvert 是视频处理流水线的 “格式桥梁”，核心功能是格式转换、缩放和裁剪，配置时需关注：
    格式适配：通过 compute-hw 和 nvbuf-memory-type 匹配硬件和下游插件需求。
    画质与性能平衡：interpolation-method 选择双线性插值，兼顾质量和速度。
    灵活处理：src-crop/dest-crop 裁剪无关区域，flip-method 纠正画面方向。
合理配置可确保视频流在不同插件间高效传输，同时满足画质和实时性要求。
```

## 6.nvdsosd

### 6.1 插件介绍

```
nvdsosd（NVIDIA DeepStream On-Screen Display）是 DeepStream 中用于在视频帧上叠加目标边界框、文本标签、时钟等元数据的核心插件，主要用于可视化推理和跟踪结果（如监控画面中显示检测到的 “人” “车” 及其 ID）。
```

### 6.2 命令查看

```
命令：
	gst-inspect-1.0 nvdsosd
输出：
Factory Details:
  Rank                     primary (256)
  Long-name                NvDsOsd plugin
  Klass                    NvDsOsd functionality
  Description              Gstreamer bounding box draw element
  Author                   NVIDIA Corporation. Post on Deepstream for Tesla forum for any queries @ https://devtalk.nvidia.com/default/board/209/

Plugin Details:
  Name                     nvdsgst_osd
  Description              Gstreamer plugin to draw rectangles and text
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/deepstream/libnvdsgst_osd.so
  Version                  6.3.0
  License                  Proprietary
  Source module            nvdsosd
  Binary package           GStreamer nvosd Plugin
  Origin URL               http://nvidia.com/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseTransform
                         +----GstNvDsOsd

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]
  
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                 format: { (string)NV12, (string)RGBA }
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
              framerate: [ 0/1, 2147483647/1 ]

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  clock-color         : clock-color
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  clock-font          : Clock Font to be set
                        flags: readable, writable
                        String. Default: null
  clock-font-size     : font size of the clock
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 60 Default: 0 
  display-bbox        : Whether to display bounding boxes
                        flags: readable, writable
                        Boolean. Default: true
  display-clock       : Whether to display clock
                        flags: readable, writable
                        Boolean. Default: false
  display-mask        : Whether to display instance mask
                        flags: readable, writable
                        Boolean. Default: false
  display-text        : Whether to display text
                        flags: readable, writable
                        Boolean. Default: true
  gpu-id              : Set GPU Device ID
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "nvdsosd0"
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  process-mode        : Rect and text draw process mode, CPU_MODE only support RGBA format
                        flags: readable, writable, changeable only in NULL or READY state
                        Enum "GstNvDsOsdMode" Default: 1, "MODE_GPU"
                           (0): MODE_CPU         - CPU_MODE
                           (1): MODE_GPU         - GPU_MODE
                           (2): MODE_NONE        - Invalid mode. Falls back to GPU
  qos                 : Handle Quality-of-Service events
                        flags: readable, writable
                        Boolean. Default: false
  x-clock-offset      : x-clock-offset
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  y-clock-offset      : y-clock-offset
                        flags: readable, writable, changeable only in NULL or READY state
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0
```

### 6.3 参数讲解

#### 6.3.1 **clock-color**

```
含义：叠加时钟的颜色（ARGB 格式，即透明度 + RGB 分量）。
默认值：0（全透明，默认不显示时钟）。
范围：0~4294967295（十六进制表示为 0xAARRGGBB，如 0xFFFF0000 表示红色不透明）。
限制：仅在 NULL 或 READY 状态时可修改，且需 display-clock=true 才生效。
效果：自定义时钟颜色（如白色时钟 0xFFFFFFFF），适配不同背景画面。
```

#### 6.3.2 **clock-font**

```
含义：叠加时钟使用的字体文件路径。
默认值：null（使用系统默认字体）。
效果：指定自定义字体（如 /usr/share/fonts/truetype/freefont/FreeSans.ttf），改变时钟的显示样式。
```

#### 6.3.3 **clock-font-size**

```
含义：叠加时钟的字体大小。
默认值：0（默认大小，约 12pt）。
范围：0~60（单位：磅）。
限制：仅在 NULL 或 READY 状态时可修改，需 display-clock=true 生效。
效果：调整时钟文字大小（如 20 表示较大字体），适应不同分辨率的显示需求。
```

#### 6.3.4 **display-bbox**

```
含义：是否在视频帧上显示目标的边界框（Bounding Box）。
默认值：true（显示）。
效果：
    true：在检测到的目标周围绘制矩形框（颜色由元数据中的类别决定，如人用蓝色、车用车绿色），直观展示目标位置。
    false：不显示边界框，仅保留其他信息（如文本标签），适合对画面简洁度要求高的场景。
```

#### 6.3.5 **display-clock**

```
含义：是否在视频帧上叠加系统时钟（如 “2025-11-08 12:34:56”）。
默认值：false（不显示）。
效果：
    true：在指定位置（x-clock-offset/y-clock-offset）显示当前时间，适合需要时间戳记录的场景（如监控录像）。
    false：不显示时钟，减少画面干扰。
```

#### 6.3.6 **display-mask**

```
含义：是否显示实例掩码（Instance Mask，如语义分割中目标的像素级掩码）。
默认值：false（不显示）。
效果：
    true：对分割模型输出的掩码区域填充颜色（如用半透明红色覆盖 “行人” 区域），适合分割任务的可视化。
    false：不显示掩码，仅显示边界框和文本。
```

#### 6.3.7 **display-text**

```
含义：是否在目标旁显示文本标签（如类别名称 “person”、跟踪 ID“ID:123”、置信度 “95%”）。
默认值：true（显示）。
效果：
    true：在边界框附近显示元数据文本，提供目标的详细信息（需上游插件生成文本元数据）。
    false：仅显示边界框，不显示文本，适合画面信息密集的场景。
```

#### 6.3.8 **gpu-id**

```
含义：指定用于绘制叠加内容的 GPU 设备 ID（多 GPU 系统中生效）。
默认值：0（默认使用第一块 GPU）。
范围：0~4294967295。
限制：仅在 NULL 或 READY 状态时可修改。
效果：多 GPU 场景中分配特定 GPU 处理绘制任务，避免单 GPU 负载过高。
```

#### 6.3.9 **name**

```
含义：插件实例的名称（用于 pipeline 中标识该 OSD 插件）。
默认值："nvdsosd0"。
效果：可自定义名称（如 "primary-osd"），方便在多 OSD 插件场景中区分（如不同流使用不同 OSD 配置）。
```

#### 6.3.10 **parent**

```
含义：GStreamer 框架内部的父对象管理，通常无需手动设置。
```

#### 6.3.11 **process-mode**

```
含义：绘制边界框和文本的处理模式（CPU 或 GPU 加速）。
默认值：1（MODE_GPU，GPU 加速）。
枚举值：
    0（MODE_CPU）：使用 CPU 绘制，仅支持 RGBA 格式的视频帧，适合无 GPU 加速的场景（效率低）。
    1（MODE_GPU）：使用 GPU 加速绘制，支持 NV12 和 RGBA 格式，效率高（推荐默认）。
    2（MODE_NONE）：无效模式，自动 fallback 到 MODE_GPU。
限制：仅在 NULL 或 READY 状态时可修改。
优缺点：
    MODE_GPU：速度快，支持更多格式，适合实时场景。
    MODE_CPU：兼容性差（仅 RGBA），速度慢，仅用于特殊调试场景。
```

#### 6.3.12 **qos**

```
含义：是否处理服务质量（QoS）事件（如丢帧、延迟）。
默认值：false（不处理）。
效果：
    true：响应上游 QoS 事件（如主动丢弃部分帧以降低延迟），可能导致叠加内容不连续（如某帧的边界框丢失）。
    false：按顺序处理所有帧，保证叠加内容完整，但延迟可能增加。
```

#### 6.3.13 **x-clock-offset / y-clock-offset**

```
含义：叠加时钟在视频帧中的 X/Y 轴偏移量（左上角为原点，单位：像素）。
默认值：均为 0（左上角位置）。
范围：0~4294967295。
限制：仅在 NULL 或 READY 状态时可修改，需 display-clock=true 生效。
效果：调整时钟位置（如 x=100, y=50 表示时钟左上角在 (100,50) 像素处），避免遮挡关键内容。
```

### 6.4 总结

```
nvdsosd 是 DeepStream 可视化的核心插件，主要用于将算法结果（边界框、文本、掩码）叠加到视频上，配置需关注：
    核心显示控制：display-bbox（边界框）、display-text（文本）、display-mask（掩码），按需开启 / 关闭。
    性能优化：process-mode 保持默认 MODE_GPU，利用 GPU 加速绘制，避免 CPU 瓶颈。
    辅助功能：display-clock 用于时间戳记录，clock-color/clock-font-size 自定义时钟样式。
合理配置可在保证可视化效果的同时，最小化对 pipeline 性能的影响，适合监控、演示等需要直观展示算法结果的场景。
```

## 7.capsfilter

### 7.1 插件介绍

```
capsfilter 是 GStreamer 核心插件之一，用于在 pipeline 中限制媒体流的格式（如视频的分辨率、编码格式，音频的采样率等），通过 “能力过滤” 确保上下游插件之间的格式兼容。它本身不修改数据，仅作为格式校验和筛选的 “阀门”。
```

### 7.2 命令查看

```
命令：
	gst-inspect-1.0 capsfilter
输出：
Factory Details:
  Rank                     none (0)
  Long-name                CapsFilter
  Klass                    Generic
  Description              Pass data without modification, limiting formats
  Author                   David Schleef <ds@schleef.org>

Plugin Details:
  Name                     coreelements
  Description              GStreamer core elements
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstcoreelements.so
  Version                  1.16.3
  License                  LGPL
  Source module            gstreamer
  Source release date      2020-10-21
  Binary package           GStreamer (Ubuntu)
  Origin URL               https://launchpad.net/distros/ubuntu/+source/gstreamer1.0

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseTransform
                         +----GstCapsFilter

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      ANY
  
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      ANY

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  caps                : Restrict the possible allowed capabilities (NULL means ANY). Setting this property takes a reference to the supplied GstCaps object.
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                                                   ANY

  caps-change-mode    : Filter caps change behaviour
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                        Enum "GstCapsFilterCapsChangeMode" Default: 0, "immediate"
                           (0): immediate        - Only accept the current filter caps
                           (1): delayed          - Temporarily accept previous filter caps
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "capsfilter0"
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  qos                 : Handle Quality-of-Service events
                        flags: readable, writable
                        Boolean. Default: false
```

### 7.3 参数讲解

#### 7.3.1 **caps**

```
含义：设置允许通过的媒体流格式（即 “能力约束”），格式需符合 GStreamer 的 GstCaps 规范（如视频分辨率、编码格式、帧率等）。
默认值：NULL（表示允许任何格式，即不限制）。
可修改时机：在 NULL、READY、PAUSED、PLAYING 状态均可动态修改。
常见用法示例：
    限制视频为 NV12 格式、1920x1080 分辨率：caps="video/x-raw(memory:NVMM), format=NV12, width=1920, height=1080"
    限制音频为 44.1kHz 采样率、立体声：caps="audio/x-raw, rate=44100, channels=2"
效果：
    若上游输出的格式与 caps 匹配，则数据通过；否则被过滤（pipeline 可能报错或停滞）。
    用于强制上下游插件使用指定格式（如让 nvvideoconvert 输出 RGBA 格式给下游渲染器）。
```

#### 7.3.1 **caps-change-mode**

```
含义：当 caps 属性动态修改时，插件处理格式变化的行为模式。
默认值：0（immediate，立即生效）。
枚举值：
    0（immediate）：立即应用新的 caps 约束，仅接受符合新格式的数据，旧格式数据被拒绝。
    1（delayed）：暂时接受旧格式数据，直到上游插件切换到新格式，避免格式切换时的瞬间断流。
可修改时机：在 NULL、READY、PAUSED、PLAYING 状态均可修改。
适用场景：
    immediate：适合格式固定的场景，确保严格符合约束。
    delayed：适合需要动态切换格式的场景（如分辨率自适应），提高兼容性。
```

#### 7.3.1 **name**

```
含义：插件实例的名称，用于在 pipeline 中标识该 capsfilter。
默认值："capsfilter0"。
效果：自定义名称（如 "nv12-caps"）方便调试和区分多个 capsfilter 实例（如 pipeline 中需多次过滤格式时）。
```

#### 7.3.1 **parent**

```
含义：GStreamer 框架内部的父对象管理，用于对象层级组织，通常无需手动设置。
```

#### 7.3.1 **qos**

```
含义：是否处理服务质量（QoS）事件（如丢帧、延迟提示）。
默认值：false（不处理）。
效果：
    true：插件会响应上游的 QoS 事件（如主动丢弃不符合格式的帧以维持流畅性）。
    false：忽略 QoS 事件，仅按 caps 约束过滤格式，可能因格式不匹配导致 pipeline 阻塞。
```

### 7.4 总结

```
capsfilter 是 GStreamer 中实现 “格式协商” 的关键插件，核心作用是：
    强制格式匹配：确保上游输出的媒体格式与下游插件支持的格式一致（如让 nvstreammux 输出的批量帧格式符合 nvinfer 的输入要求）。
    筛选特定格式：从多种支持的格式中选择最优格式（如在多个分辨率中指定使用 1080p）。
    动态格式切换：配合 caps-change-mode 实现运行时的格式调整（如根据网络状况切换视频分辨率）。
```

## 8.x264enc

### 8.1 插件介绍

```
x264enc 是基于 libx264 库的 GStreamer H.264 视频编码器插件，用于将原始视频流编码为 H.264 压缩格式，广泛应用于视频存储、直播、点播等场景。
```

### 8.2 命令查看

```
命令：
	gst-inspect-1.0 x264enc
输出：
Factory Details:
  Rank                     primary (256)
  Long-name                x264enc
  Klass                    Codec/Encoder/Video
  Description              H264 Encoder
  Author                   Josef Zlomek <josef.zlomek@itonis.tv>, Mark Nauwelaerts <mnauw@users.sf.net>

Plugin Details:
  Name                     x264
  Description              libx264-based H264 plugins
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstx264.so
  Version                  1.16.2
  License                  GPL
  Source module            gst-plugins-ugly
  Source release date      2019-12-03
  Binary package           GStreamer Ugly Plugins (Ubuntu)
  Origin URL               https://launchpad.net/distros/ubuntu/+source/gst-plugins-ugly1.0

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstVideoEncoder
                         +----GstX264Enc

Implemented Interfaces:
  GstPreset

Pad Templates:
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw
              framerate: [ 0/1, 2147483647/1 ]
                  width: [ 16, 2147483647 ]
                 height: [ 16, 2147483647 ]
                 format: { (string)Y444, (string)Y42B, (string)I420, (string)YV12, (string)NV12, (string)Y444_10LE, (string)I422_10LE, (string)I420_10LE }
  
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-h264
              framerate: [ 0/1, 2147483647/1 ]
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
          stream-format: { (string)avc, (string)byte-stream }
              alignment: au
                profile: { (string)high-4:4:4, (string)high-4:2:2, (string)high-10, (string)high, (string)main, (string)baseline, (string)constrained-baseline, (string)high-4:4:4-intra, (string)high-4:2:2-intra, (string)high-10-intra }

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  analyse             : Partitions to consider
                        flags: readable, writable
                        Flags "GstX264EncAnalyse" Default: 0x00000000, "(none)"
                           (0x00000001): i4x4             - i4x4
                           (0x00000002): i8x8             - i8x8
                           (0x00000010): p8x8             - p8x8
                           (0x00000020): p4x4             - p4x4
                           (0x00000100): b8x8             - b8x8
  aud                 : Use AU (Access Unit) delimiter
                        flags: readable, writable
                        Boolean. Default: true
  b-adapt             : Automatically decide how many B-frames to use
                        flags: readable, writable
                        Boolean. Default: true
  b-pyramid           : Keep some B-frames as references
                        flags: readable, writable
                        Boolean. Default: false
  bframes             : Number of B-frames between I and P
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 16 Default: 0 
  bitrate             : Bitrate in kbit/sec
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                        Unsigned Integer. Range: 1 - 2048000 Default: 2048 
  byte-stream         : Generate byte stream format of NALU
                        flags: readable, writable
                        Boolean. Default: false
  cabac               : Enable CABAC entropy coding
                        flags: readable, writable
                        Boolean. Default: true
  dct8x8              : Adaptive spatial transform size
                        flags: readable, writable
                        Boolean. Default: false
  frame-packing       : Set frame packing mode for Stereoscopic content
                        flags: readable, writable
                        Enum "GstX264EncFramePacking" Default: -1, "auto"
                           (-1): auto             - Automatic (use incoming video information)
                           (0): checkerboard     - checkerboard - Left and Right pixels alternate in a checkerboard pattern
                           (1): column-interleaved - column interleaved - Alternating pixel columns represent Left and Right views
                           (2): row-interleaved  - row interleaved - Alternating pixel rows represent Left and Right views
                           (3): side-by-side     - side by side - The left half of the frame contains the Left eye view, the right half the Right 
eye view
                           (4): top-bottom       - top bottom - L is on top, R on bottom
                           (5): frame-interleaved - frame interleaved - Each frame contains either Left or Right view alternately
  insert-vui          : Insert VUI NAL in stream
                        flags: readable, writable
                        Boolean. Default: true
  interlaced          : Interlaced material
                        flags: readable, writable
                        Boolean. Default: false
  intra-refresh       : Use Periodic Intra Refresh instead of IDR frames
                        flags: readable, writable
                        Boolean. Default: false
  ip-factor           : Quantizer factor between I- and P-frames
                        flags: readable, writable
                        Float. Range:               0 -               2 Default:             1.4 
  key-int-max         : Maximal distance between two key-frames (0 for automatic)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 2147483647 Default: 0 
  mb-tree             : Macroblock-Tree ratecontrol
                        flags: readable, writable
                        Boolean. Default: true
  me                  : Integer pixel motion estimation method
                        flags: readable, writable
                        Enum "GstX264EncMe" Default: 1, "hex"
                           (0): dia              - dia
                           (1): hex              - hex
                           (2): umh              - umh
                           (3): esa              - esa
                           (4): tesa             - tesa
  multipass-cache-file: Filename for multipass cache file
                        flags: readable, writable
                        String. Default: "x264.log"
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "x264enc0"
  noise-reduction     : Noise reduction strength
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 100000 Default: 0 
  option-string       : String of x264 options (overridden by element properties) in the format "key1=value1:key2=value2".
                        flags: readable, writable
                        String. Default: ""
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  pass                : Encoding pass/type
                        flags: readable, writable
                        Enum "GstX264EncPass" Default: 0, "cbr"
                           (0): cbr              - Constant Bitrate Encoding
                           (4): quant            - Constant Quantizer
                           (5): qual             - Constant Quality
                           (17): pass1            - VBR Encoding - Pass 1
                           (18): pass2            - VBR Encoding - Pass 2
                           (19): pass3            - VBR Encoding - Pass 3
  pb-factor           : Quantizer factor between P- and B-frames
                        flags: readable, writable
                        Float. Range:               0 -               2 Default:             1.3 
  psy-tune            : Preset name for psychovisual tuning options
                        flags: readable, writable
                        Enum "GstX264EncPsyTune" Default: 0, "none"
                           (0): none             - No tuning
                           (1): film             - Film
                           (2): animation        - Animation
                           (3): grain            - Grain
                           (4): psnr             - PSNR
                           (5): ssim             - SSIM
  qos                 : Handle Quality-of-Service events from downstream
                        flags: readable, writable
                        Boolean. Default: false
  qp-max              : Maximum quantizer
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 51 Default: 51 
  qp-min              : Minimum quantizer
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 51 Default: 10 
  qp-step             : Maximum quantizer difference between frames
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 50 Default: 4 
  quantizer           : Constant quantizer or quality to apply
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 50 Default: 21 
  rc-lookahead        : Number of frames for frametype lookahead
                        flags: readable, writable
                        Integer. Range: 0 - 250 Default: 40 
  ref                 : Number of reference frames
                        flags: readable, writable
                        Unsigned Integer. Range: 1 - 12 Default: 1 
  sliced-threads      : Low latency but lower efficiency threading
                        flags: readable, writable
                        Boolean. Default: false
  speed-preset        : Preset name for speed/quality tradeoff options (can affect decode compatibility - impose restrictions separately for your 
target decoder)
                        flags: readable, writable
                        Enum "GstX264EncPreset" Default: 6, "medium"
                           (0): None             - No preset
                           (1): ultrafast        - ultrafast
                           (2): superfast        - superfast
                           (3): veryfast         - veryfast
                           (4): faster           - faster
                           (5): fast             - fast
                           (6): medium           - medium
                           (7): slow             - slow
                           (8): slower           - slower
                           (9): veryslow         - veryslow
                           (10): placebo          - placebo
  sps-id              : SPS and PPS ID number
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 31 Default: 0 
  subme               : Subpixel motion estimation and partition decision quality: 1=fast, 10=best
                        flags: readable, writable
                        Unsigned Integer. Range: 1 - 10 Default: 1 
  sync-lookahead      : Number of buffer frames for threaded lookahead (-1 for automatic)
                        flags: readable, writable
                        Integer. Range: -1 - 250 Default: -1 
  threads             : Number of threads used by the codec (0 for automatic)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 2147483647 Default: 0 
  trellis             : Enable trellis searched quantization
                        flags: readable, writable
                        Boolean. Default: true
  tune                : Preset name for non-psychovisual tuning options
                        flags: readable, writable
                        Flags "GstX264EncTune" Default: 0x00000000, "(none)"
                           (0x00000001): stillimage       - Still image
                           (0x00000002): fastdecode       - Fast decode
                           (0x00000004): zerolatency      - Zero latency
  vbv-buf-capacity    : Size of the VBV buffer in milliseconds
                        flags: readable, writable, changeable in NULL, READY, PAUSED or PLAYING state
                        Unsigned Integer. Range: 0 - 10000 Default: 600 
  weightb             : Weighted prediction for B-frames
                        flags: readable, writable
                        Boolean. Default: false

Presets:
  "Profile Baseline"
  "Profile High"
  "Profile Main"
  "Profile YouTube"
  "Quality High"
  "Quality Low"
  "Quality Normal"
```

### 8.3 参数讲解

#### 8.3.1 **analyse**

```
含义：指定编码器分析的宏块分区类型（影响运动估计精度和压缩效率）。
默认值：0x00000000（(none)，不启用额外分区分析）。
Flags 选项：
    i4x4/i8x8：分析 intra 宏块的 4x4/8x8 分区。
    p8x8/p4x4：分析 inter 宏块的 8x8/4x4 分区。
    b8x8：分析 B 帧的 8x8 分区。
效果：
    启用更多分区（如 i4x4+i8x8+p8x8）：运动估计更精确，压缩效率更高，画质更好，但编码速度显著下降。
    禁用（默认）：编码速度快，适合实时场景，但压缩率较低。
```

#### 8.3.2 **aud**

```
含义：是否在码流中插入 AU（Access Unit，访问单元）分隔符，用于标识帧的边界。
默认值：true（启用）。
效果：
    true：提高码流的容错性和解码器同步能力，适合流媒体传输（如 RTSP），但增加微小码率开销。
    false：无 AU 分隔符，码流更紧凑，适合本地存储（如 MP4 封装）。
```

#### 8.3.3 **b-adapt**

```
含义：是否自动调整 B 帧数量（根据场景复杂度动态决定）。
默认值：true（启用自动调整）。
效果：
    true：复杂场景减少 B 帧（避免画质损失），简单场景增加 B 帧（提高压缩率），平衡质量和效率。
    false：固定使用 bframes 设定的数量，适合需要严格控制延迟的场景（如视频会议）。
```

#### 8.3.4 **b-pyramid**

```
含义：是否将部分 B 帧作为参考帧（形成 “B 帧金字塔” 结构）。
默认值：false（禁用）。
效果：
    true：提升压缩效率和画质（B 帧可被后续帧参考），但增加编码复杂度和解码延迟，不适合实时场景。
    false：B 帧不作为参考，编码速度快，延迟低，适合直播。
```

#### 8.3.5 **bframes**

```
含义：I 帧和 P 帧之间插入的 B 帧数量（B 帧压缩率高，但依赖前后帧，延迟较大）。
默认值：0（无 B 帧）。
范围：0~16。
效果：
    增大值（如 3）：压缩率提升（文件更小），画质更好，但编码延迟增加，解码复杂度提高。
    设为 0：无 B 帧，延迟低，适合实时编码（如监控直播），但码率更高。
```

#### 8.3.6 **bitrate**

```
含义：目标比特率（单位：kbit / 秒），决定视频质量和码流大小的核心参数。
默认值：2048（2 Mbps）。
范围：1~2048000。
效果：
    过高（如 10000 kbps）：画质细腻，但文件大、带宽占用高，适合 4K 存储。
    过低（如 512 kbps）：文件小，但可能出现块效应、模糊，适合低带宽传输（如移动端）。
建议：1080p 30fps 建议 2~8 Mbps，720p 建议 1~4 Mbps。
```

#### 8.3.7 **byte-stream**

```
含义：是否生成 Annex B 字节流格式（NALU 前添加起始码 0x000001 或 0x00000001）。
默认值：false（生成原始 NALU 格式）。
效果：
    true：兼容多数播放器（VLC、FFmpeg）和流媒体协议（RTSP、HLS），推荐用于传输。
    false：适合 MP4、MKV 等容器封装（需配合 h264parse 处理），码流更紧凑。
```

#### 8.3.8 **cabac**

```
含义：是否启用 CABAC（基于上下文的自适应二进制算术编码）熵编码。
默认值：true（启用）。
效果：
    true：比 CAVLC 熵编码节省 10~15% 码率，压缩效率更高，但编码速度慢。
    false：使用 CAVLC，编码速度快，适合低端设备或实时场景，但码率更高。
```

#### 8.3.9 **dct8x8**

```
含义：是否启用 8x8 离散余弦变换（DCT），用于提高高频细节的压缩效率。
默认值：false（禁用）。
效果：
    true：提升纹理丰富区域（如 foliage）的画质，压缩率更高，但编码复杂度增加（仅在 high 及以上 profile 支持）。
    false：仅使用 4x4 DCT，速度快，适合 baseline profile。
```

#### 8.3.10 **frame-packing**

```
含义：立体视频（3D）的帧打包模式（如左右眼视图排列方式）。
默认值：-1（auto，自动继承输入视频的打包模式）。
枚举值：包括棋盘格、行列交错、左右并排等，用于 3D 视频编码，普通 2D 场景无需修改。
```

#### 8.3.11 **insert-vui**

```
含义：是否在码流中插入 VUI（视频使用信息）NALU，包含分辨率、帧率、宽高比等元数据。
默认值：true（启用）。
效果：
    true：解码器可直接获取视频参数，避免解析错误，推荐启用。
    false：不插入 VUI，码流略小，但解码器需依赖外部参数（如容器信息）。
```

#### 8.3.12 **interlaced**

```
含义：是否按隔行扫描模式编码（适用于传统电视信号）。
默认值：false（逐行扫描）。
效果：
    true：适合隔行输入（如 PAL/NTSC 电视信号），避免运动模糊。
    false：默认逐行模式，适合现代视频（如网络视频、电影）。
```

#### 8.3.13 **intra-refresh**

```
含义：是否使用周期性 intra 刷新（而非 IDR 帧）更新画面，避免大尺寸关键帧。
默认值：false（禁用）。
效果：
    true：码率波动小，适合低带宽场景（如视频会议），但随机访问能力下降（seek 速度慢）。
    false：使用 IDR 帧作为关键帧，seek 速度快，适合点播场景。
```

#### 8.3.14 **ip-factor**

```
含义：I 帧与 P 帧的量化系数比例（控制 I 帧相对 P 帧的质量）。
默认值：1.4（I 帧量化值为 P 帧的 1.4 倍，即 I 帧质量更高）。
范围：0~2。
效果：
    增大值（如 1.8）：I 帧质量更高（更清晰），但码率增加。
    减小值（如 1.0）：I 帧与 P 帧质量接近，码率降低，但画面稳定性下降。
```

#### 8.3.15 **key-int-max**

```
含义：最大关键帧（I 帧）间隔（单位：帧），决定视频的随机访问能力。
默认值：0（自动计算，通常为帧率的 2~4 倍，如 30fps 对应 60~120 帧）。
效果：
    减小值（如 30）：关键帧密集，seek 速度快，适合点播，但码率高。
    增大值（如 300）：关键帧稀疏，码率低，但 seek 延迟大，适合直播。
```

#### 8.3.16 **mb-tree**

```
含义：是否启用宏块树（Macroblock-Tree）码率控制，动态调整宏块量化参数。
默认值：true（启用）。
效果：
    true：提升主观画质（重点区域分配更多码率），压缩效率更高，但编码速度下降。
    false：关闭动态调整，速度快，适合实时场景。
```

#### 8.3.17 **me**

```
含义：整数像素运动估计算法（影响运动矢量精度和编码速度）。
默认值：1（hex，六边形搜索）。
枚举值（从快到慢，精度递增）：
    dia（菱形搜索）：最快，精度最低。
    hex（六边形搜索）：平衡速度和精度（默认）。
    umh（非对称多六边形）：精度高，速度慢。
    esa/tesa： exhaustive 搜索，精度最高，速度极慢（适合离线编码）。	
```

#### 8.3.18 **multipass-cache-file**

```
含义：多遍编码（pass1/pass2）时的缓存文件路径，用于存储第一遍的分析数据。
默认值："x264.log"。
效果：多遍编码通过该文件优化码率分配，提升压缩效率，仅用于离线场景。
```

#### 8.3.19 **noise-reduction**

```
含义：降噪强度（减少视频噪声，间接提升压缩率）。
默认值：0（无降噪）。
范围：0~100000。
效果：
    增大值（如 10000）：减少噪声，压缩率提升，但可能模糊细节（适合低光、高噪视频）。
    设为 0：保留原始细节，适合高质量视频。
```

#### 8.3.20 **option-string**

```
含义：直接传递给 libx264 的原始参数字符串（格式：key1=value1:key2=value2），优先级高于插件属性。
默认值：""（空）。
用途：高级用户可通过此参数设置插件未暴露的 libx264 选项（如 "crf=23:scenecut=40"）。
```

#### 8.3.21 **pass**

```
含义：编码模式（单遍 / 多遍），决定码率控制方式。
默认值：0（cbr，恒定比特率）。
枚举值：
    cbr：码率恒定，适合固定带宽场景（如广播电视），但复杂场景可能画质下降。
    quant：恒定量化参数（QP），画质均匀，码率波动大，适合对画质一致性要求高的场景。
    qual：恒定质量模式（CRF），码率自适应场景，适合存储（推荐）。
    pass1/pass2：多遍编码，压缩效率最高，不支持实时。
```

#### 8.3.22 **pb-factor**

```
含义：P 帧与 B 帧的量化系数比例（控制 P 帧相对 B 帧的质量）。
默认值：1.3（P 帧质量高于 B 帧）。
范围：0~2。
效果：类似 ip-factor，调整 P/B 帧质量分配，平衡码率和画质。
```

#### 8.3.23 **psy-tune**

```
含义：针对特定内容的心理视觉优化（提升主观画质）。
默认值：0（none，无优化）。
枚举值：
    film：优化电影内容（减少块效应）。
    animation：优化动画（保留锐利边缘）。
    grain：保留胶片颗粒感。
    psnr/ssim：优先优化客观指标（PSNR/SSIM）。
```

#### 8.3.24 **qos**

```
含义：是否处理下游的 QoS 事件（如丢帧请求）。
默认值：false（不处理）。
效果：
    true：响应下游丢帧指令，降低延迟，适合实时场景，但可能影响画质连续性。
    false：按顺序编码所有帧，保证完整，但延迟可能增加。
```

#### 8.3.25 **qp-max / qp-min / qp-step**

```
含义：量化参数（QP）的最大 / 最小限制，以及帧间 QP 最大差值（QP 越小，画质越好，码率越高）。
默认值：qp-max=51，qp-min=10，qp-step=4。
效果：限制 QP 范围避免画质波动过大，qp-step 控制帧间质量变化平滑度。
```

#### 8.3.26 **quantizer**

```
含义：恒定量化模式（pass=quant）下的量化参数，或恒定质量模式（pass=qual）下的质量值。
默认值：21（中等质量）。
范围：0~50（值越小，画质越好）。
```

#### 8.3.27 **rc-lookahead**

```
含义：码率控制的前瞻帧数（分析未来帧以优化当前帧码率分配）。
默认值：40。
范围：0~250。
效果：
    增大值（如 100）：码率分配更优，画质更稳定，但延迟增加（适合离线）。
    减小值（如 10）：延迟降低，适合实时场景。
```

#### 8.3.28 **ref**

```
含义：参考帧数量（编码器用于运动补偿的历史帧数）。
默认值：1。
范围：1~12。
效果：
    增大值（如 4）：运动补偿更精确，画质和压缩率提升，但编码速度下降，解码器内存需求增加。
    减小值（如 1）：速度快，适合实时场景。
```

#### 8.3.29 **sliced-threads**

```
含义：是否使用切片线程（sliced threading）模式（将帧分割为切片并行编码）。
默认值：false（使用帧级线程）。
效果：
    true：延迟低（切片级并行），但压缩效率下降，适合实时低延迟场景（如视频会议）。
    false：帧级并行，压缩效率高，适合离线编码。
```

#### 8.3.30 **speed-preset**

```
含义：速度与质量的权衡预设（核心参数之一）。
默认值：6（medium）。
枚举值（从快到慢）：ultrafast → superfast → ... → veryslow → placebo。
效果：越慢的预设压缩效率越高（画质更好、码率更低），但编码耗时越长。
```

#### 8.3.31 **sps-id**

```
含义：SPS（序列参数集）和 PPS（图像参数集）的 ID 号（多流场景用于区分参数集）。
默认值：0。
范围：0~31。
用途：多路 H.264 流复用时常用于区分不同参数集，单流场景无需修改。
```

#### 8.3.32 **subme**

```
含义：亚像素运动估计和分区决策的质量等级（1 = 最快，10 = 最佳）。
默认值：1。
效果：
    增大值（如 7）：运动估计更精确，画质提升，但编码速度显著下降。
    减小值（如 1）：速度快，适合实时场景。
```

#### 8.3.33 **sync-lookahead**

```
含义：线程化前瞻的缓冲帧数（配合多线程编码优化码率控制）。
默认值：-1（自动）。
范围：-1~250。
效果：调整多线程下的前瞻缓冲，平衡速度和码率控制精度。
```

#### 8.3.34 **threads**

```
含义：编码线程数（0 表示自动根据 CPU 核心数分配）。
默认值：0。
效果：
    增大值（如 4）：多线程并行加速，适合多核 CPU，但可能增加码率波动。
    设为 1：单线程编码，码率更稳定，速度慢。
```

#### 8.3.35 **trellis**

```
含义：是否启用网格搜索量化（trellis quantization），优化残差编码。
默认值：true（启用）。
效果：
    true：减少高频噪声，提升画质，压缩率更高，但编码速度下降。
    false：关闭优化，速度快，适合实时场景。
```

#### 8.3.36 **tune**

```
含义：非心理视觉的场景优化（可组合多个 flag）。
默认值：0x00000000（(none)）。
Flags 选项：
    stillimage：优化静态图像（如幻灯片）。
    fastdecode：限制高级特性，提升解码速度（适合低端设备）。
    zerolatency：零延迟模式（禁用 B 帧、减少参考帧），适合实时交互（如视频会议）。
```

#### 8.3.37 **vbv-buf-capacity**

```
含义：VBV（视频缓冲区验证器）缓冲区大小（单位：毫秒），控制码率波动范围。
默认值：600（600ms）。
效果：
    增大值（如 1000）：允许更大码率波动，复杂场景画质更好，适合存储。
    减小值（如 300）：码率更平稳，适合固定带宽传输（如直播）。
```

#### 8.3.38 **weightb**

```
含义：是否对 B 帧启用加权预测（提升 B 帧质量）。
默认值：false（禁用）。
效果：
    true：B 帧质量提升，压缩率更高，但编码复杂度增加，适合离线场景。
    false：禁用加权预测，速度快，适合实时。
```

### 8.4 总结

```
x264enc 的属性可分为核心控制（bitrate、speed-preset、tune、pass）和高级优化（ref、bframes、me 等）。配置时需根据场景权衡：
    实时场景（直播 / 监控）：优先低延迟，选 speed-preset=ultrafast、tune=zerolatency、bframes=0、ref=1。
    离线存储：优先质量和压缩率，选 speed-preset=slow、pass=qual、bframes=3、ref=4。
    平衡场景：默认 medium 预设 + 合理比特率，兼顾速度和质量。
```

## 9.h264parse

### 9.1 插件介绍

```

```

### 9.2 命令查看

```
命令：
	gst-inspect-1.0 h264parse
输出：
Factory Details:
  Rank                     primary + 1 (257)
  Long-name                H.264 parser
  Klass                    Codec/Parser/Converter/Video
  Description              Parses H.264 streams
  Author                   Mark Nauwelaerts <mark.nauwelaerts@collabora.co.uk>

Plugin Details:
  Name                     videoparsersbad
  Description              videoparsers
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstvideoparsersbad.so
  Version                  1.16.3
  License                  LGPL
  Source module            gst-plugins-bad
  Source release date      2020-10-21
  Binary package           GStreamer Bad Plugins (Ubuntu)
  Origin URL               https://launchpad.net/distros/ubuntu/+source/gst-plugins-bad1.0

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseParse
                         +----GstH264Parse

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-h264
                 parsed: true
          stream-format: { (string)avc, (string)avc3, (string)byte-stream }
              alignment: { (string)au, (string)nal }
  
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-h264

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  config-interval     : Send SPS and PPS Insertion Interval in seconds (sprop parameter sets will be multiplexed in the data stream when detected.
) (0 = disabled, -1 = send with every IDR frame)
                        flags: readable, writable
                        Integer. Range: -1 - 3600 Default: 0 
  disable-passthrough : Force processing (disables passthrough)
                        flags: readable, writable
                        Boolean. Default: false
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "h264parse0"
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
```

### 9.3 参数讲解

#### 9.3.1 `config-interval`

```
含义：设置 SPS（序列参数集）和 PPS（图像参数集）的插入间隔（单位：秒）。SPS 和 PPS 是 H.264 编码中描述视频序列和图像属性的关键元数据，
	 解码器必须获取这些数据才能正确解码。
取值范围：-1、0 或 1-3600（秒）。
默认值：0。
不同取值的效果与优缺点：
0（默认）：禁用主动插入 SPS/PPS，仅在解析到流中已有的 SPS/PPS 时传递。
        优点：减少数据冗余，适合已知解码器已缓存 SPS/PPS 的场景（如本地文件播放）。
        缺点：若解码器未缓存或丢失 SPS/PPS（如网络传输中断后重连），会导致解码失败。
-1：每次遇到 IDR 帧（即时解码刷新帧，可作为视频序列起点）时插入 SPS/PPS。
    优点：确保解码器在关键帧处总能获取元数据，适合网络流（如 RTSP/RTMP），抗丢包能力强。
    缺点：增加数据量（SPS/PPS 随每个 IDR 帧重复发送），可能略微增加带宽占用。
N（1-3600 秒）：每 N 秒强制插入一次 SPS/PPS（即使没有 IDR 帧）。
    优点：平衡冗余和可靠性，适合对延迟不敏感但需定期同步元数据的场景（如监控录像回放）。
    缺点：若 N 过大，仍可能出现解码器因元数据丢失而解码失败；若 N 过小，冗余数据过多。
```

#### 9.3.2 `disable-passthrough`

```
含义：强制启用解析功能，禁用 “透传模式”（passthrough）。
取值：true（强制解析）或 false（默认，自动透传）。
透传模式：当输入流已符合 h264parse 输出的规范（如已解析为 AVC 格式、带正确对齐）时，直接转发数据而不重复解析。
不同取值的效果与优缺点：
false（默认）：自动判断是否透传。
    优点：减少不必要的解析计算，提升性能（尤其对已处理过的合规流）。
    缺点：若输入流存在隐性格式问题（如对齐错误），透传可能导致下游元素处理失败。
true：强制解析所有输入流，重新处理格式（如修正 NAL 对齐、补充解析信息）。
    优点：确保输出流严格符合规范，兼容对格式要求严格的下游元素（如硬件解码器）。
    缺点：增加 CPU 占用（重复解析），降低处理效率。
```

#### 9.3.3 `name`

```
含义：设置 h264parse 元素的实例名称（用于 GStreamer 管道中标识元素）。
取值：字符串（默认："h264parse0"，自动编号）。
作用：在复杂管道中区分多个 h264parse 实例（如多流处理），便于调试和日志跟踪。
设置建议：
    无需修改：简单管道中默认名称足够。
    自定义名称：多流场景下（如 h264parse_left、h264parse_right），提升管道可读性。
```

#### 9.3.4 `parent`

```
含义：指定该元素的父对象（GObject 层次结构中的上层容器）。
取值：GstObject 类型的对象（默认：无父对象）。
作用：主要用于 GStreamer 内部对象管理（如内存释放、生命周期关联），一般用户无需手动设置。
使用场景：仅在自定义 GStreamer 插件或复杂对象管理时需要，普通管道配置中可忽略。
```

### 9.4 总结

```
config-interval：核心是平衡 SPS/PPS 冗余与解码可靠性，网络流建议设为 -1，本地文件可用默认 0。
disable-passthrough：默认 false 优先保证性能，下游元素报错时再设为 true 强制修正格式。
name 和 parent：主要用于标识和内部管理，普通场景无需修改。
```

## 10.rtph264pay

### 10.1 插件介绍

```

```

### 10.2 命令查看

```
命令：
	gst-inspect-1.0 rtph264pay
输出：
Factory Details:
  Rank                     secondary (128)
  Long-name                RTP H264 payloader
  Klass                    Codec/Payloader/Network/RTP
  Description              Payload-encode H264 video into RTP packets (RFC 3984)
  Author                   Laurent Glayal <spglegle@yahoo.fr>

Plugin Details:
  Name                     rtp
  Description              Real-time protocol plugins
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstrtp.so
  Version                  1.16.3
  License                  LGPL
  Source module            gst-plugins-good
  Source release date      2020-10-21
  Binary package           GStreamer Good Plugins (Ubuntu)
  Origin URL               https://launchpad.net/distros/ubuntu/+source/gst-plugins-good1.0

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstRTPBasePayload
                         +----GstRtpH264Pay

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      application/x-rtp
                  media: video
                payload: [ 96, 127 ]
             clock-rate: 90000
          encoding-name: H264
  
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-h264
          stream-format: avc
              alignment: au
      video/x-h264
          stream-format: byte-stream
              alignment: { (string)nal, (string)au }

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SRC: 'src'
    Pad Template: 'src'
  SINK: 'sink'
    Pad Template: 'sink'

Element Properties:
  config-interval     : Send SPS and PPS Insertion Interval in seconds (sprop parameter sets will be multiplexed in the data stream when detected.
) (0 = disabled, -1 = send with every IDR frame)
                        flags: readable, writable
                        Integer. Range: -1 - 3600 Default: 0 
  max-ptime           : Maximum duration of the packet data in ns (-1 = unlimited up to MTU)
                        flags: readable, writable
                        Integer64. Range: -1 - 9223372036854775807 Default: -1 
  min-ptime           : Minimum duration of the packet data in ns (can't go above MTU)
                        flags: readable, writable
                        Integer64. Range: 0 - 9223372036854775807 Default: 0 
  mtu                 : Maximum size of one packet
                        flags: readable, writable
                        Unsigned Integer. Range: 28 - 4294967295 Default: 1400 
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "rtph264pay0"
  onvif-no-rate-control: Enable ONVIF Rate-Control=no timestamping mode
                        flags: readable, writable
                        Boolean. Default: false
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  perfect-rtptime     : Generate perfect RTP timestamps when possible
                        flags: readable, writable
                        Boolean. Default: true
  pt                  : The payload type of the packets
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 127 Default: 96 
  ptime-multiple      : Force buffers to be multiples of this duration in ns (0 disables)
                        flags: readable, writable
                        Integer64. Range: 0 - 9223372036854775807 Default: 0 
  seqnum              : The RTP sequence number of the last processed packet
                        flags: readable
                        Unsigned Integer. Range: 0 - 65535 Default: 0 
  seqnum-offset       : Offset to add to all outgoing seqnum (-1 = random)
                        flags: readable, writable
                        Integer. Range: -1 - 65535 Default: -1 
  source-info         : Write CSRC based on buffer meta RTP source information
                        flags: readable, writable
                        Boolean. Default: false
  sprop-parameter-sets: The base64 sprop-parameter-sets to set in out caps (set to NULL to extract from stream)
                        flags: readable, writable, deprecated
                        String. Default: null
  ssrc                : The SSRC of the packets (default == random)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 4294967295 
  stats               : Various statistics
                        flags: readable
                        Boxed pointer of type "GstStructure"
                                                          clock-rate: 0
                                                        running-time: 18446744073709551615
                                                              seqnum: 0
                                                           timestamp: 0
                                                                ssrc: 0
                                                                  pt: 96
                                                       seqnum-offset: 0
                                                     timestamp-offset: 0

  timestamp           : The RTP timestamp of the last processed packet
                        flags: readable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 0 
  timestamp-offset    : Offset to add to all outgoing timestamps (default = random)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 4294967295
```

### 10.3 参数讲解

#### 10.3.1 `config-interval`

```
含义：设置 SPS（序列参数集）和 PPS（图像参数集）在 RTP 流中的插入间隔（单位：秒）。SPS/PPS 是 H.264 解码必需的元数据，
	 通过 RTP 流中的 sprop-parameter-sets 字段传递。
取值范围：-1、0 或 1-3600（秒），默认值 0。
不同取值的效果与优缺点：
0（默认）：仅在初始协商时发送一次 SPS/PPS，后续不再主动插入。
    优点：减少冗余数据，节省带宽，适合解码器已稳定缓存 SPS/PPS 的场景（如长连接且编码参数不变）。
    缺点：若解码器中途丢失 SPS/PPS（如网络中断重连），会导致解码失败，可靠性低。
-1：每次发送 IDR 帧（关键帧）时强制插入 SPS/PPS。
    优点：确保解码器在关键帧处总能获取元数据，极大提升网络流（如 RTSP/webrtc）的抗丢包能力和重连恢复速度。
    缺点：增加带宽占用（SPS/PPS 随每个 IDR 帧重复发送），对低带宽场景不友好。
N（1-3600 秒）：每 N 秒强制插入一次 SPS/PPS（即使无 IDR 帧）。
    优点：平衡冗余和可靠性，适合编码参数可能动态变化（如分辨率调整）或需定期同步的场景（如监控直播）。
    缺点：N 过大会降低可靠性，N 过小会增加带宽开销。
```

#### 10.3.2 `max-ptime`

```
含义：单个 RTP 包承载的 H.264 数据的最大时长（单位：纳秒，1ns=1e-9秒），超过此值会拆分数据。
取值范围：-1（无限制，仅受 MTU 约束）或 0-9e18，默认 -1。
效果与优缺点：
-1（默认）：仅按 MTU 限制拆分，不限制数据时长。
    优点：减少拆分次数，降低协议开销，适合大码率、高帧率视频（如 4K/60fps）。
    缺点：若单帧数据过大（如复杂场景的 I 帧），可能导致 RTP 包过大，增加网络传输丢包风险。
N（自定义时长）：强制限制单包数据时长（如 40000000ns=40ms）。
    优点：控制单包数据量，避免超大帧导致的网络拥塞，适合低带宽或不稳定网络（如无线传输）。
    缺点：可能增加拆分次数，引入更多 RTP 头部开销，降低传输效率。
```

#### 10.3.3 `min-ptime`

```
含义：单个 RTP 包承载的 H.264 数据的最小时长（单位：纳秒），低于此值会合并数据。
取值范围：0-9e18，默认 0（不限制，即允许任意小的时长）。
效果与优缺点：
0（默认）：不合并小数据帧，直接封装为 RTP 包。
    优点：低延迟，适合实时交互场景（如视频会议）。
    缺点：若存在大量小帧（如低复杂度场景的 P 帧），会生成大量小 RTP 包，增加协议开销和网络负担。
N（自定义时长）：合并短时数据帧，直到达到 N 时长再封装。
    优点：减少 RTP 包数量，降低协议开销，适合对带宽敏感但延迟容忍度较高的场景（如安防录像传输）。
    缺点：增加延迟（需等待数据合并），不适合实时交互。
```

#### 10.3.4 `mtu`

```
含义：单个 RTP 包的最大字节数（含 RTP 头部），即网络最大传输单元（MTU）限制。
取值范围：28-4294967295（字节），默认 1400。
效果与优缺点：
默认 1400：适配多数网络（以太网 MTU 为 1500，减去 IP+UDP 头部约 100 字节）。
	优点：兼容主流网络，避免数据包被分片（分片会增加丢包风险和解码复杂度）。
调大（如 1460）：
    优点：单包承载更多数据，减少包数量，提升传输效率，适合局域网等 MTU 较大的环境。
    缺点：可能超过部分网络的 MTU 限制，导致数据包被分片或丢弃。
调小（如 1000）：
    优点：降低单包大小，适合高丢包率网络（如 4G/5G 无线传输），丢包后影响范围更小。
    缺点：增加包数量和协议开销，降低传输效率。
```

#### 10.3.5 `name`

```
含义：设置 rtph264pay 元素的实例名称，用于在 GStreamer 管道中标识元素。
取值：字符串，默认 rtph264pay0（自动编号）。
作用：在多流处理等复杂管道中（如同时传输多路 H.264 视频），通过自定义名称（如 rtp_pay_cam1、rtp_pay_cam2）区分不同实例，便于调试和日志跟踪。普通场景无需修改。
```

#### 10.3.6 `onvif-no-rate-control`

```
含义：启用 ONVIF 协议中的 “无速率控制”（Rate-Control=no）时间戳模式。
取值：true/false，默认 false。
效果：
	ONVIF 设备（如网络摄像头）在该模式下，时间戳仅反映帧捕获顺序，不严格对应实际时间间隔。
    true：适配 ONVIF 设备的特殊时间戳格式，确保接收端正确同步。
    false：使用标准 RTP 时间戳（基于 90kHz 时钟，反映实际时间），适合非 ONVIF 场景。
```

#### 10.3.7 `perfect-rtptime`

```
含义：尽可能生成 “完美” 的 RTP 时间戳（严格按 90kHz 时钟递增，与帧间隔精确匹配）。
取值：true/false，默认 true。
效果与优缺点：
true（默认）：时间戳精准，确保接收端平滑播放（无卡顿或跳帧），适合实时视频流。
	缺点：若输入帧的时间戳本身不精准（如编码器时钟漂移），可能导致修正后的时间戳与实际帧间隔不一致。
false：直接使用输入帧的时间戳（不修正），适合对原始时间戳敏感的场景（如离线文件打包）。
	缺点：时间戳可能不连续，导致接收端播放卡顿。
```

#### 10.3.8 `pt`

```
含义：RTP 包的负载类型（Payload Type），用于标识 payload 格式（此处固定为 H.264）。
取值范围：0-127，默认 96（动态负载类型，需通过 SDP 协商）。
效果：
    标准协议中，96-127 为动态负载类型，需在会话协商（如 SDP）中指定对应编码（H.264）。
    若修改为其他值（如 97），需确保发送端与接收端协商一致，否则接收端无法识别 payload 格式。
```

#### 10.3.9 `ptime-multiple`

```
含义：强制 RTP 包承载的数据时长为该值的整数倍（单位：纳秒），0 表示禁用。
取值范围：0-9e18，默认 0。
效果：用于对齐数据时长（如强制按 20ms 倍数打包），确保接收端时钟同步更简单。仅在对时间精度有特殊要求的场景（如广播电视）需设置，普通场景建议保持 0。
```

#### 10.3.10 `seqnum` / `seqnum-offset`

```
seqnum：只读属性，记录最后发送的 RTP 包的序列号（范围 0-65535，循环递增），用于调试丢包或乱序问题。
seqnum-offset：设置序列号偏移量（-1 表示随机偏移），默认 -1。
作用：避免多流场景下序列号冲突（如多路 RTP 流在同一网络传输），增强安全性（防止序列号预测攻击）。
```

#### 10.3.11 `source-info`

```
含义：是否基于缓冲区元数据中的 RTP 源信息写入 CSRC（贡献源列表）。
取值：true/false，默认 false。
作用：CSRC 用于标识多个源对当前 RTP 包的贡献（如混音场景），普通单源流无需启用，多源流合并时设为 true。
```

#### 10.3.12 `sprop-parameter-sets`（已废弃）

```
含义：手动设置 base64 编码的 SPS/PPS（替代从流中自动提取），已被 config-interval 替代。
建议：无需设置，保持默认 null 即可，由元素自动从输入流中提取 SPS/PPS。
```

#### 10.3.13 `ssrc`

```
含义：RTP 包的同步源标识符（SSRC），用于接收端区分不同流，默认 4294967295（随机生成）。
效果：多流场景下需手动设置不同 SSRC（如 12345、67890），避免冲突；单流场景保持默认随机即可。
```

#### 10.3.14 `stats`

```
含义：只读属性，记录 RTP 流的统计信息（如时钟频率、序列号、时间戳、SSRC 等），用于调试和监控（如通过 gst-inspect-1.0 或代码查询）
```

#### 10.3.15 `timestamp` / `timestamp-offset`

```
timestamp：只读属性，记录最后发送的 RTP 包的时间戳（基于 90kHz 时钟）。
timestamp-offset：设置时间戳偏移量（默认随机），用于多流同步或避免时间戳冲突，普通场景无需修改。
```

### 10.4 总结

```
核心属性：config-interval（可靠性）、mtu（网络适配）、max-ptime/min-ptime（包大小与延迟平衡）是配置重点。
网络流建议：config-interval=-1（确保 SPS/PPS 随 IDR 帧发送）、mtu=1400（兼容主流网络）、perfect-rtptime=true（平滑播放）。
特殊场景：ONVIF 设备需启用 onvif-no-rate-control=true；多流传输需自定义 name、ssrc、seqnum-offset 避免冲突。
```

## 11.udpsink

### 11.1 插件介绍

```

```

### 11.2 命令查看

```
命令：
	gst-inspect-1.0 udpsink
输出：
Factory Details:
  Rank                     none (0)
  Long-name                UDP packet sender
  Klass                    Sink/Network
  Description              Send data over the network via UDP
  Author                   Wim Taymans <wim@fluendo.com>

Plugin Details:
  Name                     udp
  Description              transfer data via UDP
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstudp.so
  Version                  1.16.3
  License                  LGPL
  Source module            gst-plugins-good
  Source release date      2020-10-21
  Binary package           GStreamer Good Plugins (Ubuntu)
  Origin URL               https://launchpad.net/distros/ubuntu/+source/gst-plugins-good1.0

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseSink
                         +----GstMultiUDPSink
                               +----GstUDPSink

Implemented Interfaces:
  GstURIHandler

Pad Templates:
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      ANY

Element has no clocking capabilities.

URI handling capabilities:
  Element can act as sink.
  Supported URI protocols:
    udp

Pads:
  SINK: 'sink'
    Pad Template: 'sink'

Element Properties:
  async               : Go asynchronously to PAUSED
                        flags: readable, writable
                        Boolean. Default: true
  auto-multicast      : Automatically join/leave the multicast groups, FALSE means user has to do it himself
                        flags: readable, writable
                        Boolean. Default: true
  bind-address        : Address to bind the socket to
                        flags: readable, writable
                        String. Default: null
  bind-port           : Port to bind the socket to
                        flags: readable, writable
                        Integer. Range: 0 - 65535 Default: 0 
  blocksize           : Size in bytes to pull per buffer (0 = default)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 4096 
  buffer-size         : Size of the kernel send buffer in bytes, 0=default
                        flags: readable, writable
                        Integer. Range: 0 - 2147483647 Default: 0 
  bytes-served        : Total number of bytes sent to all clients
                        flags: readable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0 
  bytes-to-serve      : Number of bytes received to serve to clients
                        flags: readable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0 
  clients             : A comma separated list of host:port pairs with destinations
                        flags: readable, writable
                        String. Default: "localhost:5004"
  close-socket        : Close socket if passed as property on state change
                        flags: readable, writable
                        Boolean. Default: true
  enable-last-sample  : Enable the last-sample property
                        flags: readable, writable
                        Boolean. Default: true
  force-ipv4          : Forcing the use of an IPv4 socket (DEPRECATED, has no effect anymore)
                        flags: readable, writable, deprecated
                        Boolean. Default: false
  host                : The host/IP/Multicast group to send the packets to
                        flags: readable, writable
                        String. Default: "localhost"
  last-sample         : The last sample received in the sink
                        flags: readable
                        Boxed pointer of type "GstSample"
  loop                : Used for setting the multicast loop parameter. TRUE = enable, FALSE = disable
                        flags: readable, writable
                        Boolean. Default: true
  max-bitrate         : The maximum bits per second to render (0 = disabled)
                        flags: readable, writable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0 
  max-lateness        : Maximum number of nanoseconds that a buffer can be late before it is dropped (-1 unlimited)
                        flags: readable, writable
                        Integer64. Range: -1 - 9223372036854775807 Default: -1 
  multicast-iface     : The network interface on which to join the multicast group
                        flags: readable, writable
                        String. Default: null
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "udpsink0"
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  port                : The port to send the packets to
                        flags: readable, writable
                        Integer. Range: 0 - 65535 Default: 5004 
  processing-deadline : Maximum processing deadline in nanoseconds
                        flags: readable, writable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 20000000 
  qos                 : Generate Quality-of-Service events upstream
                        flags: readable, writable
                        Boolean. Default: false
  qos-dscp            : Quality of Service, differentiated services code point (-1 default)
                        flags: readable, writable
                        Integer. Range: -1 - 63 Default: -1 
  render-delay        : Additional render delay of the sink in nanoseconds
                        flags: readable, writable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0 
  send-duplicates     : When a distination/port pair is added multiple times, send packets multiple times as well
                        flags: readable, writable
                        Boolean. Default: true
  socket              : Socket to use for UDP sending. (NULL == allocate)
                        flags: readable, writable
                        Object of type "GSocket"
  socket-v6           : Socket to use for UDPv6 sending. (NULL == allocate)
                        flags: readable, writable
                        Object of type "GSocket"
  sync                : Sync on the clock
                        flags: readable, writable
                        Boolean. Default: true
  throttle-time       : The time to keep between rendered buffers (0 = disabled)
                        flags: readable, writable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0 
  ts-offset           : Timestamp offset in nanoseconds
                        flags: readable, writable
                        Integer64. Range: -9223372036854775808 - 9223372036854775807 Default: 0 
  ttl                 : Used for setting the unicast TTL parameter
                        flags: readable, writable
                        Integer. Range: 0 - 255 Default: 64 
  ttl-mc              : Used for setting the multicast TTL parameter
                        flags: readable, writable
                        Integer. Range: 0 - 255 Default: 1 
  used-socket         : Socket currently in use for UDP sending. (NULL == no socket)
                        flags: readable
                        Object of type "GSocket"
  used-socket-v6      : Socket currently in use for UDPv6 sending. (NULL == no socket)
                        flags: readable
                        Object of type "GSocket"

Element Signals:
  "client-added" :  void user_function (GstElement* object,
                                        gchararray arg0,
                                        gint arg1,
                                        gpointer user_data);
  "client-removed" :  void user_function (GstElement* object,
                                          gchararray arg0,
                                          gint arg1,
                                          gpointer user_data);

Element Actions:
  "add" :  void user_function (GstElement* object,
                               gchararray arg0,
                               gint arg1);
  "remove" :  void user_function (GstElement* object,
                                  gchararray arg0,
                                  gint arg1);
  "clear" :  void user_function (GstElement* object);
  "get-stats" :  GstStructure* user_function (GstElement* object,
                                               gchararray arg0,
                                               gint arg1);
```

### 11.3 参数讲解



### 11.4 总结

```

```

## 12.queue

### 12.1 插件介绍

```

```

### 12.2 命令查看

```

```

### 12.3 参数讲解



### 12.4 总结

```

```

## 13.待定

### 13.1 插件介绍

```

```

### 13.2 命令查看

```

```

### 13.3 参数讲解



### 13.4 总结

```

```

## 14.待定

### 14.1 插件介绍

```

```

### 14.2 命令查看

```

```

### 14.3 参数讲解



### 14.4 总结

```

```

## 15.待定

### 15.1 插件介绍

```

```

### 15.2 命令查看

```

```

### 15.3 参数讲解



### 15.4 总结

```

```

