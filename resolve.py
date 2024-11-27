import logging
import re
from typing import Union

import pyrogram
from pyrogram import raw, utils
from pyrogram.errors import PeerIdInvalid

log = logging.getLogger(__name__)

# Constants for peer id ranges
MIN_CHANNEL_ID = -1002147483647
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID = -2147483647
MAX_USER_ID_OLD = 2147483647
MAX_USER_ID = 999999999999

def get_peer_type(peer_id: int) -> str:
    """Determine the peer type based on peer_id value."""
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"
        if peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"
    raise ValueError(f"Peer id invalid: {peer_id}")

class ResolvePeer:
    def __init__(self, client: pyrogram.Client) -> None:
        self.client = client

    async def resolve_peer(
        self, 
        peer_id: Union[int, str]
    ) -> Union[raw.base.InputPeer, raw.base.InputUser, raw.base.InputChannel]:
        """
        Get the InputPeer of a known peer id. Useful when working with raw Telegram API methods.
        """
        if not self.client.is_connected:
            raise ConnectionError("Client has not been started yet")

        try:
            return await self.client.storage.get_peer_by_id(peer_id)
        except KeyError:
            if isinstance(peer_id, str):
                if peer_id in {"self", "me"}:
                    return raw.types.InputPeerSelf()

                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return await self.client.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        await self.client.invoke(
                            raw.functions.contacts.ResolveUsername(username=peer_id)
                        )
                        return await self.client.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return await self.client.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid

            peer_type = get_peer_type(peer_id)

            if peer_type == "user":
                await self.client.fetch_peers(
                    await self.client.invoke(
                        raw.functions.users.GetUsers(
                            id=[raw.types.InputUser(user_id=peer_id, access_hash=0)]
                        )
                    )
                )
            elif peer_type == "chat":
                await self.client.invoke(
                    raw.functions.messages.GetChats(id=[-peer_id])
                )
            else:
                await self.client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[raw.types.InputChannel(channel_id=utils.get_channel_id(peer_id), access_hash=0)]
                    )
                )

            try:
                return await self.client.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid