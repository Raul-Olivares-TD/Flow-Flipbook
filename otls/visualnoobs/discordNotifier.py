import hou
import os
import requests


class DiscordConnections:
    def __init__(self):
        token = os.environ["DISCORD_TOKEN_BOT"]

        self.headers = {
            "Authorization" : token
        }

    def flipbok_notifier(self):
        """Creates the flipbook upload notification for send it at discord."""
        
        channel_id = os.environ["DISCORD_CHANNEL"]
    
        endpoint = f"https://discordapp.com/api/channels/{channel_id}/messages"

        user_id = os.environ["DISCORD_USER"]
        
        project = hou.pwd().parm("project").evalAsString()
        task = hou.pwd().parm("task").evalAsString()

        payload = {
            "content" : f"**{user_id}** uploaded a new flipbook version to "
            f"review of the task `{task}` from the project `{project}`", 
        }

        post = requests.post(endpoint,json=payload, headers=self.headers)
        
