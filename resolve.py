import logging
import re
from typing import Union

import pyrogram
from pyrogram import raw, utils
from pyrogram.errors import PeerIdInvalid

log = logging.getLogger(__name__)

# Constants for Peer ID validation
MIN_CHANNEL_ID = -1002147483647
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID = -2147483647
MAX_USER_ID_OLD = 2147483647
MAX_USER_ID = 999999999999

def get_peer_type(peer_id: int) -> str:
    """
    Determine the type of peer (user, chat, or channel) based on the peer ID.

    Args:
        peer_id (int): The peer ID.

    Returns:
        str: The type of the peer ('user', 'chat', or 'channel').

    Raises:
        ValueError: If the peer ID is invalid.
    """
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"
        if peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"
    raise ValueError(f"Invalid peer ID: {peer_id}")


class ResolvePeer:
    def __init__(self, client: "pyrogram.Client") -> None:
        """
        Initialize the ResolvePeer utility.

        Args:
            client (pyrogram.Client): The Pyrogram client instance.
        """
        self.client = client

    async def resolve_peer(
        self, peer_id: Union[int, str]
    ) -> Union[raw.base.InputPeer, raw.base.InputUser, raw.base.InputChannel]:
        """
        Resolve a peer ID into its corresponding InputPeer type.

        Args:
            peer_id (Union[int, str]): The peer ID, username, or phone number.

        Returns:
            Union[raw.base.InputPeer, raw.base.InputUser, raw.base.InputChannel]: 
                The resolved InputPeer object.

        Raises:
            PeerIdInvalid: If the peer ID cannot be resolved.
            ConnectionError: If the client is not connected.
        """
        if not self.client.is_connected:
            raise ConnectionError("Client has not been started yet.")

        # Try to fetch peer directly from storage
        try:
            return await self.client.storage.get_peer_by_id(peer_id)
        except KeyError:
            pass

        # Resolve username or phone number
        if isinstance(peer_id, str):
            peer_id = peer_id.strip().lower()

            if peer_id in ("self", "me"):
                return raw.types.InputPeerSelf()

            # Remove non-numeric characters if the input is a phone number
            peer_id = re.sub(r"[@+\s]", "", peer_id)

            try:
                int(peer_id)  # Check if it is numeric
            except ValueError:
                # Handle as a username
                try:
                    return await self.client.storage.get_peer_by_username(peer_id)
                except KeyError:
                    await self.client.invoke(
                        raw.functions.contacts.ResolveUsername(username=peer_id)
                    )
                    return await self.client.storage.get_peer_by_username(peer_id)
            else:
                # Handle as a phone number
                try:
                    return await self.client.storage.get_peer_by_phone_number(peer_id)
                except KeyError:
                    raise PeerIdInvalid

        # Resolve numeric peer ID
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
        elif peer_type == "channel":
            await self.client.invoke(
                raw.functions.channels.GetChannels(
                    id=[
                        raw.types.InputChannel(
                            channel_id=utils.get_channel_id(peer_id),
                            access_hash=0,
                        )
                    ]
                )
            )

        # Retry fetching from storage after invocation
        try:
            return await self.client.storage.get_peer_by_id(peer_id)
        except KeyError:
            raise PeerIdInvalid
