import os
import requests


class DiscordConnections:
    def __init__(self):
        token = os.environ["DISCORD_TOKEN_BOT"]

        self.headers = {
            "Authorization" : token
        }

    def flipbok_notifier(self):
        channel_id = "1038419404184100909"

        endpoint = f"https://discordapp.com/api/channels/{channel_id}/messages"

        user_id = "309690259753533440"

        payload = {
            "content" : f"<@{user_id}> a subido un flipbook para revisar.", 
        }

        post = requests.post(endpoint,json=payload, headers=self.headers)
        
        