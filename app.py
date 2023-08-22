from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests
from bs4 import BeautifulSoup

#======python的函數庫==========
import tempfile, os
import datetime
import time
import random
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv('OPENAI_API_KEY')


# 監聽所有來自 /callback 的 Post Request
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

# 圖片串
img_urls = ['https://megapx-assets.dcard.tw/images/12d3fe91-e447-44f7-9086-6ec1642b9656/full.jpeg',
            'https://i.ibb.co/D4wgZ4c/S-39297092.jpg',
            'https://i.ibb.co/dgc3xSM/S-39297094.jpg',
            'https://i.ibb.co/S6VL2wq/S-39297129.jpg',
           'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1604631271916.jpg',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZFjmvS6JMNuUoPidFc3MvaOXKHP78IA7kLA&usqp=CAU'
           'https://megapx-assets.dcard.tw/images/7db8fae0-c60c-42a8-9687-ce27c1cb8aee/full.png']

# 获得 Dcard 热门帖子
def get_dcard_hot_posts():
    url = 'https://www.dcard.tw/f'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    posts = []
    for post in soup.find_all('h2', class_='tgn9uw-3'):
        title = post.text.strip()
        posts.append(title)
    return posts

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    random_image_url = random.choice(img_urls)
    image_message = ImageSendMessage(original_content_url=random_image_url,preview_image_url=random_image_url)
    msg = event.message.text
    if '你好' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='我不好'))
    if '請問' in msg:
        num=random.randint(0,3)
        img_url=reply_img(num)
        img_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
        line_bot_api.reply_message(event.reply_token,img_message)
    if '行事曆' in msg:
        message = TextSendMessage(text='國立中興大學112學年度行事曆\n'
                                  'https://www.nchu.edu.tw/calendar/')
        line_bot_api.reply_message(event.reply_token, (image_message,message))
    if '推薦排課系統' in msg:
        message = TextSendMessage(text='推薦排課系統\n'
                                  'https://nchuclass.axisflow.biz/Login')
        line_bot_api.reply_message(event.reply_token, (image_message,message))
    if '關於我' in msg:
        message = TextSendMessage(text='🎈作者暑假太無聊所製作\n'
                                  '🎈系統啟動需要時間，如長時間已讀不回，請耐心等候\n'
                                  '🎈題材內容絕無參考112新生群製作;\n'
                                  '🎈如有雷同，就代表你也挺暴躁的')
        line_bot_api.reply_message(event.reply_token, message)
    if '選課推薦' in msg:
        message = TextSendMessage(text='請善用網路\n'
                                  'https://www.dcard.tw/search?query=%E9%81%B8%E8%AA%B2&forum=nchu')
        line_bot_api.reply_message(event.reply_token, [image_message ,message] )
    if '新生EZ come' in msg:
        message = TextSendMessage(text='🎈單一簽證入口：\n'
                                  'https://portal.nchu.edu.tw/portal/\n'
                                  '🎈帳號：學號\n'
                                  '🎈密碼：身分證開頭字母大小寫＋身分證後4碼＋生日4碼\n\n'
                                  '🎈左側選單即有入口')
        line_bot_api.reply_message(event.reply_token, (image_message,message))
    if '公車' in msg:
        message = TextSendMessage(text='【FMOP｜臺中公車通】\n'
                                  'https://www.dcard.tw/f/nchu/p/252906645')
        line_bot_api.reply_message(event.reply_token, (image_message,message))
    if 'Dcard' in msg:
        hot_posts = get_dcard_hot_posts()
        hot_posts_str = '\n'.join(hot_posts)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hot_posts_str))
    else:
        message = TextSendMessage(text='收到')
        line_bot_api.reply_message(event.reply_token, (image_message,message))
#        GPT_answer = GPT_response(msg)
#        print(GPT_answer)
#        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))


@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    message = TextSendMessage(text='🎈作者暑假太無聊所製作\n'
                                  '🎈系統啟動需要時間，如長時間已讀不回，請耐心等候\n'
                                  '🎈題材內容絕無參考112新生群製作;\n'
                                  '🎈如有雷同，就代表你也挺暴躁的')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
