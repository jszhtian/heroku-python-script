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
from SQLServer import SQLServices
from Extraction import VNDBGetInfo
from Extraction import TDFGetInfo
from Extraction import BangumiGetInfo

import discord

def chunks(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]

BotVer='20171018'
client = discord.Client()

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

    elif message.content.startswith('!sqlusage'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        Usage=sql.Usage()
        if Usage==-1:
            await client.send_message(message.channel,'Get Usage information is failed!')
            sql.Disconnect()
            del sql
            return
        sql.Disconnect()
        del sql
        await client.send_message(message.channel, 'Usage:'+str(Usage)+'/10000')
        
    elif message.content.startswith('!listmemo'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        MemoList=sql.ListMemo(message.author.id)
        if len(MemoList)==0:
            await client.send_message(message.channel,"No memorandum in List")
        elif MemoList[0]=="SQL Query executes Fail!":
            await client.send_message(message.channel,'SQL Query executes Fail!')
            sql.Disconnect()
            del sql
            return
        else:
            #await client.send_message(message.channel,"ID||Memo")
            chks=chunks(MemoList,25)
            for chk in chks:
                out=''
                for line in chk:
                    info=line.split('||',1)
                    out+='ID:'+info[0]+'\n'
                    out+='Memo:'+info[1]+'\n'
                    out+='\n'
                await client.send_message(message.channel,embed=discord.Embed(title='Memo List:', description=out, colour=0xDEADBF))
        sql.Disconnect()
        del sql

    elif message.content.startswith('!listres'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        ResList=sql.ListRes()
        if len(ResList)==0:
            await client.send_message(message.channel,"No resources in List")
        elif ResList[0]=="SQL Query executes Fail!":
            await client.send_message(message.channel,'SQL Query executes Fail!')
            sql.Disconnect()
            del sql
            return
        else:
            #await client.send_message(message.channel,"ID||Name||Link")
            chks=chunks(ResList,25)
            for chk in chks:
                out=''
                for line in chk:
                    info=line.split('||',2)
                    out+="ID:"+info[0]+'\n'
                    out+="Name:"+info[1]+'\n'
                    out+=info[2]+'\n'
                    out+='\n'
                await client.send_message(message.channel,embed=discord.Embed(title='Resource List:', description=out, colour=0xDEADBF))
        sql.Disconnect()
        del sql
    
    elif message.content.startswith('!addres'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        RAWRES=message.content[8:]
        infolist=RAWRES.split('|',1)
        if len(infolist)!=2:
            await client.send_message(message.channel,'Parameter Error!')
            return
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        res=sql.AddRes(infolist[0],infolist[1])
        if not res:
            await client.send_message(message.channel,'SQL Query executes Fail!')
            sql.Disconnect()
            del sql
            return
        else:
            await client.send_message(message.channel,"Add Res:"+infolist[0])
        sql.Disconnect()
        del sql

    elif message.content.startswith('!updmemo'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        RAWRES=message.content[9:]
        infolist=RAWRES.split('|',1)
        if len(infolist)!=2:
            await client.send_message(message.channel,'Parameter Error!')
            return
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        res=sql.UpdMemo(infolist[0],message.author.id,infolist[1])
        if not res:
            await client.send_message(message.channel,'SQL Query executes Fail!')
            sql.Disconnect()
            del sql
            return
        else:
            await client.send_message(message.channel,"UPD Memo:"+infolist[0])
        sql.Disconnect()
        del sql

    elif message.content.startswith('!delres'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        RAWRES=message.content[8:]
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        res=sql.DelRes(RAWRES)
        if not res:
            await client.send_message(message.channel,'SQL Query executes Fail!')
            sql.Disconnect()
            del sql
            return
        else:
            await client.send_message(message.channel,"DEL Res:"+RAWRES)
        sql.Disconnect()
        del sql

    elif message.content.startswith('!addmemo'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        RAWStr=message.content[9:]
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        res=sql.AddMemo(message.author.id,RAWStr)
        if not res:
            await client.send_message(message.channel,'SQL Query executes Fail!')
            sql.Disconnect()
            del sql
            return
        else:
            await client.send_message(message.channel,"Add Memo:"+RAWStr)
        sql.Disconnect()
        del sql

    elif message.content.startswith('!delmemo'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        RAWRES=message.content[9:]
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        res=sql.DelMemo(message.author.id,RAWRES)
        if not res:
            await client.send_message(message.channel,'SQL Query executes Fail!')
            sql.Disconnect()
            del sql
            return
        else:
            await client.send_message(message.channel,"DEL Memo:"+RAWRES)
        sql.Disconnect()
        del sql

    elif message.content.startswith('!sqlcleanup'):
        await client.send_message(message.channel,'<@'+str(message.author.id)+'>')
        sql=SQLServices()
        ret=sql.Connect()
        if not ret:
            await client.send_message(message.channel,'Connect to SQL Server is failed!')
            sql.Disconnect()
            del sql
            return
        res=sql.CleanUp()
        if not res:
            await client.send_message(message.channel,'Cleanup is failed!')
            sql.Disconnect()
            del sql
            return
        sql.Disconnect()
        del sql
        await client.send_message(message.channel, 'CleanUp finish!')

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
        payload+="sqlusage:Get information about SQL server usage."+'\n'
        payload+="sqlcleanup:delete all old records(>45 Days)."+'\n'
        payload+="addres resName|resLink: add resource record"+'\n'
        payload+="delres ID:Delete the res record"+'\n'
        payload+="addmemo string:add string to memo"+'\n'
        payload+="delmemo ID:Delete the memo record"+'\n'
        payload+="updmemo ID|string:Update the memo record with ID and record"+'\n'
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
                    chks=chunks(Result,30)
                    for chk in chks:
                        valuestr=''
                        em=discord.Embed(title='GameList', description='possible game:'+contentstr, colour=0xDEADBF)
                        for li in chk:
                            if li=='List':
                                continue
                            valuestr+=li
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


client.run('MzY4NzA0MzcyMjgyMDk3NjY1.DMXEuw.t_gMfrr_YgCKNmcn_9JG5OfrEVE')
