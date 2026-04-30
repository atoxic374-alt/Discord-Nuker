import requests as req, os, random


from Plugins.logger import Logger



class Tools:
    @staticmethod
    def auth_headers(token: str):
        cleaned = token.strip()
        # Only Self-bot headers (no "Bot " prefix)
        return {"Authorization": cleaned}

    @staticmethod
    def request_with_auth(method: str, url: str, token: str, **kwargs):
        base_headers = kwargs.pop("headers", {})
        headers = {**Tools.auth_headers(token), **base_headers}
        response = req.request(method, url, headers=headers, **kwargs)
        return response, headers

    @staticmethod
    def check_token(token: str):
        # Direct check for self-bot token
        response, _ = Tools.request_with_auth("GET", "https://discord.com/api/v10/users/@me", token)
        if response.status_code == 200:
            return True
        Logger.Error.error("Invalid Self-bot token %s" % token)
        return False
    
    @staticmethod
    def get_guilds(token: str):
        url = Tools.api("users/@me/guilds")

        request, _ = Tools.request_with_auth("GET", url, token, headers={"Content-Type": "application/json"})

        if request.status_code != 200:
            return []

        guilds = request.json()
        if not isinstance(guilds, list) or len(guilds) == 0:
            return []

        return [[i["id"], i["name"]] for i in guilds]
    


    @staticmethod
    def proxy():
        if os.path.exists("./proxies.txt"):
            with open("./proxies.txt", "r") as file:
                lines = file.readlines()

                if len(lines) != 0:
                    p = random.choice(
                        [i.strip() for i in lines]
                    )
                    return {"http": p, "https": p}
        else:
            return None
    
    @staticmethod
    def api(endpoint: str):
        base_api = "https://discord.com/api/v10/"
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]

        return base_api+endpoint 
    
    @staticmethod
    async def break_limit(base_api: str, token: str, return_full_data: bool = False):
        chunk_size = 1000

        users = []

        while True:
            parm = "?limit=%s" % chunk_size
            if len(users) != 0:
                last_id = users[-1]["user"]["id"] if isinstance(users[-1], dict) and "user" in users[-1] else (users[-1]["id"] if isinstance(users[-1], dict) else users[-1])
                parm+="&after=%s" % last_id
            
            r, _ = Tools.request_with_auth("GET", base_api+parm, token)
            if r.status_code == 200:
                data = r.json()
                if not data: break
                
                if return_full_data:
                    users += data
                else:
                    try:
                        ids = [i["user"]["id"] for i in data]
                    except (KeyError, TypeError):
                        ids = [i["id"] for i in data]
                    users += ids

                if len(data) < chunk_size: break
            else:
                break
        
        return users

    @staticmethod
    def chunker(text, chunk_size: int) -> list:
        length = len(text)
        num = 0
        chunks = []

        while num < len(text):
            chunks.append(text[num:length-(length-(chunk_size))+num:])
            num+=chunk_size

        return chunks
    
    @staticmethod
    def information(guild_id: str, token: str):
        url = Tools.api("users/@me")
        user, headers = Tools.request_with_auth("GET", url, token)

        url = Tools.api(f"/guilds/{guild_id}")
        guild = req.get(url, headers=headers)


        info_dict = {
            "user": user.json(),
            "guild": guild.json()
        }
        return info_dict
