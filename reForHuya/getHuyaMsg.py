import requests
import re
from selenium import webdriver
import pymongo


MONGO_URL = 'localhost'
MONGO_DB = '虎牙'
MONGO_COLLECTION = '英雄联盟板块'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_page(url):

    """  获取页面  """

    # 设置请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66',
        'Referer': 'https://www.huya.com/'
    }
    response = requests.get(url, headers=header)

    if response.status_code == 200:
        return response.text
    return None


def parse_html(html):

    """  利用正则表达式解析网页  """

    pattern = re.compile(
        '"gameFullName".*?"(.*?)",.*?totalCount".*?"(.*?)",.*?roomName".*?"(.*?)",.*?nick".*?"(.*?)",.*?introduction".*?"(.*?)",.*?profileRoom".*?"(.*?)"', re.S
    )
    items = re.findall(pattern, html)
    for index, item in enumerate(items):
        yield {
            '当前页序号': index,
            '类别': item[0].encode('utf-8').decode('unicode_escape'),  # 解码encode('utf-8').decode('unicode_escape')
            '标题': item[2].encode('utf-8').decode('unicode_escape'),
            '主播': item[3].encode('utf-8').decode('unicode_escape'),
            '人气': item[1],
            '直播介绍': item[4].encode('utf-8').decode('unicode_escape'),
            '直播间地址': 'https://www.huya.com/' + str(item[5])
        }


def main(page_no):
    # url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=2633&tagAll=0&page=' + str(page_no)
    url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=1&tagAll=0&page=' + str(page_no)
    html = get_page(url)
    # 网页解析返回yield生成器类型
    for item in parse_html(html):

        """  实现根据字典键找到对应值自动打开浏览器并跳转到直播间, if item['主播'] == 'xxxx' : get()  """
        if 'Uzi' in item['主播']:
            # print('UZI在直播')
            global browser
            # browser = webdriver.Edge()  # 初始化浏览器对象
            # browser.get('https://www.huya.com/666888')  #
        print(item)
        save_to_mongo(item)


def save_to_mongo(res):
    myList = []
    myList.append(res)
    try:
        if db[MONGO_COLLECTION].insert_many(myList):
            print('插入数据库成功')
    except Exception:
        print('插入数据库失败')


if __name__ == '__main__':
    print('开始清洗历史数据')
    db[MONGO_COLLECTION].delete_many({})
    print('历史数据清洗完成')
    for i in range(1, 10):
        main(page_no=i)
