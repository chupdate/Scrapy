#coding=utf-8
import scrapy
from test1.items import dmozItem

class dmoz_spider(scrapy.Spider):
    name='dmoz'
    allowed_domains=['dmoz.org']
    #每个start_url得到response,传入parse
    start_urls=['http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
                'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/']

    def parse(self,response):     #处理respoonse
        '''
        filename=response.url.split('/')[-2]
        with open(filename,'wb') as f:
            f.write(response.body)
        '''
        for sel in response.xpath('//ul/li'):
            item=dmozItem()
            item['title']=sel.xpath('a/text()').extract()
            item['url']=sel.xpath('a/@href').extract()
            item['desc']=sel.xpath('text()').extract()
            yield item