import requests
import re
from concurrent.futures import ThreadPoolExecutor


class Bili_spider():
    def __init__(self, bvid):
        self.headers = {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'cookie': "bsource=seo_bing; _uuid=663371CB-5514-DE59-BA27-0BCDBB0A75CA07147infoc; buvid3=873BCEE9-964E-4E1C-B37D-701FCAC4D96D53947infoc; sid=bp1xvkam; DedeUserID=243649950; DedeUserID__ckMd5=365ebebca8eceac0; SESSDATA=ab8a1208%2C1606268513%2Cc37cc*51; bili_jct=16c27ec0f751d09649044021b03d2c57; CURRENT_FNVAL=16; rpdid=|(J|)|~Rlu)k0J'ulm|~uYll); PVID=3; bfe_id=fdfaf33a01b88dd4692ca80f00c2de7f",
            'origin': "https://www.bilibili.com",
            'referer': "https://www.bilibili.com/video/BV1mz411B7UV?p=3",
            'sec-fetch-dest': "empty",
            'sec-fetch-mode': "cors",
            'sec-fetch-site': "same-site",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        }
        self.bvid = bvid

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
        for i in cids[-9:]:
            cid = i["cid"]
            part = i["part"]

            # 启用线程池进行爬取   设置线程最大值
            executor = ThreadPoolExecutor(max_workers=5)
            f = executor.submit(self.spider, cid, part)

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
        size = response.json()['data']['durl'][0]['size'] / 1024 /1024
        print('%s正在下载视频，大小为：% .2fM' % (part, size))
        self.save(url, part)

    # 保存视频
    @staticmethod
    def save(url, part):
        h = re.findall("http://(.+)com", url)
        host = h[0] + "com"
        headers = {
            'host': host,
            'accept': "application/json, text/javascript, */*; q=0.01",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'cookie': "bsource=seo_bing; _uuid=663371CB-5514-DE59-BA27-0BCDBB0A75CA07147infoc; buvid3=873BCEE9-964E-4E1C-B37D-701FCAC4D96D53947infoc; sid=bp1xvkam; DedeUserID=243649950; DedeUserID__ckMd5=365ebebca8eceac0; SESSDATA=ab8a1208%2C1606268513%2Cc37cc*51; bili_jct=16c27ec0f751d09649044021b03d2c57; CURRENT_FNVAL=16; rpdid=|(J|)|~Rlu)k0J'ulm|~uYll); PVID=3",
            'origin': "https://www.bilibili.com",
            'referer': "https://www.bilibili.com/video/BV1mz411B7UV?p=2",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        }
        response = requests.get(url, headers=headers, stream=True, verify=False)

        print(response.status_code)
        with open(f'{part}.flv', 'wb') as fi:
            fi.write(response.content)


if __name__ == '__main__':
    # 此处传入Biv即可下载所有视频
    bili = Bili_spider(bvid='BV1RE41187Yo')
    bili.get_cids()
