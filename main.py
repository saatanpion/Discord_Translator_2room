import asyncio
import os
import re

from async_google_trans_new import AsyncTranslator
import discord
import aiohttp
import ujson

client = discord.Client(activity=discord.Game(name='neko2.net/juroom_ug'))
g = AsyncTranslator(url_suffix='co.jp')

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

CHANNEL1_ID = int(os.environ['CHANNEL1_ID'])
CHANNEL1_URL = os.environ['CHANNEL1_URL']
CHANNEL1_LANG = os.environ['CHANNEL1_LANG']

CHANNEL2_ID = int(os.environ['CHANNEL2_ID'])
CHANNEL2_URL = os.environ['CHANNEL2_URL']
CHANNEL2_LANG = os.environ['CHANNEL2_LANG']

try:
    GAS_URL = os.environ['GAS_URL']
except:
    GAS_URL = ''

try:
    IGNORE_ID = os.environ['IGNORE_ID']
    l = IGNORE_ID.split(':')
    if len(l) >= 1:
        ignore_ids = [int(id) for id in l]
    else:
        ignore_ids = []
except:
    ignore_ids = []

del_word = [r"<a?:\w+?:\d+?>",r"<@! \d+>",r"^(.)\1+$",r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+",
    r"^!.*",r"^w$",r"^ｗ$",r"ww+",r"ｗｗ+",r"^\s+",r"\s+$"]

del_word_compiled = [re.compile(w) for w in del_word]

async def gas_translate(msg, lang_tgt, lang_src):
    gas_use = False
    params = {
        'text' : msg,
        'target' : lang_tgt,
        'source' : lang_src
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(GAS_URL, params=params) as r:
            if r.status == 200:
                js = await r.json()
                if js['code'] == 200:
                    translated_text = js.get('text')
                    gas_use = True
            return translated_text, gas_use

async def web_hook(message, msg, url, author, thumbnail):
    headers = {'Content-Type': 'application/json'}
    data = {
        "username"   : author,
        "content"    : msg,
        "avatar_url" : thumbnail
    }
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.post(url, headers=headers, json=data) as res:
            if res.status != 204:
                await message.channel.send('Webhookの送信に失敗しました')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.channel.id != CHANNEL1_ID and message.channel.id != CHANNEL2_ID:
        return
    
    if message.author.id in ignore_ids:
        return
    
    msg = message.content
    for r in del_word_compiled:
        msg = r.sub('', msg)
    
    display_name = message.author.display_name
    author_thumbnail = message.author.avatar_url.BASE + message.author.avatar_url._url
    
    if message.channel.id == CHANNEL1_ID:
        url = CHANNEL2_URL
        lang_src = CHANNEL1_LANG
        lang_tgt = CHANNEL2_LANG
    elif message.channel.id == CHANNEL2_ID:
        url = CHANNEL1_URL
        lang_src = CHANNEL2_LANG
        lang_tgt = CHANNEL1_LANG

    if len(msg) <= 1:
        msg = message.content
        await web_hook(message, msg, url, display_name, author_thumbnail)
    else:
        d_task = asyncio.create_task(g.detect(msg))
        detect = await d_task
        detect = detect[0]
        
        if detect == lang_tgt:
            msg = message.content
            await web_hook(message, msg, url, display_name, author_thumbnail)
            return
        
        translated = ''
        gas_use = False
        
        if GAS_URL:
            translated, gas_use = await gas_translate(msg, lang_tgt, lang_src)
        if not translated:
            trans_task = asyncio.create_task(g.translate(msg, lang_tgt,lang_src))
            translated = await trans_task
        
        if not translated:
            return
        
        p = f'({display_name}){msg}:{translated}'
        if gas_use:
            p = p + '(GAS)'
        else:
            p = p + '(No GAS)'
        print(p)
        await web_hook(message, translated, url, display_name, author_thumbnail)

client.run(DISCORD_TOKEN)