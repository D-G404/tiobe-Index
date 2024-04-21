# 条型竞赛图项目
本文可视化效果如视频：[b站视频链接](https://www.bilibili.com/video/BV14z421k7dF/?vd_source=f77d7d4b4ca29431faf164ca9877cca9)  
所使用网站：[爬取网站链接](https://www.tiobe.com/tiobe-index/)

本项目是数据可视化项目 主要是后端 前端采用[flourish](https://app.flourish.studio/projects)来可视化的实现，使用Python进行数据爬取以及后端数据处理,
主要用到的库有requests、pandas、re对csv文件处理

前端也可采用 node.js JavaScript Typescripe 进行可视化实现，可使用b站up见齐的开源项目 [见齐项目](https://github.com/Jannchie/anichart.js)
python中也有bar race chart库可供使用

本项目只使用spider.py即可，生成csv文件后再转置即可得到最终文件
