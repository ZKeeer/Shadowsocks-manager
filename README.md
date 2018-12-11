# SSAdmin
shadowsocks多用户管理，一键安装shadowsocks和ssadmin，控制端口流量/速度，查看端口状态，修改ss配置<br/>
<hr/>
<h3>notice:</h3>
<li>限速功能/系统信息尚未完成，2018年12月13日之前完成。</li>
<li>仅适用于shadowsocks-python</li>
<li>仅适用于Ubuntu，仅在Ubuntu 16.04 x64测试通过</li>
<hr/>
<h3>如何使用</h3>
0.尽量使用root用户登录<br/>
1.使用wget https://github.com/ZKeeer/SSAdmin.git<br/>
2.进入ssadmin目录<br/>
3.使用命令python3 setup.py install进行安装，大约耗时2~4分钟<br/>
4.使用命令python3 setup.py start/stop/restart可启动/停止/重启ssadmin<br/>
5.ssadmin默认用户admin 密码：ssadmin 登陆后请及时修改密码。<br/>
6.通过ssadmin可以对shadowsocks启动ss/停止ss/修改配置/添加用户/限制流量/限制速度/端口流量监控/系统信息...<br/>
7.如何优化提速，请查看我博客<br/>
8.如果您的vps同时运行其他服务，或者想用80端口（默认是8000）运行，请安装nginx并进行合理配置。
<hr/>
<h2>热烈欢迎PR~</h2>
我第一次写前端，求大佬PR<br>
或者有什么好的想法和功能，欢迎PR
<br/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-1.png">
<br/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-2.png">
<br/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-3.png">
<br/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-1.png">

