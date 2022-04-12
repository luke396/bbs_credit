"""
对每一个变量给出说明，此代码涉及众多不同相似概念，为避免混淆，特给出说明
name    网站的名字
url     原始的主页链接
block   网页侧面的版区
page    由帖子组成的页
post    帖子
帖子内部的页面，由于需要登录以查看所有，暂时不予以抓取。
"""

'''
在最后txt文件成型之后，为了保持词云图效果，实当删减了无关词汇
例如：
    1 2 3...数字，
    下载附件
    上传
    等
不对最后结果造成影响
'''


class Website:
    """
    对网站进行初步处理
    """

    def __init__(self,
                 name, url,
                 block, absoluteBlock,
                 post, absolutePost,
                 titleTag, bodyTag):
        self.name = name
        self.url = url
        self.block = block
        self.post = post
        self.absoluteBlock = absoluteBlock
        self.absolutePost = absolutePost
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Content:
    """对获取到的内容进行处理"""

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def save(self):
        """将结果以txt，带签名的utf-8储存"""
        with open('result.csv', 'a', encoding='utf-8-sig') as f:
            # f.write(self.url)
            f.write(self.title)
            f.write(self.body)


import re
import requests
from bs4 import BeautifulSoup
import time


class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    def getPage(self, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        try:
            req = requests.get(url=url, headers=headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            body = self.safeGet(bs, self.site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.save()
        else:
            print('Someting wrong with it.')

    def blocks(self):
        """获取所有区块"""
        bs = self.getPage(self.site.url)
        blocks = bs.find_all('a', href=re.compile(self.site.block))
        blocks_list = []
        for block in blocks:
            block = block.attrs['href']
            if self.site.absoluteBlock is False:
                block = '{}{}'.format(self.site.url, block)
            blocks_list.append(block)
        print(blocks_list)
        return blocks_list

    def crawl(self):
        blocks = self.blocks()
        for block in blocks:
            '''从首页进行，并翻页'''
            nextPageUrl = block
            while nextPageUrl:
                if nextPageUrl not in self.visited:
                    bs = self.getPage(nextPageUrl)
                    posts = bs.find_all('a', href=re.compile(self.site.post))
                    '''当前区块当前页的所有帖子'''
                    for post in posts:
                        post = post.attrs['href']
                        if not self.site.absolutePost:
                            post = '{}{}{}'.format(self.site.url, '/', post)
                        if post not in self.visited:
                            print('post: ' + post)
                            self.parse(post)
                            self.visited.append(post)
                    time.sleep(0.5)
                    self.visited.append(nextPageUrl)
                    print('nowPageUrl: ' + nextPageUrl)

                nextPage = bs.find('a', class_='nxt')
                nextPageUrl = self.site.url + '/' + nextPage['href'] if nextPage is not None else False


bbs = Website('Credit_bbs', 'https://bbs.51credit.com',
              'forum-.+', True,
              'thread.+', False,
              'h1', 'td.t_f')

crawler = Crawler(bbs)
result = crawler.crawl()
