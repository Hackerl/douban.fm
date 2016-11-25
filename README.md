# ![](art/logo.jpg) doubanfm-py

![](https://img.shields.io/badge/python-2.7%2B%2C%203.3%2B-blue.svg)

**豆瓣 FM -- Python** 频道播放器。你需要事先安装  `requests`、`urwid` 库，以及安装 [mpg123](http://www.mpg123.de/) / [mplayer](http://mplayerhq.hu/design7/news.html) / [mpv](http://mpv.io/) 三款命令行播放器中的其中一款。

**Finally，使用 `./fm.py` 命令启动程式**。*（暂不支持运行在 Windows 下）*
## 更新
- 频道收听
- 红心、取消红心

## 截图
![](art/screenshot.png)

## 按键
- **`m`：** 切换循环模式
- **`↑`、`↓`、`j`、`k`：** 上下移动光标
- **`PageUp`、`PageDown`：** 上下翻页
- **`Enter`、`Space`：** 播放所选曲目
- **`←`、`→`：** 播放上一曲、下一首曲目
- **`q`、`Esc`：** 退出程式
- **`l`、`L`：** 红心、取消红心，注意正在播放歌曲后面红心，代表红心状态

##设置
- 在fm.cfg中填写邮箱、密码cookie
- cookie为登录豆瓣后取得的cookie，需要自行设置，因为cookie获取api还在开发中，请见谅!

##参考
- https://github.com/nekocode/doubanfm-py
