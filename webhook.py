import requests, json

class webhook_sender:
    async def webhook_send(self, webhook_url, name, picture_url, message):
        if name == "no" and picture_url == "no":
            main_content = {
                            'content': message,
                        }
        else:
            main_content = {
                            'username': name,
                            'avatar_url': picture_url,
                            'content': message,
                        }
                    
        headers      = {'Content-Type': 'application/json'}

        response     = requests.post(webhook_url, json.dumps(main_content), headers=headers)
    