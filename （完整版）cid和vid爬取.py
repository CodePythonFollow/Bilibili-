import requests
import re
from concurrent.futures import ThreadPoolExecutor


class Bili_spider():
    def __init__(self, bvid):
        self.bvid = bvid
        self.headers = {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'cookie': "bsource=seo_bing; _uuid=663371CB-5514-DE59-BA27-0BCDBB0A75CA07147infoc; buvid3=873BCEE9-964E-4E1C-B37D-701FCAC4D96D53947infoc; sid=bp1xvkam; DedeUserID=243649950; DedeUserID__ckMd5=365ebebca8eceac0; SESSDATA=ab8a1208%2C1606268513%2Cc37cc*51; bili_jct=16c27ec0f751d09649044021b03d2c57; CURRENT_FNVAL=16; rpdid=|(J|)|~Rlu)k0J'ulm|~uYll); PVID=3; bfe_id=fdfaf33a01b88dd4692ca80f00c2de7f",
            'origin': "https://www.bilibili.com",
            'referer': f"https://www.bilibili.com/video/{self.bvid}",
            'sec-fetch-dest': "empty",
            'sec-fetch-mode': "cors",
            'sec-fetch-site': "same-site",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        }
        

    # 获取每个视频的id
    def get_cids(self):
        url = 'https://api.bilibili.com/x/player/pagelist'
        params = {
            'bvid': self.bvid,
            'jsonp': 'jsonp'
        }
        response = requests.get(url, params=params)
        cids = response.json()['data']
        # print(cids)
        for i in cids:
            cid = i["cid"]
            part = i["part"]

            # 启用线程池进行爬取   设置线程最大值
            executor = ThreadPoolExecutor(max_workers=5)
            executor.submit(self.spider, cid, part)
            

    # 获取flv视频链接并保存   也可单独调用用来下载单个视频
    def spider(self, cid, part):
        url = 'https://api.bilibili.com/x/player/playurl'
        params = {
            'cid': cid,
            'bvid': self.bvid,
            'qn': '112',
            'type': '',
            'otype': 'json',
            'fourk': '1',
        }

        response = requests.get(url, params=params)
        url = response.json()['data']['durl'][0]['url']
        size = response.json()['data']['durl'][0]['size'] / 1024 / 1024
        self.save(url, part, size)

    # 保存视频
    def save(self, url, part, size):
        h = re.findall("http://(.*?)/", url)
        host = h[0]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': host,
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36',
        }
        
        response = requests.get(url, headers=headers)
 
        if response.status_code < 300  and not os.path.exists(f"{part}.flv"):
            print('%s正在下载视频，大小为：% .2fM' % (part, size))
            with open(f'{part}.flv', 'wb') as fi:
                fi.write(response.content)
            print(f"{part}保存完成")



if __name__ == '__main__':
    # 此处传入Biv即可下载所有视频
    bili = Bili_spider(bvid='BV1U4411U7Zc')
    bili.get_cids()
