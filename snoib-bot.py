#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord import Client
from re import findall
import asyncio
import logging
import random


class SnoibBot(Client):
    def __init__(self, channel_id):
        super().__init__()

        self._channel_id = channel_id

        self._logger = logging.getLogger('SnoibBot')
        self._logger.setLevel(logging.DEBUG)

        f = logging.Formatter('[%(levelname)s]: %(message)s')

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(f)

        fh = logging.FileHandler('snoibbot.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(f)

        self._logger.addHandler(sh)
        self._logger.addHandler(fh)

    def count_words(self, msg, list_):
        '''
        Returns the number of times all words from the list list_ shows up in the message msg
        '''
        return sum([len(findall(word, msg.lower())) for word in list_])
        # return any([fnmatch(msg, '*'+item+'*') for item in list_])

    def classify(self, message):
        msg = message.content
        print(msg)

        response = "test"

        return response

    async def on_message(self, message):
        print(message)
        if message.author == self.user:
            return

        response = None

        if f"<@!{self.user.id}" in message.content:
            self._logger.info('User has dared to mention the all-knowing Snoib bot! Smite them!')
            response = mentioned[random.randint(0, len(mentioned) - 1)]

        elif message.channel.id == self._channel_id:
            self._logger.info('Received message from {0}: {1}, classifying it.'.format(message.author.name, message.content))
            response = classify(message)

        if response:
            try:
                await message.reply(response, mention_author=True)
            except:
                await self.get_channel(self._channel_id).send(message.author.mention+' '+response)

    async def on_ready(self):
        self._logger.info(f'Logged in as {self.user.name}({self.user.id})!')


def main():
    TOKEN = ''
    CHANNEL_ID = 0

    bot = SnoibBot(CHANNEL_ID)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
