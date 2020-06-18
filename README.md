# who_i_am 我是谁表情包生成器  
> 本文发表于知乎专栏Django学习小组，[Django+PIL 做一个表情包生成网站](https://zhuanlan.zhihu.com/p/28793844)

## ZERO 前言  

最近看到一个系列表情包火了起来，无聊之下想起入门Django时没什么好玩项目的种种不利，就写下了这篇文章，记录一个小型Django入门项目从创建到部署的过程。  

![效果图](/images/view.png)

## ONE 什么是Django 

Django 项目是一个python定制框架，它源自一个在线新闻 Web 站点，于 2005 年以开源的形式被释放出来。Django 框架的核心组件有：  
- 用于创建模型的对象关系映射  
- 为最终用户设计的完美管理界面  
- 一流的 URL 设计  
- 设计者友好的模板语言  
- 缓存系统。  

总之Django是一款非常值得学习的web框架，关于框架的内容不再赘述，下面直接进入正题    
Django官网: https://www.djangoproject.com/  
Django项目主页: https://github.com/django  
## TWO 创建项目  
如果你还没有安装Django, 那么可以通过pip工具十分方便地进行安装：  
```
pip install djangoBash  
```  
短暂的等待后，运行以下命令创建项目：　　
```
django-admin startproject who_i_amBash
```  
当前目录下会产生一个名为who_i_am的文件夹，结构如下：  
```
who_i_am/
├── manage.py
└── who_i_am
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 5 files
```
进入文件夹，运行命令创建app:  
```
python manage.py startapp index 
```  
修改`who_i_am/settings.py`,在`INSTALLED_APPS`中加入刚刚建立的应用`index`:  
``` python
……
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
]
…… 
```
使用命令`python manage.py runserver 0.0.0.0:8080`运行开发服务器，打开浏览器访问`http://localhost:8080/`出现以下界面：　　 

![](/images/create_project.jpg)  

Django应用创建成功  
 
## THREE 真正的部分  

１）配置路由　 修改who_i_am/urls.py，绑定URL与视图函数：  
``` python 
…… 
from index import views as v

urlpatterns = [
    url(r'^admin/', admin.site.urls), #Django自带后台
    url(r'^$', v.index), #首页
    url(r'^makeit$', v.makeit), #生成表情包的接口
    url(r'^about$', v.about), #关于页面
]
……
```
２）创建视图函数
1. `index`函数处理首页：　
``` python 
def index(request):
    if request.method == "GET":
        return render(request,'index.html',{})　#直接使用render渲染返回即可Python
```  

2. `makeit`按参数生成图片并返回结果：  
这是最重要的一部分，实现了本网站的主要功能  
先用PIL库实现对图片的修改：　
``` python 
base = Image.open("base.png") #打开源图片
font = ImageFont.truetype('font.ttf', 40) #打开字体并设置字号
d = ImageDraw.Draw(base) # 实现对图片的绘图
d.text((100-len(text_one)*10, 30), text_one, font=font, fill=(0,0,0))  #向图片绘制文字，第一个参数是起始坐标，　第二个是字符串，font为字体，fill为文字颜色
```  
实现绘图以后，我们就可以使用PIL动态生成我们的表情包了  
创建视图函数makeit，使用`request.GET.get()`获取URL参数：  
``` python 
def makeit(request):
    if request.method == "GET":
        text_one = request.GET.get('whoiam',u"我们是谁！")
        ...
```
使用刚刚的代码根据参数生成图片后将图片存入内存：  
```  python
...
buf = BytesIO()
base.save(buf,format="png")  #将图片存入内存
image_stream = buf.getvalue()  #获取文件数据
return HttpResponse(base64.b64encode(image_stream))  #处理数据为base64编码并返回
...
``` 
３这个项目没有多少涉及Django的前端模板，前端部分就不再多讲，框架是用的materialize，地址在[Documentation - Materialize](https://materializecss.com/)　上面介绍的很详细…… 
下面贴一下负责动态加载图片的js代码, 这里是用了JQuery：
``` javascript
$(document).ready(function() {
    $('#makeit').click(function() {
        var one = $("#whoiam").val();
        var two = $("#name").val();
        var three = $("#whatwewant").val();
        var four = $("#idontknow").val();
        var five = $("#when").val();
        var six = $("#now").val();
        $.get("/makeit", {
            'whoiam': one,
            'name': two,
            'whatwewant': three,
            'idontknow': four,
            'when': five,
            'now': six,
        }, function(rec) {
            var img = "data:image/png;base64," + rec;
            $("#result").attr("src", img)
        })
    })
})
```
## FOUR 部署  

Django网站的部署对于新手来说是最大的一个坑   
关于部署，我认为最详细的教程应该是自强学堂的这篇[Django 部署(Nginx) - Django 教程 - 自强学堂](http://code.ziqiangxuetang.com/django/django-nginx-deploy.html) 这里省去安装nginx和uwsgi,直接聊聊配置文件.  
我的Nginx的.conf文件如下： 
``` conf
server {
    listen      80;
    server_name 你的域名;
    charset     utf-8;
    keepalive_timeout   70;   
    # 日志
    access_log 你的项目地址/access.log;
    error_log 你的项目地址/error.log;
    
    # 静态文件
    location /static {
        alias 你的项目地址/static;
    }
    
    # Django
    location / {
        uwsgi_pass  127.0.0.1:8080;#此处为uwsgi.ini(下面讲)中填的内容
        include     /etc/nginx/uwsgi_params;
    }
}
```
在项目目录下建立uwsgi.ini文件：  
``` ini
[uwsgi]

# Django-related settings

socket = :8080 #此处的端口应于.conf中的一致

# the base directory (full path)
chdir           = 项目地址

# Django uwsgi file
module  = who_i_am.wsgi

# process-related settings
# master
master          =        true

# maximum number of worker processes
processes       = 4

# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
touch-reload = 项目地址/reload # 监听reload文件，可以用于快速重启应用
die-on-term = true # 如果没有此配置，在重启项目后会大量占用CPU资源……（此坑 坑我不浅）
```  
修改`/etc/supervisord.conf`配置supervisor： 
在文件最后添加：  
``` ini
[program:who_i_am]
command=/path/to/uwsgi --ini 项目目录/uwsgi.ini #此处为刚刚建立的uwsgi.ini地址
directory=项目目录
startsecs=0
``` 
最后重启Nginx和supervisor：  
``` bash
service restart nginx
supervisorctl -c /etc/supervisord.conf restart who_i_am
```  
在域名服务商处建立A类型解析， 指向你的服务器ip地址，在浏览器输入你的域名：   

![](/images/view.png)  

当当当当～ 完成啦，就是最上面那张图的样子  

项目地址放在这里 [Who_I_am](https://github.com/Gengxin-Zhang/who_i_am)!   
最后放上几个表情包～  

![表情包1](/images/who_i_am_1.jpg)  
![表情包2](/images/who_i_am_2.jpg)  
![表情包3](/images/who_i_am_3.jpg)  



