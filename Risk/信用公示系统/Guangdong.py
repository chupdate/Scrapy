__author__ = 'Chen'
#coding=utf-8
import  urllib.parse,urllib.request
import re
from datetime import *
from YCParser import YCParser
import json

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urllib.parse.urlencode({
            'pageNo':'%d' % pageNos,
            'textfield':''
        }).encode('utf-8')
        return postdata

    def getinfpostdata(self,entNo,entType,regOrg):
        postdata=urllib.parse.urlencode({
            'entNo':entNo,
            'entType':entType+'++',
            'regOrg':regOrg
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=-1
        while True:
            pageNos+=1
            req=urllib.request.Request(
                url='http://gsxt.gdgs.gov.cn/aiccips/main/abnInfoList.html?pageNo='+str(pageNos),
                data=self.getpostdata(pageNos),
                headers={'User-Agent':'Magic Browser'}
            )
            result=self.gethtml(req)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            print('Page %d Reading' % (pageNos+1))
            relist=json.loads(str(result))['rows']
            br=0
            for re in relist:
                cdate=re['abnTimeStr']
                cdate=date(int(cdate[0:4]),int(cdate[5:7]),int(cdate[8:10]))
                if cdate<startdate:
                    br=1
                    break
                else:
                    if cdate<=enddate:
                        Name=re['entName'];regID=re['regNO'];entNo=re['entNo']
                        entType=re['entType'];regOrg=re['decOrg']
                        entdict=dict(Name=Name,regID=regID,entNo=entNo,entType=entType,regOrg=regOrg)
                        self.PrintInfo(entdict)
            if br==1:break


    def PrintInfo(self,ent):
        #使用post方法提取经营异常信息
        req=urllib.request.Request(
            url='http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipUnuDirInfo',
            data=self.getinfpostdata(ent['entNo'],ent['entType'],ent['regOrg']),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='广东'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,10,8),enddate=date.today()-timedelta(days=1))