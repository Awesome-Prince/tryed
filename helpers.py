async def get_chats(client):
    """
    Get the subscription channels and generate invite links.
    """
    global chats
    if not chats:
        try:
            chats = [await client.get_chat(FSUB_1), await client.get_chat(FSUB_2)]
            new_links = []
            for chat in chats:
                invite_link = await client.create_chat_invite_link(chat.id, creates_join_request=True)
                new_links.append(invite_link.invite_link)
            for idx, chat in enumerate(chats):
                chat.invite_link = new_links[idx]
        except Exception as e:
            print(f"Error in get_chats function: {e}")
            return None  # Properly handle errors to avoid NoneType issues
    return chats
