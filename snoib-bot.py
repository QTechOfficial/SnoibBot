#!/usr/bin/env python
# -*- coding: utf-8 -*-

from discord import Client
from re import findall
import asyncio
import json
import logging
import os
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

        self.load_classifications('classifications.json')
        self.load_responses('responses.json')


    def load_classifications(self, name):
        if os.path.exists(name):
            with open(name, 'r') as f:
                self.classifications = json.load(f)
        else:
            raise RuntimeError(f'{name} does not exist!')

    def load_responses(self, name):
        if os.path.exists(name):
            with open(name, 'r') as f:
                self.responses = json.load(f)
        else:
            raise RuntimeError(f'{name} does not exist!')

    def count_words(self, msg, list_):
        '''
        Returns the number of times all words from the list list_ shows up in the message msg
        '''
        return sum([len(findall(word, msg.lower())) for word in list_])
        # return any([fnmatch(msg, '*'+item+'*') for item in list_])

    def classify(self, message):
        msg = message.content

        scores = {}

        self._logger.debug('Message classification:')
        for c in self.classifications:
            scores[c] = self.count_words(msg, c)
            self._logger.debug(f'\t{c} points: {scores[c]}')

        winner = max(scores, key=scores.get)
        self._logger.debug(f'{winner} wins!')

        response = self.responses[winner][random.randint(0, len(self.responses[winner]) - 1)]

        #response = "test"

        return response

    async def on_message(self, message):
        if message.author == self.user:
            return

        response = None

        if f"<@!{self.user.id}" in message.content:
            self._logger.info('User has dared to mention the all-knowing Snoib bot! Smite them!')
            response = self.responses["mentioned"][random.randint(0, len(self.responses["mentioned"]) - 1)]

        elif message.channel.id == self._channel_id:
            self._logger.info('Received message from {0}: {1}, classifying it.'.format(message.author.name, message.content))
            response = self.classify(message)

        if response:
            try:
                await message.reply(response, mention_author=True)
            except:
                await self.get_channel(self._channel_id).send(message.author.mention+' '+response)

    async def on_ready(self):
        self._logger.info(f'Logged in as {self.user.name}({self.user.id})!')


def main():
    if not os.path.exists('secrets.json'):
        # If the secrets file doesn't exist, make a new one
        with open('secrets.json', 'w') as f:
            secrets = {
                    'token': '',
                    'channel_id': 0,
            }
            json.dump(secrets, f, indent=2)
        raise RuntimeError('Please fill in secrets.json')

    secrets = None
    with open('secrets.json', 'r') as f:
        secrets = json.load(f)

    if secrets:
        bot = SnoibBot(secrets['channel_id'])
        bot.run(secrets['token'])
    else:
        raise RuntimeError('Secrets.json failed to load somehow')


if __name__ == '__main__':
    main()
