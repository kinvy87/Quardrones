from lxml import etree
import urllib.request
import urllib.parse
import time
import os
import random


# 每次重启后，代理都是随机的
def get_headers():
    random_UA = random.choice(['Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
                               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
                               'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
                               'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
                               'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
                               'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                               'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                               'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
                               'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                               'NOKIA5700/ UCWEB7.0.2.37/28/999',
                               'Openwave/ UCWEB7.0.2.37/28/999',
                               'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
                               'UCWEB7.0.2.37/28/999',
                               'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
                               'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
                               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
                               'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                               'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                               'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                               'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                               'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                               'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
                               ])
    headers = {
        'User-Agent': random_UA
    }
    return headers


def handle_request(url, page=None):
    if page:
        url = url.format(page)
    headers = get_headers()
    print(headers)
    request = urllib.request.Request(url=url, headers=headers)
    return request


def parse_content(content, board):
    tree = etree.HTML(content)
    # 文章链接列表
    href_list = tree.xpath('//table[@id="threadlisttableid"]//a[@class="s xst"]/@href')
    # print(href_list)
    for href in href_list:
        picture = get_picture(href, board)


def get_picture(href, board):
    request = handle_request(href)  # 通过二级链接构建请求对象
    content = urllib.request.urlopen(request).read().decode('gbk')
    tree = etree.HTML(content)
    # 文章标题
    title = tree.xpath('//span[@id="thread_subject"]/text()')[0]
    print('正在爬取文章%s....' % title)
    # 图片下载路径列表
    src_list = tree.xpath('//div[@id="postlist"]/div//td[@class="t_f"]//img/@zoomfile')
    print(src_list)
    # 图片id列表
    id_list = tree.xpath('//td[@class="t_f"]//img/@id')
    for src in src_list:
        img_id = id_list[src_list.index(src)]
        print(src)
        print(img_id)
        suffix = src.split('.')[-1]
        # 图片名
        img_name = title + img_id + '.' + suffix

        # 建立文件夹
        dirname = board
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        # 保存路径
        filepath = os.path.join(dirname, img_name)

        # 保存文件
        try:
            urllib.request.urlretrieve(src, filepath)
        except:
            print("Error: 标题格式不正确")  # title有乱码,无法写入时会报错

        time.sleep(0.5)


def main():
    board = int(input('请输入需要查看的分类代号：1--多旋翼；2--固定翼；3--航拍;4--无人机技术*****：'))
    if board == 1:
        code = input('请输入所需要爬取的板块代号：576--穿越机综合技术讨论区;770--多旋翼综合技术讨论专栏*****：')
        board = '我爱模型论坛/多旋翼'
    elif board == 2:
        code = input('请输入所需要爬取的板块代号：706--固定翼精彩视频与图片；718--电动固定翼*****：')
        board = '我爱模型论坛/固定翼'
    elif board == 3:
        code = input('请输入所需要爬取的板块代号：716--航拍与第一视角飞行技术*****：')
        board = '我爱模型论坛/航拍'
    elif board == 3:
        code = input('请输入所需要爬取的板块代号：716--航拍与第一视角飞行技术*****：')
        board = '我爱模型论坛/无人机技术'

    else:
        print('您输入的分类还未录入，请查询现有分类，谢谢！')

    # url='http://bbs.5imx.com/forum.php?mod=forumdisplay&fid=718&page={}'  #电动固定翼
    url = 'http://bbs.5imx.com/forum.php?mod=forumdisplay&fid=%s&page={}' % code
    start_page = int(input('请输入起始页码:'))
    end_page = int(input('请输入结束页码:'))
    for page in range(start_page, end_page + 1):
        print('正在爬取第%s页....' % page)
        request = handle_request(url, page)
        content = urllib.request.urlopen(request).read().decode('gbk')
        parse_content(content, board)
        print('完成爬取第%s页....' % page)
        time.sleep(2)


if __name__ == '__main__':
    main()
