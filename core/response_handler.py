import asyncio

from commands import Commands
from utils.message import Message
from core.restapi import *

class ResponseHandler:
    def __init__(self, response: dict, BOT_TOKEN: str):
        self.TOKEN = BOT_TOKEN
        self.__handler(response)

    def __handler(self, response: dict):
        res = response['t']
        if res == "MESSAGE_CREATE":
            self.__parser(response)
        elif res == "GUILD_CREATE":
            pass
        elif res == "INTERACTION_CREATE":
            if response['d']["type"] == 3:
                data = response['d']["data"]
                interaction_id = response['d']["id"]
                interaction_token = response['d']["token"]

                callback = ComponentCallback(self.TOKEN, data, interaction_id, interaction_token)
                callback.type4()
        else:
            print(response)

    def __parser(self, response: dict):
        author = response['d']["author"]
        del author["public_flags"]
        del author["discriminator"]
        del author["avatar"]

        content = response['d']["content"]
        message_id = response['d']["id"]
        channel_id = response['d']["channel_id"]

        msg = Message(author, content, message_id, channel_id)
        Commands(msg, self.TOKEN)

#https://discord.com/developers/docs/interactions/receiving-and-responding#responding-to-an-interaction
class ComponentCallback:
    def __init__(self, BOT_TOKEN, data, id, token):
        self.BOT_TOKEN = BOT_TOKEN
        self.interaction_id = id
        self.interaction_token = token

    def type4(self): #DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
        payload = {}
        payload["type"] = 4
        payload["data"] = {
            "content": "굳"
        }

        http = RestAPI(self.BOT_TOKEN)
        asyncio.create_task(http.request(Route("POST", "/interactions/{}/{}/callback".format(self.interaction_id, self.interaction_token)),payload=payload))

    def type6(self): #DEFERRED_UPDATE_MESSAGE
        pass

    def type7(self): #UPDATE_MESSAGE
        pass

    def type8(self): #APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
        pass