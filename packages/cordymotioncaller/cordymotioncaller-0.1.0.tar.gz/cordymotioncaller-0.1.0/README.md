# Motion Caller
# 概述
* cordymotioncaller 是珠海市科迪电子科技有限公司基于 Linux(Ubuntu22.04) 平台的设备驱动运控程序客户端。
* 客户端通过TCP与服务端通信。客户端发送指令，服务端解析指令并执行设备的运动控制，最终将结果返回给客户端。
* 目前cordymotioncaller只支持Linux(Ubuntu22.04)版本。

---
## 主要特点
* cordymotioncaller是C/S架构，实现客户端的指令隔离，使作为客户端的cordymotioncaller实现指令兼容。后续增加新的指令，只需要服务端支持即可，无需修改客户端cordymotioncall


---

## pip 安装
cordymotioncaller已经发布到Pypi官网，通过 pip 指令可以安装。
注意：需要提前在Ubuntu22.04操作系统上安装python(版本3.10)
```
pip install cordymotioncaller
```

验证cordymotioncaller 是否安装成功
```
>>> from cordymotioncaller import MotionCaller
>>> MotionCaller().run_check()
```
输出如下内容:
```
cordymotioncaller installed.
```
表示安装成功

## 示例代码~~~~
```
from cordymotioncaller import MotionCaller  
caller = MotionCaller()                     
print(caller.send_command("127.0.0.1", 8899, "powerondut", 10000)) # 
```
代码说明:
1. from cordymotioncaller import MotionCaller   #导入MotionCaller模块
2. caller = MotionCaller()  #创建MotionCaller对象)
3. caller.send_command("127.0.0.1", 8899, "powerondut", 10000)
    * "127.0.0.1" : 运控服务程序地址，127.0.0.1表示运控服务程序在在本地安装
    * 8899: 服务程序监听端口
    * "powerondut": 运控设备指令，详细指令说明参考下文“指令支持”部分
    * 10000: TCP连接超时，单位(ms)

---
## 指令支持
| version | command    | example                                                |
|---------|------------|--------------------------------------------------------|
| 0.1.0   | powerondut | send_command("127.0.0.1", 8899, "powerondut", 10000)   |
|         |            |                                                        |
