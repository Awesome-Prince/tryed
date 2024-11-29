from pyrogram import Client, idle
from config import *
import sys
from resolve import ResolvePeer
import asyncio
from time import time

# List of channels to subscribe
FSUB = [FSUB_1, FSUB_2]

class ClientLike(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_message_time = {}

    async
