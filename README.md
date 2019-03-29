# 用户登录注册系统项目

基于`python3.6`和`django1.11.7`的登录注册页面

![download](https://img.shields.io/badge/download-2M-green.svg)  ![](https://img.shields.io/badge/bulid-passing-brightgreen.svg)

## 主要功能

- 登录时会添加session，打开新窗口不用再次登录。
- 页面添加验证码功能，输入错误无法登录或注册。
- 注册时需要邮箱验证，通过接受的邮箱连接才可能注册成功。
- 判断用户名和邮箱地址是否存在，若该账号已注册，将不能再次注册。
- 通过bootstrap美化页面，使界面完整充实。
- 添加百度分享组件，实现页面多平台分享功能。
- 使用ajax动态刷新验证码和动态验证功能。
- 增加"抖"按钮，实现页面元素抖动，来源于[coolshell](https://coolshell.cn)。

## 安装

使用pip安装：
`pip install -Ur requirements.txt`

## 配置
配置都是在`settings.py`中，部分邮箱个人信息用example替代了，正式运行时替换成自己的即可。

## 运行
### 创建数据库
由于本项目采用mysql数据库存储数据，所以需要在运行前进行创建数据库操作
```
CREATE DATABASE 'mysite' DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```
并修改配置文件中数据库的账号与密码等设置
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456'
    }
}
```
数据库创建和修改好后，要进行数据库迁移操作，在终端进入到项目路径后执行
```
python manage.py makemigrations
python manage.py migrate
```
### 创建超级用户
在项目目录路径下的终端输入
```
python manage.py createsuperuser
```
超级用户的密码不能过于简单，否则无法通过

### 开始运行
```
python manage.py runserver 
```
## 问题相关
有任何问题欢迎提Issue，或者将问题描述发送至我的邮箱`welisit#qq.com`.我会尽快解答，推荐提交Issue方式。
***
## 致大家:raising_hand_man: :raising_hand_woman:
本项目是我做的第一个django练习项目，可能当中有很多还不完善的地方，但我希望能够通过大家的努力让这个项目变得更加美好。
:bow: :bow: 
