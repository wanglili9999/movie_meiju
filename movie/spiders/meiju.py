# -*- coding: utf-8 -*-
import scrapy
from movie.items import MovieItem


class MeijuSpider(scrapy.Spider):
    name = 'meiju'    # 爬虫名。一个项目下可能有多个爬虫，并且每个爬虫有优先级、并发等设置。scrapy crawl [spider_name]
    allowed_domains = ['meijutt.com']  # 为了防止爬虫项目自动爬取到其它网站，设置限制，每一次请求前都会检查请求的网址是否属于这个域名下，是的话才允许请求。 注意：爬取日志爬取网址后响应总为None，检查allowed_domain书写是否正确。值是一级域名。
    start_urls = ['http://meijutt.com/new100.html']  # 第一个请求的url，整个程序逻辑的入口。得到的response返回给 self.parse(self.response=response)

    def parse(self, response):
        # print(response.status_code, response.content, response.text)
        # 非框架下写法 dom = lxml.etree.HTML(response.text) ; dom.xpath('')
        # scrapy框架下正规写法 Selector(response.text).xpath('').extract()

        # 获取美剧名
        movie_list = response.xpath('//ul[@class="top-list  fn-clear"]/li')  # [<Selector datda=li>对象, <Selector datda=li>对象]
        # / h5 / text()
        for movie in movie_list:
              # xpath()返回[Selector, Selector()] ，功能强，可以在Selector对象上进行第二次xpath解析
              # xpath().extract() 返回['剧集名1', '剧集名2']
              # movie.xpath().extract_first() 返回'剧集名1'
              # .表示在子标签基础上继续解析

            name = movie.xpath('./h5/a/text()').extract_first()
            # print(movie, name)  # 建议debug不是print，不然因为并发会重复打印多次信息

            item = MovieItem()
            item['name'] = name
            yield item   # 相当于同步脚本方法中的return
