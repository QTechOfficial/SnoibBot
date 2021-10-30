#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import logging
import discord
import asyncio
from discord.ext import tasks
from re import findall
from urllib.request import urlopen

TOKEN = ''
CHANNELID = 0

#######################


logger = logging.getLogger('SnoibBot')
logger.setLevel(logging.DEBUG)
f = logging.Formatter('[%(levelname)s]: %(message)s')
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(f)
fh = logging.FileHandler('snoibbot.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(f)
logger.addHandler(sh)
logger.addHandler(fh)

client = discord.Client()

def contains(msg, list):
    return sum([len(findall(word, msg.lower())) for word in list])
    # return any([fnmatch(msg, '*'+item+'*') for item in list])

def classify(message):
    msg = message.content
    print(msg)

    response = "test"

    return response

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = None

    if f"<@!{client.user.id}" in message.content:
        logger.info('User has dared to mention the all-knowing Snoib bot! Smite them!')
        response = mentioned[random.randint(0, len(mentioned) - 1)]

    elif message.channel.id == CHANNELID:
        logger.info('Received message from {0}: {1}, classifying it.'.format(message.author.name, message.content))
        response = classify(message)

    if response:
        try:
            await message.reply(response, mention_author=True)
        except:
            await client.get_channel(CHANNELID).send(message.author.mention+' '+response)

@client.event
async def on_ready():
    logger.info('Logged in as {0}({1})!'.format(client.user.name, client.user.id))

client.run(TOKEN)
