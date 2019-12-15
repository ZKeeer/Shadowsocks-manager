# SSAdmin
一个简单的小工具，方便大家使用<br/>
shadowsocks多用户管理，一键安装shadowsocks和ssadmin，控制端口流量/速度，查看端口状态，修改ss配置<br/>
<hr/>
<h3>notice:</h3>
<li>限速功能/系统信息尚未完成，<del>2018年12月13日之前</del>完成。</li>
<li>仅适用于shadowsocks-python</li>
<li>仅适用于Ubuntu，仅在Ubuntu 16.04 x64测试通过</li>
<li><a href="https://www.vultr.com/?ref=7634513">vultr</a>、阿里云测试通过，腾讯云无法启动shadowsocks</li>
<li>vultr新加坡 测试效果与 阿里云香港 差不多，价格更便宜，一个月3.5刀，使用链接注册有优惠https://www.vultr.com/?ref=7634513</li>
<hr/>
<h3>如何使用</h3>
0.尽量使用root用户登录<br/>
1.使用wget https://github.com/ZKeeer/Shadowsocks-manager/archive/master.zip<br/>
2.进入ssadmin目录<br/>
3.使用命令python3 setup.py install进行安装shadowsocks和ssadmin，同时会启动ssadmin，大约耗时2~4分钟<br/>
4.使用命令python3 setup.py start/stop/restart可启动/停止/重启ssadmin<br/>
5.ssadmin默认用户admin 密码：ssadmin 登陆后请及时修改密码。<br/>
6.通过ssadmin可以对shadowsocks启动ss/停止ss/修改配置/添加用户/限制流量/限制速度/端口流量监控/系统信息...<br/>
7.如何优化提速，请查看我博客<br/>
8.如果您的vps同时运行其他服务，或者想用80端口（默认是8000）运行，请安装nginx并进行合理配置。<br/>
9.进一步优化请访问：http://zkeeer.space/?tag=shadowsocks
<hr/>
<h2>热烈欢迎PR~</h2>
我第一次写前端，求大佬PR<br>
或者有什么好的想法和功能，欢迎PR
<hr/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-1.png">
<br/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-2.png">
<br/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-3.png">
<br/>
<img src="https://github.com/ZKeeer/SSAdmin/blob/master/static/img/ssadmin-4.png">

