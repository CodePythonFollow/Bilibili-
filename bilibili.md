# 一、这个会用在之后下载一个系列的视频

https://api.bilibili.com/x/player/pagelist?bvid=BV1mz411B7UV&jsonp=jsonp

这网站可以获取该列表下的所有的视频cid  

# 二、找到flv视频地址

https://api.bilibili.com/x/player/playurl

params = {

​		'cid': "178502235",                # 视频id
​		'bvid': "BV1mz411B7UV",  # 类别id
​		'qn': "0",								#从响应看出是画质，   112是最高有的没有标注
​		'type': "",
​		'otype': "json",
​		'fourk': "1",
​		'fnver': "0",
​		'fnval': "16",
​		'session': "652a83de29bb1a2c4a4c99614b91abcc",

}   # 后面三个参数就是分段的原因注释即可得到原视频即flv

​	

