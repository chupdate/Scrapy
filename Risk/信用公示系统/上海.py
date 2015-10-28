__author__ = 'Han'
#coding=utf-8
#只能获取50页的信息
import urllib.request,urllib.parse
import re
from datetime import *
from YCParser import YCParser

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'captcha':'',
            'condition.pageNo':'%d'% pageNos,
            'condition.insType':'',
            'session.token':'88872345-df19-4ee0-b711-ee4b2b2104d7',
            'condition.keyword':''
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>50:break
                req=urllib.request.Request(
                    url='https://www.sgs.gov.cn/notice/search/ent_except_list',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                table=result.find('table')
                infolist=table.findAll('td')
                l=len(infolist)
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(2,l,3):
                    try:
                        cdate=infolist[i].contents[0]
                        reg=r'年(.*?)月'
                        pattern=re.compile(reg)
                        month=int(pattern.findall(cdate)[0])
                        reg=r'月(.*?)日'
                        pattern=re.compile(reg)
                        day=int(pattern.findall(cdate)[0])
                        cdate=date(int(cdate[0:4]),month,day)
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=infolist[i-2].find('a').contents[0].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                regID=infolist[i-1].contents[0]
                                href=infolist[i-2].find('a').get('href')
                                entdict=dict(Name=Name,regID=regID,href=href)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        infourl=ent.get('href')
        inforesult=self.gethtml(infourl)
        infolist=inforesult.find('table',attrs={'id':'exceptTable'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='上海'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,10,8),enddate=date.today()-timedelta(days=0),fmode='a')