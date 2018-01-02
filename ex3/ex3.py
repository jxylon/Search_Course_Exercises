import re
import requests
from bs4 import BeautifulSoup
import os
import urllib
import urllib3

def write_title(content):
    """
    把title中的内容写入文件
    """
    path = './data/'
    if not os.path.isdir('./data'):
        os.makedirs(path)
    with open('./data/title_list.txt', 'w') as f:
        f.write(content)


def remove_empty_line(content):
    """
    去除网页的空行以及英文字母
    """
    r = re.compile(r'''^\s+$''', re.M | re.S)
    s = r.sub('', content)
    r = re.compile(r'''\n+''', re.M | re.S)
    s = r.sub('\n', s)
    return s


def remove_js_css(content):
    """
    移除content中的script、style、meta、注释等脚本
    """
    r = re.compile(r'''<script.*?</script>''', re.I | re.M | re.S)
    s = r.sub('', content)
    r = re.compile(r'''<style.*?</style>''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''<!--.*?-->''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''<meta.*?>''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''<ins.*?</ins>''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''&nbsp;|&copy;''', re.I | re.M | re.S)
    s = r.sub('', s)
    r = re.compile(r'''\s''', re.I | re.M | re.S)
    s = r.sub('', s)
    return s


def remove_any_tag(s):
    """
    移除网页的多余标签
    """
    s = re.sub(r'''<[^>]+>''', '', s)
    return s.strip()


def extract_text(content):
    s = remove_empty_line(remove_js_css(content))
    s = remove_any_tag(s)
    s = remove_empty_line(s)
    return s


def write_content(content):
    path = './data/'
    if not os.path.isdir('./data'):
        os.makedirs(path)
    with open('./data/content.txt', 'w', encoding='utf-8') as f:
        f.write(content)


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('utf-8')


def getImg(html):
    reg = r'src="(.+?\.jpg|.+?\.png)"'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)
    x = 0
    path = './data/img'
    paths = path + '/'
    if not os.path.isdir(path):
        os.makedirs(path)
    for imgurl in imglist:
        try:
            urllib.request.urlretrieve(imgurl, '{}{}.jpg'.format(paths, 'img' + str(x)))
            x = x + 1
        except:
            continue
    return imglist


if __name__ == '__main__':
    url = 'https://bbs.hupu.com/20745392.html'
    # 提取网页内容 content为网页正文
    request = requests.get(url)
    request.encoding = 'utf-8'
    content = request.text
    # 提取标题
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('title').text
    # 标题写入文件
    write_title(title)
    # 移除网页其他标签
    content = extract_text(content)
    # 移除后的网页写入文件
    write_content(content)
    # 爬取网页的子链接 并写入文件
    a_list = soup.find_all('a')
    with open('./data/a_list.txt', 'w', encoding='utf-8') as f:
        for link in a_list:
            a = link.get('href')
            key = link.string
            if (key != None and a != None):
                f.write(key + '\t' + a + '\n')
    # 爬取网页图片
    html = getHtml(url)
    getImg(html)
