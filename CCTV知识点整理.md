## CCTV知识点整理

### 一、流媒体协议

#### 1.1 RTSP 协议

```

```

#### 1.2 RTMP 协议

```

```

#### 1.3 HTTP-FLV 协议

**介绍：**

```
	HTTP-FLV是一种直播流协议，有时候也简称FLV，是在HTTP连接上传输FLV格式的直播流。
	
	和文件下载不同的是，直播流的长度是无限长，或者不确定长度，因此一般是基于HTTP Chunked协议实现。和HTTP-FLV类似的，还有HTTP-TS， 或者HTTP-MP3，TS主要应用于广播电视领域，MP3主要应用于音频领域。

和HLS不同的是，HLS本质上就是HTTP文件下载，而HTTP-FLV本质上是流传输。CDN对于HTTP文件下载的支持很完善，因此HLS的兼容性比HTTP-FLV 要好很多；同样HTTP-FLV的延迟比HLS要低很多，基本上可以做到3的5秒左右延迟，而HLS的延迟一般是8到10秒以上。

从协议实现上看，RTMP和HTTP-FLV几乎一样，RTMP是基于TCP协议，而HTTP-FLV基于HTTP也是TCP协议，因此两者的特点也非常类似。一般推流和 流的生产使用RTMP，主要是因为流的生产设备都支持RTMP；而流的播放和消费端采用HTTP-FLV或者HLS，因为播放设备支持HTTP更完善。

HTTP-FLV的兼容性很好，除了iOS原生浏览器不支持，其他平台和浏览器都支持了，参考MSE。 若需要支持iOS浏览器，你可以考虑使用HLS或者使用WASM；注意一般iOS的Native应用，可以选择使用ijkplayer播放器。
```

#### 1.4 WebRTC 协议

```

```

#### 1.5 HLS 协议

```
HLS是适配性和兼容性最好的流媒体协议，没有之一。这个世界上几乎所有的设备都能支持HLS协议，包括PC、Android、iOS、OTT、SmartTV等等。 各种各样的浏览器对HLS的支持也很好，包括Chrome、Safari、Firefox、Edge等等，包括移动端的浏览器。

如果你的用户群体是多种多样的，特别是设备性能还不太好，那么HLS是最好的选择。如果你希望兼容更多的设备，那么HLS是最好的选择。 如果你希望在任何一个CDN都能分发你的直播流，在全球范围内分发你的直播流，那么HLS是最好的选择。

当然了，HLS并不是没有毛病，它的问题就是延迟比较高，一般在30秒左右。虽然经过优化可以到8秒左右，但是不同播放器的行为可能不一致。 对比起其他流媒体协议，优化后的延迟也很高。因此如果你特别在意直播的延迟，那么请使用RTMP或者 HTTP-FLV协议。

HLS主要的应用场景包括：

跨平台：PC主要的直播方案是HLS，可用hls.js库播放HLS。所以实际上如果选一种协议能跨PC/Android/IOS，那就是HLS。
iOS上苛刻的稳定性要求：iOS上最稳定的当然是HLS，稳定性不差于RTMP和HTTP-FLV的稳定性。
友好的CDN分发方式：HLS分发的基础是HTTP，所以CDN的接入和分发会比RTMP更加完善。HLS能在各种CDN之间切换。
简单问题少：HLS作为流媒体协议非常简单，apple支持得也很完善。Android对HLS的支持也会越来越完善。
HLS协议是SRS的核心协议，将会持续维护和更新，不断完善对HLS协议的支持。SRS将RTMP、SRT或WebRTC流，转换成HLS流。 特别是WebRTC，SRS实现了音频转码的能力。
```

### 二、流媒体服务器

#### 2.1 定义

```

```







参考：

```
网站：https://ossrs.net/lts/zh-cn/docs/v7/doc/http-server
网站：https://info.support.huawei.com/info-finder/encyclopedia/zh/%E7%BB%84%E6%92%AD.html
```

