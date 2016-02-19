#coding=utf-8
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class tieba_spider(CrawlSpider):
    name='tieba_card'
    start_urls=['http://tieba.baidu.com/f?kw=%E4%B8%AD%E5%9B%BD%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C',
    'http://tieba.baidu.com/f?kw=%E5%86%9C%E8%A1%8C',
    'http://tieba.baidu.com/f?kw=%D6%D0%B9%FA%D2%F8%D0%D0',
    'http://tieba.baidu.com/f?kw=%D6%D0%B9%FA%BD%A8%C9%E8%D2%F8%D0%D0',
    'http://tieba.baidu.com/f?kw=%E4%BA%A4%E9%80%9A%E9%93%B6%E8%A1%8C&ie=utf-8',
    'http://tieba.baidu.com/f?kw=%D0%A1%D5%D0e%D5%BB&fr=ala0&loc=rec',
    'http://tieba.baidu.com/f?kw=%D5%C2%D3%E3%BF%A8&fr=ala0&loc=rec',
    'http://tieba.baidu.com/f?ie=utf-8&kw=%E5%B9%BF%E5%8F%91%E9%93%B6%E8%A1%8C',
    'http://tieba.baidu.com/f?kw=sh601166%B9%C9%C6%B1&fr=ala0&tpl=5',
    'http://tieba.baidu.com/f?kw=sh600015%B9%C9%C6%B1&fr=ala0&tpl=5',
    'http://tieba.baidu.com/f?kw=%E4%B8%AD%E5%9B%BD%E6%B0%91%E7%94%9F%E9%93%B6%E8%A1%8C',
    'http://tieba.baidu.com/f?kw=%D3%CA%B4%A2%D2%F8%D0%D0'
    ]
    rules=(
        Rule(LinkExtractor(allow=('&ie=utf-8&pn='))),
        Rule(LinkExtractor(allow=('/p/\d+')),callback='parse_item')
    )

    def parse_item(self,response):
        item=scrapy.Item()



