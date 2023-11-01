from flask import Flask, request
# 載入 json 標準函式庫，處理回傳的資料格式
import json
# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot import LineBotApi, WebhookHandler
from firebase import firebase
import threading
from hw import initial,verify
from identify import identify
# 需要額外載入對應的函示庫
from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate,ConfirmTemplate,CarouselTemplate,CarouselColumn
app = Flask(__name__)
import json

def get_data():
    with open('data.json','r') as f:
        data = json.load(f)
    return  data
url = get_data()['url']
fdb = firebase.FirebaseApplication(url, None)
user_ids=[]

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        data = get_data()
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = data["access_token"]
        secret = data['secret']
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        print(type)
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            user = json_data['events'][0]['source']['userId']
            print(msg)  
            from key import call
            import datetime
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            keywords=call()
            from late import students
            if msg in keywords:
                if "F" in msg:
                    fdb.put("/"+user,"樓層",msg)
                elif "0" in msg:
                    fdb.put("/"+user,"房號",msg)    
                elif msg.isdigit():
                    fdb.put("/"+user,"床號",msg)
                    fdb.put("/"+user,"時間",now)
                    students()
        elif type=='image':
            msgID = json_data['events'][0]['message']['id']  # 取得訊息 id
            message_content = line_bot_api.get_message_content(msgID)  # 根據訊息 ID 取得訊息內容
            # 在同樣的資料夾中建立以訊息 ID 為檔名的 .jpg 檔案
            with open(f'{msgID}.jpg', 'wb') as fd:
                fd.write(message_content.content)             # 以二進位的方式寫入檔案
            line_bot_api.reply_message(
            tk, TextSendMessage(text=identify(msgID).replace('\n', '')))
            # reply = '圖片儲存完成！' 
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

def running():
    app.run()
if __name__ == "__main__":
    driver=initial()
    # port = int(os.environ.get('PORT', 80))
    t1=threading.Thread(target = running)
    t=threading.Thread(target = verify, args = (driver,))
    t.start()
    t1.start()
    