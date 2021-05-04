### 传统电商项目模块特点

    * 概念和原理较多
    * 横向展开的知识点比较多
    * 虚拟机中已部署项目与环境，可以一键启动脚本
    * 传统的tomcat + mysql项目
    
### 目标
    
    * 掌握Jmeter脚本开发技术
    * 了解项目中常见的几种协议
    * 会使用grafana进行服务器监控与mysql监控
    * 掌握JVM/GC调优的概念与原理
    * 了解电商项目的运行原理等
    
### 虚拟机连接MobaXterm

    1、虚拟机使用命令查看ip地址：ifconfig | grep 192
       返回ip地址：192.168.148.131
    2、MobaXterm新建seesion：Remote Host输入：ip地址；Specify username输入虚拟机名称root；端口号默认是22
    3、若有提示输入密码则输入虚拟机创建时的密码
    
### 一键启动脚本存放的位置

    1、cd /data/startup 切换目录
    2、ll 查看可执行脚本
    3、./d1-startDsShop-tomcat.sh 一键启动商城的脚本
    4、192.168.148.131:8083  谷歌浏览器访问商城