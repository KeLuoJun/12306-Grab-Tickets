# 12306 抢票助手

## 项目简介

这是一个用于自动抢购12306火车票的Python脚本。通过Selenium库模拟浏览器操作，定时查询并尝试预订指定的车次。抢票成功后会发送邮件通知。
![demo](./data/demo.gif)

## 项目结构

```
.
├── .gitignore
├── readme.md
├── requirements.txt
├── test.ipynb
├── asset/
│   └── chromedriver.exe
├── config/
│   └── settings.py
├── core/
│   ├── by.py
│   └── main.py
├── tests/
└── utils/
    └── sendemail.py
```

### 主要文件说明

- `config/settings.py`: 包含项目的配置信息，如起始站、目的站、购票日期、抢票时间、车次配置等。
- `core/main.py`: 项目的主逻辑文件，负责定时运行购票程序，并在成功或失败时发送邮件提醒。
- `core/by.py`: 抢票逻辑的具体实现，包括登录12306网站、设置Cookie、查询车次、选择乘车人、提交订单等。
- `utils/sendemail.py`: 辅助工具，用于发送邮件通知。

## 环境准备

### 安装依赖

确保你已经安装了以下依赖项：

```bash
pip install -r requirements.txt
```

### 配置ChromeDriver

请确保你的系统中已安装与浏览器版本匹配的 [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) ，并将 `chromedriver.exe` 放置在 `asset/` 目录下。

## 使用方法

1. **修改配置文件**  
   打开 `config/settings.py` 文件，根据需要修改起始站、目的站、购票日期、抢票时间、车次配置等信息。
   其中，起始站和目的站需要的是cookie值，cookie值可以在12306官网的登录页面中获取，`_jc_save_fromStation`为起始站，`_jc_save_toStation`为目的站
   ![车站cookie值获取](./data/cookie.png)

2. **启动抢票程序**

   Windows用户可运行以下命令启动抢票程序：

   ```bash
   python core/main.py
   ```

   Linux用户可运行以下命令启动抢票程序：
   ```bash
   bash run.sh
   ```
   运行后需要在浏览器上扫码登录
   ![扫码登录](./data/login.png)
   

3. **等待抢票结果**  
   程序会在设定的时间执行抢票操作，并在成功或失败时发送邮件通知。
   ![邮件通知](./data/email.jpg)

## 注意事项

- 请确保已正确配置发件人邮箱的授权码。
- 抢票过程中，请勿关闭浏览器窗口，以免影响抢票流程。
- 如果遇到问题，请查看日志文件 `app.log` 获取更多信息。



