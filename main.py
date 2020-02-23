from flask import Flask, request, abort

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

    text='v('ω')v'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text),
        TemplateSendMessage(alt_text='Buttons template',
                            template=ButtonsTemplate(thumbnail_image_url='https://www.nintendo.co.jp/switch/aab6a/assets/images/battle-sec03_logo.png',
                                                     title='リーグマッチ募集',
                                                     text='選択してください',
                                                     actions=[MessageAction(label='参加する', text='参加')])))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
