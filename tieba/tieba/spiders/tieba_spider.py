#coding=utf-8
from tieba.items import TiebaItem
import time
import scrapy
import re
import logging

class tieba_spider(scrapy.Spider):
    name='tieba_card'
    #规范形式网址(带有吧全名）
    start_urls=['http://tieba.baidu.com/f?kw=%E4%B8%AD%E5%9B%BD%E5%BB%BA%E8%AE%BE%E9%93%B6%E8%A1%8C']
    allowed_domains=['baidu.com']
    url_complete=[]
    #如果需要网站标题，可以写一个以网址为键的字典，将值传递给回调函数

    def parse(self,response):
        for url in response.xpath('//a[@class="j_th_tit"]/@href').re('/p/\d+$'):
            url_long='http://tieba.baidu.com'+url
            if url_long not in self.url_complete:
                self.url_complete.append(url_long)
                yield scrapy.Request(url_long,callback=self.parse_item)
        pos=response.url.find('&')
        for url in response.xpath('//a/@href').re('%s.*&pn=\d+$' % re.escape(response.url[22:pos])):             #验证是否是本吧的贴子
            url_long='http://tieba.baidu.com'+url
            if url_long not in self.url_complete:
                self.url_complete.append(url_long)
                yield self.make_requests_from_url(url_long)


    def parse_item(self,response):
        #贴子被隐藏的情况
        if response.body.find('l_post j_l_post l_post_bright')==-1:return
        sel=response.xpath('//div[@class="l_post j_l_post l_post_bright noborder "]')
        if sel:
            data_field=self.make_data_field(sel)
            if data_field:
                self.zt_text_id=data_field['content']['post_id']
                item=self.item_extract(data_field,1,'')
                title=response.xpath('//h1[contains(@class,"core_title_txt")]/text()').extract()
                if not title:title=''
                else:title=title[0]
                item['text']=title+':'+sel.xpath('.//div[contains(@class,"d_post_content j_d_post_content")]/text()').extract()[0].replace('\n','').strip()
                yield item

        for sel in response.xpath('//div[@class="l_post j_l_post l_post_bright  "]'):
            data_field=self.make_data_field(sel)
            if not data_field:continue
            item=self.item_extract(data_field,2,self.zt_text_id)
            item['text']=sel.xpath('.//div[contains(@class,"d_post_content j_d_post_content")]/text()').extract()[0].replace('\n','').strip()
            yield item

        comment_list=response.xpath('//script/text()').re('\"commentList\" : (\{.*\}).*"isAdThread"')[0]
        try:
            comment_list=eval(comment_list.replace('null','""'))
        except Exception:
            logging.ERROR('Read comment_list error: %s' % response.url)
        else:
            for text_id in comment_list.keys():
                if comment_list[text_id]:
                    for comment in comment_list[text_id]:
                        item=TiebaItem()
                        item['user_id']=comment['user_id']
                        item['text_id']=comment['comment_id']
                        item['post_time']=self.timestamp_datetime(comment['now_time'])
                        item['type']=3
                        item['post_id']=text_id
                        stext=comment['content']
                        pattern=re.compile(r'<(a|img).*>')
                        stext=pattern.sub('',stext)
                        pos=stext.find(':')
                        item['text']=stext[pos+1:].replace('\n','').strip()
                        yield item

        for url in response.xpath('//a/@href').re('/p/.*pn=\d+$'):
            url_long='http://tieba.baidu.com'+url
            if url_long not in self.url_complete:
                self.url_complete.append(url_long)
                yield scrapy.Request(url_long,callback=self.parse_item)

    def make_data_field(self,sel):
        data_field=sel.xpath('@data-field').extract()[0]
        data_field=data_field.replace('null','""').replace('true','True').replace('false','False')
        try:
            data_field=eval(data_field)
        except Exception:
            logging.ERROR('Download Item error: %s' % data_field)
            return {}
        else:
            return data_field

    def item_extract(self,data_field,type,post_id):
        item=TiebaItem()
        if data_field['author'].get('user_id'):
            item['user_id']=data_field['author'].get('user_id')
        else:
            item['user_id']=data_field['author'].get('user_name')
        item['level']=data_field['author'].get('level_id')
        item['text_id']=data_field['content']['post_id']
        item['post_time']=data_field['content']['date']
        item['type']=type
        item['post_id']=post_id
        return item

    def timestamp_datetime(self,value):
        format = '%Y-%m-%d %H:%M'
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt