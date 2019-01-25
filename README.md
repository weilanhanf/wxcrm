# wxcrm

河南省某高级中学校园管理系统样例，基于<code>python3.5</code>和<code>Django2.0</code>


## 功能简介：

- 登录注册：普通用户与管理人员入口不同，老师及学生通过状态选择验证。
- 权限管理：权限组管理及个人权限管理。
- 基本信息管理：针对用户（学生，老师，年级主任，管理人员）基本信息的增删改查。
- 年级管理：年级与年级主任，该年级下属的班级关联。
- 班级管理：班级与班级主任，授课老师，该班级所有的学生，统计学生数，按老师筛选班级。
- 宿舍管理：宿舍责任老师，宿舍长，以及当前宿舍学生。
- 考试管理：考试记录的建立。
- 成绩管理：成绩排名，单条成绩记录的增加修改以及删除时同此考试，年级或班级的相应个人成绩重新排序。


## 在线样例：

### 管理人员入口

[http://39.108.176.210/xadmin](http://39.108.176.210/xadmin)

管理人员账号：root

管理人员密码：admin123123

年级主任账号：liushuaicai

年级主任密码：liushuaicai


### 学生及教师入口

[http://39.108.176.210](http://39.108.176.210)

教师测试账号：1024

教师账号密码：123456

学生测试账号：20180001

学生账号密码：123456


## 安装

### 依赖包安装

下载文件进入项目目录之后，使用pip安装依赖包

<code>pip install -Ur requirements.txt</code>

### 数据库配置

修改wxcrm/setting.py 修改数据库配置，如下所示：

```
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wxcrm',
        'USER': 'root', 
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 3306,
    }
}
```

### 创建数据库

mysql数据库中执行:

<code>CREATE DATABASE 'wxcrm'</code>

迁移数据库，终端下执行:

```
./python manage.py makemigrations
./python manage.py migrate
```

### 创建超级用户

终端下执行:

<code>./python manage.py createsuperuser</code>

然后输入相应的超级用户名以及密码，邮箱即可。

### 开始运行

终端下执行:

<code>./python manage.py runserver</code>
 
浏览器打开: <code>http://127.0.0.1</code> 即可进入普通用户入口

浏览器打开: <code>http://127.0.0.1/xadmin</code> 即可进入超级用户入口
  
## 感谢
管理系统参考<a href="https://github.com/sshwsfc/xadmin" target="_blank">https://github.com/sshwsfc</a>的xadmin后台管理系统
