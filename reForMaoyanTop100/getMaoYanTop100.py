import re
import time
import pymongo
import requests
'''  使用 正则表达式提取猫眼前100电影  '''


MONGO_URL = 'localhost'
MONGO_DB = 'MOVE'
MONGO_COLLECTION = 'top'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_one_page(url):

    # 设置请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66',
        'Referer': 'https://maoyan.com/'
    }
    # 发起请求
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        return response.text
    return None


def parse_html(html):
    pattern = re.compile(
        '<dd>.*?board-index-.*?>(.*?)</i>.*?href.*?title="(.*?)".*?data-src="(.*?)".*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排名': item[0],
            '片名': item[1],
            '图片': item[2],
            '主演': item[3].strip()[3:] if len(item[3]) > 3 else '',
            '上映时间': item[4].strip()[5:] if len(item[4]) > 5 else '',
            '评分': item[5].strip() + item[6].strip()
        }


def save_to_mongo(res):
    mylist = []
    mylist.append(res)
    try:
        if db[MONGO_COLLECTION].insert_many(mylist):
            print('插入Mongo成功')
    except Exception:
        print('插入Mongo失败')


def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    for item in parse_html(get_one_page(url)):
        save_to_mongo(item)
        print(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
