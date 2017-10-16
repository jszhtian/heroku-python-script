import urllib.parse
import urllib.request
import re
from bs4 import BeautifulSoup


class VNDBGetInfo():
    url=''
    soup=None
    def GetPage(self,url):
        self.url=url
        #print('input URL:'+url)
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
        req=urllib.request.Request(url,None,{'User-Agent':user_agent})
        response=urllib.request.urlopen(req)
        page=response.read()
        return page
    def ExtractInfo(self,buf):
        if not self.soup:
            try:
                self.soup=BeautifulSoup(buf,'html.parser')
            except:
                print('Soup failed to get information:'+self.url)
                return
        title=self.soup.title.string
        if title=='Browse visual novels':
            Gamelist=['List']
            divs=self.soup.find('div',attrs={'class':'mainbox browse vnbrowse'})
            table = divs.find('table', attrs={'class':'stripe'})
            rows = table.find_all('tr')
            for row in rows:
                try:
                    Gamelist.append(row.td.a['title']+"|"+'Number: '+row.td.a['href'][2:])
                except:
                    pass
            return Gamelist
        else:
            infolist=['Game']
            imgURL=''
            title1=''
            title2=''
            description=''
            aliases=''
            length=''
            developer=''
            publisher=''
            divs=self.soup.find('div',attrs={'class':'mainbox'})
            detail=divs.find('div',attrs={'class':'vndetails'})
            imgsrc=detail.find('img')
            if(imgsrc):
                imgURL=imgsrc['src']
            table = detail.find('table', attrs={'class':'stripe'})
            rows = table.find_all('tr')
            desc=table.find('td',attrs={'class':'vndesc'})
            if desc:
                description=desc.p.getText()
            for row in rows:
                index=0
                tds=row.find_all('td')
                if tds[0].string=='Title':
                    title1=tds[1].string
                elif tds[0].string=='Original title':
                    title2=tds[1].string
                elif tds[0].string=='Aliases':
                    aliases=tds[1].string
                elif tds[0].string=='Length':
                    length=tds[1].string
                elif tds[0].string=='Developer':
                    list=tds[1].find_all('a')
                    for line in list:
                        developer+=line.string+','
                elif tds[0].string=='Publishers':
                    list=tds[1].find_all('a')
                    for line in list:
                        publisher+=line.string+','
            infolist.append(imgURL)
            infolist.append(title1)
            infolist.append(title2)
            infolist.append(description)
            infolist.append(aliases)
            infolist.append(length)
            infolist.append(developer)
            infolist.append(publisher)
            return infolist
        
class BangumiGetInfo():
    url=''
    soup=None
    def GetPage(self,url):
        self.url=url
        #print('input URL:'+url)
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
        req=urllib.request.Request(url,None,{'User-Agent':user_agent})
        response=urllib.request.urlopen(req)
        page=response.read()
        return page
    def ExtractInfo(self,buf):
        if not self.soup:
            try:
                self.soup=BeautifulSoup(buf,'html.parser')
            except:
                print('Soup failed to get information:'+self.url)
                return
        title=self.soup.title.string
        Gamelist=[]
        if title.startswith("Bangumi"):
            Gamelist.append("List")
            uls=self.soup.find('ul',attrs={'id':'browserItemList'})
            lis = uls.find_all('li')
            for li in lis:
                try:
                    Gamelist.append(li.div.h3.a.getText()+'|'+'Number:'+li['id'][5:])
                except:
                    pass
            return Gamelist
        else:
            infolist=['Game']
            imgURL=''
            divs=self.soup.find('div',attrs={'id':'bangumiInfo'})
            img=divs.find('div',attrs={'align':'center'})
            imgsrc=img.find('img')
            if(imgsrc):
                imgURL=imgsrc['src']
            infolist.append(imgURL)
            descdiv=self.soup.find('div',attrs={'id':'subject_detail'})
            desc=descdiv.find('div',attrs={'id':'subject_summary'})
            infolist.append(desc.getText())
            table = divs.find('ul', attrs={'id':'infobox'})
            rows = table.find_all('li')
            gametitle=self.soup.find('h1',attrs={'class':'nameSingle'})
            infolist.append('标题:'+gametitle.getText())
            for row in rows:
                infolist.append(row.getText())
            return infolist

class TDFGetInfo():
    url=''
    soup=None
    def GetPage(self,url):
        self.url=url
        #print('input URL:'+url)
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
        req=urllib.request.Request(url,None,{'User-Agent':user_agent})
        response=urllib.request.urlopen(req)
        page=response.read()
        return page
    def ExtractInfo(self,buf):
        if not self.soup:
            try:
                self.soup=BeautifulSoup(buf,'html.parser')
            except:
                print('Soup failed to get information:'+self.url)
                return
        title=self.soup.title.string
        #print(title)
        Gamelist=[]
        if title.startswith("游戏条目"):
            Gamelist.append("List")
            ul=self.soup.find('ul',attrs={'class':'media-list inline intro-list'})
            lis=ul.find_all('li',attrs={'class':'media'})
            #print(lis)
            for li in lis:
                try:
                    Gamelist.append(li.div.h4.a.getText()+'|'+'Number:'+li.div.h4.a['href'][10:])
                except:
                    pass
            return Gamelist
        else:
            infolist=['Game']
            imgURL=''
            divs=self.soup.find('div',attrs={'class':'span8'})
            img=divs.find('div',attrs={'class':'media'})
            imgsrc=img.find('img')
            if(imgsrc):
                imgURL=imgsrc['src']
                if imgURL.find('?')!=-1:
                    imgURL=imgURL[0:imgURL.find('?')]
            infolist.append(imgURL)

            titlediv=self.soup.find('div',attrs={'class':'navbar navbar-inner block-header no-border'})
            infolist.append(titlediv.h3.getText())

            div = divs.find('div', attrs={'class':'control-group'})
            rows = div.find_all('p')
            for row in rows:
                result=re.sub(" +"," ",row.getText())
                infolist.append(result)
            return infolist



