import requests
import json
from lxml import etree
"""
此代码未完成，原理是分段爬取再利用ffemp进行合并  这里已返回了视频音频的url 后面未完成
"""

class Bili():
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': "bsource=seo_bing; _uuid=663371CB-5514-DE59-BA27-0BCDBB0A75CA07147infoc; buvid3=873BCEE9-964E-4E1C-B37D-701FCAC4D96D53947infoc; sid=bp1xvkam; DedeUserID=243649950; DedeUserID__ckMd5=365ebebca8eceac0; SESSDATA=ab8a1208%2C1606268513%2Cc37cc*51; bili_jct=16c27ec0f751d09649044021b03d2c57; CURRENT_FNVAL=16; rpdid=|(J|)|~Rlu)k0J'ulm|~uYll); PVID=2",
            'referer': 'https://search.bilibili.com/all?keyword=mangodb',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }

    def spider_url(self):
        url = 'https://www.bilibili.com/video/BV1mz411B7UV?p=2'

        response = requests.get(url, headers=self.headers)

        html = etree.HTML(response.text)
        scripts = html.xpath('//head/script[3]/text()')[0]

        json_data = scripts[scripts.find('=')+1:]
        data = json.loads(json_data)
        videos = data['data']['dash']['video']
        audios = data['data']['dash']['audio']
        video = videos[0]['baseUrl']
        audio = audios[0]['baseUrl']
        return video, audio


if __name__ == '__main__':
    bili = Bili()
    video, audio = bili.spider_url()

