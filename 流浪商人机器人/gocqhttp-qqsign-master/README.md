<p align="center">
    <a href="https://gitee.com/changwenpeng/svipbot" target="_blank" rel="noopener noreferrer">
        <img src="https://q.qlogo.cn/headimg_dl?dst_uin=201088830&spec=5" alt="logo" width="150px"/>
    </a>
</p>
<h1 align="center">gocqhttp-qqsign</h1>
<h2 align="center">不懂加Q群：727289809</h2>
<h2 align="center">另外会 java 开发的可以看我另外的开源项目，<a href="https://gitee.com/changwenpeng/svipbot-demo">基于java实现开发qq机器人</a></h2>

## 介绍：
这是最新的 `go-cqhttp` 版本

这是最新的 `qq-sign` 版本

能帮助您解决 `gocqhttp` 各种登录不上的问题

#### 文件更新日期：<span style="color:green">2023-11-25</span>

## 使用说明

1.  启动qqsign 
    <p><b>Windows</b>: 
        <br>1. 打开cmd窗口进入unidbg-fetch-qsign-1.1.9\bin路径下
        <br>2. 执行：unidbg-fetch-qsign.bash --basePath=C:\Users\chang\Desktop\qq-sign\unidbg-fetch-qsign-1.1.9\txlib\协议版本 </p>
    <p><b>Linux</b>: 
        <br>1. 启动前先配置指定\txlib\协议版本的config.json配置文件配置端口
        <br>2. 建议使用nohup启动, 进入unidbg-fetch-qsign-1.1.9/bin路径下
        <br>3. 执行：nohup ./unidbg-fetch-qsign --basePath=/app/qq-sign/unidbg-fetch-qsign-1.1.9/txlib/协议版本 > nohup.out 2>&1 &
        <br>4. <b>傻瓜式：执行bash.sh文件</b>
    <p>
        
</p>
2.  启动gocqhttp (这个不会就别用了！！！)
    这个需要修改config.xml
    主要就是修改：

```yaml
        sign-servers:
          -url: 'http://127.0.0.1:8080'  # 主签名服务器地址， 必填
```

> 注意: 使用设备签名 8.9.71 较为稳定推荐使用 (可能已经过时)
> 注意: 目前使用设备签名 8.9.80+ 较为稳定推荐使用

### gocqhttp更换版本协议方法

1. 项目 `unidbg-fetch-qsign-1.1.9/txlib/协议版本` 文件夹内有版本协议文件，android_pad.json，android_phone.json 
&nbsp;&nbsp;&nbsp;&nbsp;<br>将这俩文件复制到 `go-cqhttp` 生成的 `data` 文件夹下的 `versions` 文件夹中 
&nbsp;&nbsp;&nbsp;&nbsp;<br>然后改名：android_pad.json需改为gocqhttp对应协议6.json，android_phone.json需改为需改为gocqhttp对应协议1.json
&nbsp;&nbsp;&nbsp;&nbsp;<br>改完名字后路径为：gocqhttp/data/versions/1.json，gocqhttp/data/versions/6.json
2. 更改 `device.json` 文件内 `protocol` 的参数，放进去的是 `1.json` 就改为 `1` 放进去是别的 `x.json` 就改为 `x`, 这里的 `x` 为数字
3. 启动 `qqsign` 
4. 如果失败清空 data 目录并重试, `versions` 文件夹可以保留;


>`device.json` 需要启动一次 `gocqhttp`，会自动生成

## 特别注意

如果你之前使用过gocqhttp 建议将gocqhttp 路径下data文件夹内容删除。