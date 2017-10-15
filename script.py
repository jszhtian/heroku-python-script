#!/usr/bin/env python
#coding:utf-8

import urllib.parse
import urllib.request
import asyncio
import re
import time
import wikipedia
from bs4 import BeautifulSoup
from googletrans import Translator

import discord

BotVer='20171016'
client = discord.Client()

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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Bot Ver:'+BotVer)
    print('------')

@client.event
async def on_message(message):
    #if message.content.startswith('!test'):
    #   counter = 0
    #    tmp = await client.send_message(message.channel, 'Calculating messages...')
    #    async for log in client.logs_from(message.channel, limit=100):
    #        if log.author == message.author:
    #            counter += 1
    #    await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    if message.content.startswith('!info'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        await client.send_message(message.channel, 'USER:'+client.user.name)
        await client.send_message(message.channel, 'ID:'+client.user.id)
        

    elif message.content.startswith('!time'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        await client.send_message(message.channel, 'Bot Server date:'+date)
    
    elif message.content.startswith('!ver'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        await client.send_message(message.channel, 'Bot ver:'+BotVer)

    elif message.content.startswith('!translate'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        contentStr=message.content[11:]
        try:          
            translator = Translator()
            result=translator.translate(contentStr,dest='zh-cn').text
            await client.send_message(message.channel, 'Translate Result:'+result)
        except:
            await client.send_message(message.channel,'Emmmm... Something wrong?')

    elif message.content.startswith('!img'):
        if message.content=='!img':
            await client.send_message(message.channel,'Emmmm... No parameter found.')
            return
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        contentstr=message.content[5:]
        query_string=urllib.parse.quote_plus(contentstr)
        url="https://www.google.com/searchbyimage?&image_url="+query_string
        user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
        req=urllib.request.Request(url,None,{'User-Agent':user_agent})
        response=urllib.request.urlopen(req)
        page=response.read()
        soup=BeautifulSoup(page,'html.parser')
        pos=soup.find('a',attrs={'class':'_gUb'})
        if pos:
            ans=pos.getText()
            em=discord.Embed(title='Image lookup', description='possible:'+ans, colour=0xDEADBF)
            em.set_image(url=contentstr)
            await client.send_message(message.channel, embed=em)
        else:
            await client.send_message(message.channel, "No result receive")



    elif message.content.startswith('!y2b'):
        if message.content=='!y2b':
            await client.send_message(message.channel,'Emmmm... No parameter found.')
            return
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        contentstr=message.content[5:]
        query_string = urllib.parse.urlencode({"search_query" : contentstr})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        await client.send_message(message.channel, "Possible video:")
        await client.send_message(message.channel, "http://www.youtube.com/watch?v=" + search_results[0])
    
    elif message.content.startswith('!wiki'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        if message.content=='!wiki':
            await client.send_message(message.channel,'Emmmm... No parameter found.')
            return
        wikipedia.set_lang("zh")
        contentstr=message.content[6:]
        wikidir=wikipedia.search(contentstr)
        dirpayload=''
        if len(wikidir)>1:
            for line in wikidir:
                dirpayload+=line+'\n'
            em=discord.Embed(title='Wiki Search Result:',description=dirpayload,colour=0xDEADBF)
            try:
                await client.send_message(message.channel,embed=em)
            except:
                await client.send_message(message.channel,'Out of Buffer! Change the search string.')
            
            try:
                wikipg=wikipedia.page(contentstr)
                await client.send_message(message.channel,wikipg.title)
                await client.send_message(message.channel,wikipg.url)
            except:
                await client.send_message(message.channel,'Emmmm....Something wrong')
        else:
            await client.send_message(message.channel,'404 Not Found!')
        

    elif message.content.startswith('!help'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        payload="vndb|bangumi|2df string:search string in VNDB.org/bangumi.tv"+'\n'
        payload+="info:get the Bot info"+'\n'
        payload+="ver:get the Bot version"+'\n'
        payload+="time:get the Bot server time"+'\n'
        payload+="vndb|bangumi|2df direct number:Direct access the number website in VNDB.org/bangumi.tv"+'\n'
        payload+="img imgURL:Google image lookup"+'\n'
        payload+="wiki String:search in wikipedia"+'\n'
        payload+="translate String:translate string to CHS."+'\n'
        payload+="y2b string:Search the string in youtube.com"
        em=discord.Embed(title='Function List:',description=payload,colour=0xDEADBF)
        await client.send_message(message.channel, embed=em)

    elif message.content.startswith('!vndb'):
        if message.content=='!vndb' or message.content=='!vndb direct ':
            await client.send_message(message.channel,'Emmmm... No parameter found.')
            return
        elif message.content.startswith('!vndb direct '):
            contentstr=message.content[13:]
            if contentstr.startswith('v'):
                url='https://vndb.org/'+contentstr
            else:
                url='https://vndb.org/v'+contentstr
        else:
            contentstr=message.content[6:]
            urlpayload=urllib.parse.quote_plus(contentstr)
            url='https://vndb.org/v/all?sq='+urlpayload

        info=VNDBGetInfo()
        buf=info.GetPage(url)
        Result=info.ExtractInfo(buf)
        if(not buf):
            print('Get HTML is failed!')
        else:
            await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
            
            flag=Result[0]
            if flag=='List':
                
                
                if len(Result)>1:
                    if len(Result)>30:
                        em=discord.Embed(title='GameList', description='possible game:'+contentstr, colour=0xDEADBF)
                        em2=discord.Embed(title='GameList', description='possible game:'+contentstr, colour=0xDEADBF)
                        valuestr1=''
                        valuestr2=''
                        for index in range(0,30):
                            if Result[index]=='List':
                                continue
                            valuestr1+=Result[index]
                            valuestr1+='\n'
                        for index in range(31,len(Result)):
                            valuestr2+=Result[index]
                            valuestr2+='\n'
                        em.add_field(name="Game Name",value=valuestr1)
                        em2.add_field(name="Game Name",value=valuestr2)
                        try:
                            await client.send_message(message.channel,embed=em)
                            await client.send_message(message.channel,embed=em2)
                            await client.send_message(message.channel,url)
                        except:
                            await client.send_message(message.channel,'Out of Buffer! Change the search string.')
                            await client.send_message(message.channel,url)
                    else:
                        valuestr=''
                        em=discord.Embed(title='GameList', description='possible game:'+contentstr, colour=0xDEADBF)
                        for line in Result:
                            if line=='List':
                                continue
                            valuestr+=line
                            valuestr+='\n'
                        em.add_field(name="Game Name",value=valuestr)
                        try:
                            await client.send_message(message.channel,embed=em)
                            await client.send_message(message.channel,url)
                        except:
                            await client.send_message(message.channel,'Out of Buffer! Change the search string.')
                            await client.send_message(message.channel,url)
                else:
                    await client.send_message(message.channel,'find nothing')
            if flag=='Game':
                em=discord.Embed(title='GameInfo', description='Gameinfo about '+Result[2]+'/'+Result[3], colour=0xDEADBF)
                if len(Result[1])!=0:
                    em.set_image(url=Result[1])
                payload='Game Name: '+Result[2]+'/'+Result[3]+'\n'
                payload+='Aka: '+Result[5]+'\n'
                payload+='Length: '+Result[6]+'\n'
                payload+='Developer: '+Result[7]+'\n'
                payload+='Publisher: '+Result[8]+'\n'
                em.add_field(name='Basic Info:',value=payload)
                em2=discord.Embed(title='Description:', description=Result[4], colour=0xDEADBF)
                await client.send_message(message.channel,embed=em)
                try:
                    await client.send_message(message.channel,embed=em2)
                    await client.send_message(message.channel,url)
                except:
                     await client.send_message(message.channel,'Maybe too many description?')
                     await client.send_message(message.channel,url)
    
    elif message.content.startswith('!bangumi'):
        if message.content=='!bangumi' or message.content=='!bangumi direct ':
            await client.send_message(message.channel,'Emmmm... No parameter found.')
            return
        elif message.content.startswith('!bangumi direct '):
            contentstr=message.content[16:]
            url='http://bangumi.tv/subject/'+contentstr
        else:
            contentstr=message.content[9:]
            urlpayload=urllib.parse.quote_plus(contentstr)
            url='http://bangumi.tv/subject_search/'+urlpayload+'?cat=4'
        
        info=BangumiGetInfo()
        buf=info.GetPage(url)
        Result=info.ExtractInfo(buf)
        if(not buf):
            print('Get HTML is failed!')
        else:
            await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
            
            flag=Result[0]
            if flag=='List':
                em=discord.Embed(title='GameList', description='possible game:'+contentstr, colour=0xDEADBF)
                valuestr=''
                if len(Result)>1:
                    for line in Result:
                        if line=='List':
                            continue
                        valuestr+=line
                        valuestr+='\n'
                    em.add_field(name="Game Name",value=valuestr)
                    try:
                        await client.send_message(message.channel,embed=em)
                        await client.send_message(message.channel,url)
                    except:
                        await client.send_message(message.channel,'Out of Buffer! Change the search string.')
                        await client.send_message(message.channel,url)
                else:
                    await client.send_message(message.channel,'find nothing')
            if flag=='Game':
                em=discord.Embed(title='GameInfo',description='Gameinfo about '+Result[3][3:],colour=0xDEADBF)
                if len(Result[1])!=0:
                    imgUrl='http:'+Result[1]
                    #print(imgUrl)
                    em.set_image(url=imgUrl)
                payload=''
                for index in range(len(Result)):
                    if index!=0 and index!=1 and index!=2:
                        payload+=Result[index]+'\n'
                em.add_field(name='Basic Info:',value=payload)
                em2=discord.Embed(title='Description:', description=Result[2][3:], colour=0xDEADBF)
                await client.send_message(message.channel,embed=em)
                try:
                    await client.send_message(message.channel,embed=em2)
                    await client.send_message(message.channel,url)
                except:
                     await client.send_message(message.channel,'Maybe too many description?')
                     await client.send_message(message.channel,url)

    
    elif message.content.startswith('!2df'):
        if message.content=='!2df' or message.content=='!2df direct ':
            await client.send_message(message.channel,'Emmmm... No parameter found.')
            return
        elif message.content.startswith('!2df direct '):
            contentstr=message.content[12:]
            url='http://www.2dfan.com/subjects/'+contentstr
        else:
            contentstr=message.content[5:]
            urlpayload=urllib.parse.quote_plus(contentstr)
            url='http://www.2dfan.com/subjects/search?keyword='+urlpayload
        #print(url)
        try:
            info=TDFGetInfo()
            buf=info.GetPage(url)
            Result=info.ExtractInfo(buf)
        except:
            await client.send_message(message.channel,'Emmmm....Something wrong')
            print('Connect Error!')
            return
        if(not buf):
            print('Get HTML is failed!')
        else:
            await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
            
            flag=Result[0]
            if flag=='List':
                em=discord.Embed(title='GameList', description='possible game:'+contentstr, colour=0xDEADBF)
                valuestr=''
                if len(Result)>1:
                    for line in Result:
                        if line=='List':
                            continue
                        valuestr+=line
                        valuestr+='\n'
                    em.add_field(name="Game Name",value=valuestr)
                    try:
                        await client.send_message(message.channel,embed=em)
                        await client.send_message(message.channel,url)
                    except:
                        await client.send_message(message.channel,'Out of Buffer! Change the search string.')
                        await client.send_message(message.channel,url)
                else:
                    await client.send_message(message.channel,'find nothing')
            if flag=='Game':
                #print(Result)
                em=discord.Embed(title='GameInfo',description='Gameinfo about '+Result[2],colour=0xDEADBF)
                if len(Result[1])!=0:
                    imgUrl=Result[1]
                    #print(imgUrl)
                    em.set_image(url=imgUrl)
                payload=''
                for index in range(len(Result)):
                    if index!=0 and index!=1 and index!=2:
                        payload+=Result[index]
                em.add_field(name='Basic Info:',value=payload)
                await client.send_message(message.channel,embed=em)
                await client.send_message(message.channel,url)

                 
    elif message.content.startswith('!'):
        await client.send_message(message.channel,'What are you doing?')


client.run('MzY4NzA0MzcyMjgyMDk3NjY1.DMPBwA.i5k4WqVdSDnSxu84eLS28ed6QHg')
