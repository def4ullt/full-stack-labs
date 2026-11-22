"""Long polling Telegram Bot API. Токен читається з оточення."""
import json
import logging
import os
import time
from urllib.request import Request,urlopen
from urllib.error import URLError
from quiz import Quiz

def run(token):
    sessions={}
    offset=0
    def api(method,params):
        request=Request(f"https://api.telegram.org/bot{token}/{method}",data=json.dumps(params).encode(),headers={"Content-Type":"application/json"})
        with urlopen(request,timeout=40) as reply:
            return json.load(reply)["result"]
    while True:
        try:
            for update in api("getUpdates",{"offset":offset,"timeout":25,"allowed_updates":["message"]}):
                message=update.get("message",{})
                if "text" in message:
                    chat=message["chat"]["id"]
                    key=(chat,message["from"]["id"])
                    text=message["text"].strip()
                    if text.split("@")[0]=="/start":
                        sessions[key]=Quiz()
                        result=sessions[key].prompt()
                    elif key in sessions:
                        result=sessions[key].answer(text)
                        if sessions[key].index==10:
                            del sessions[key]
                    else:
                        result="Розпочни тест командою /start."
                    api("sendMessage",{"chat_id":chat,"text":result})
                offset=update["update_id"]+1
        except (TimeoutError,URLError):
            logging.warning("Немає відповіді Telegram. Повтор через 5 секунд.")
            time.sleep(5)
if __name__=="__main__":
    run(os.environ["BOT_TOKEN"])
