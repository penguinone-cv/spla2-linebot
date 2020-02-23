from flask import Flask, request, abort
import urllib
import urllib.request
import json
from datetime import datetime
import re

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, MessageAction, ButtonsTemplate,
)
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def get_rule_stage(hour):
    req = urllib.request.Request("https://spla2.yuu26.com/{rule}/schedule".format(rule='league'))
    req.add_header("user-agent", "@penguinone2580")
    with urllib.request.urlopen(req) as res:
        response_body = res.read().decode("utf-8")
        response_json = json.loads(response_body.split("\n")[0])
        data = response_json["result"]
        for d in data:
            start_time = datetime.strptime(d["start"], '%Y-%m-%dT%H:%M:%S')
            end_time = datetime.strptime(d["end"], '%Y-%m-%dT%H:%M:%S')
            start_hour = start_time.strftime("%H")
            if hour == int(start_hour):
                text = "{start} ~ {end}\n{rule}\n{stage1}\t{stage2}".format(
                    start=start_time.strftime("%m/%d %H:%M"),
                    end=end_time.strftime("%m/%d %H:%M"),
                    rule=d["rule_ex"]["name"],
                    stage1=d["maps_ex"][0]["name"],
                    stage2=d["maps_ex"][1]["name"])

                return text

def check_hour(hour):
    if hour==0:
        hour = 23
    elif hour%2==0:
        hour = hour - 1
    return hour

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    receive_txt = event.message.text
    league = False
    private = False
    if ("リグマ" in receive_txt or "リーグマッチ" in receive_txt or "4タグ" in receive_txt) and "募集" in receive_txt:
        league = True

    if ("プラべ" in receive_txt or "プライベートマッチ" in receive_txt) and "募集" in receive_txt:
        private = True

    if league and private:
        league = False
        private = False

    if league:
        hour = int(re.sub("\\D", "", receive_txt))%24
        hour = check_hour(hour)
        text = get_rule_stage(hour)
        print(text)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Buttons template',
                                template=ButtonsTemplate(thumbnail_image_url='https://www.nintendo.co.jp/switch/aab6a/assets/images/battle-sec03_logo.png',
                                                        title='リーグマッチ募集',
                                                        text=text,
                                                        actions=[MessageAction(label='参加する', text='参加')])))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
