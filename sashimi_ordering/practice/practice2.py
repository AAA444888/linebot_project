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
from practice1 import initial,verify
from identify import identify
# 需要額外載入對應的函示庫
from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate,ConfirmTemplate,CarouselTemplate,CarouselColumn
app = Flask(__name__)
url = 'https://orderbot-4c7c5-default-rtdb.firebaseio.com'
fdb = firebase.FirebaseApplication(url, None)
user_ids=[]

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    order={}
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = "855/Io+qJcb4ckjL6xUuLTZghraa8DcQoVWxf8d5pcnCWTN/gnvj6UyhNhT3zFUuCe9cA4jPTGTxD2lAVlkOJ5wQCRDpu0DJTyZ2AVid62sHndS8q93X4nNiGsNklWsmDSbvfnV0CombT/3atYFlsQdB04t89/1O/w1cDnyilFU="
        secret = "1eec70f63262544199fc971730b20038"
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
            if msg in keywords:
                if "桌" in msg:
                    print(1)
                    fdb.put("/"+user,"桌號",now+msg)
                elif msg=="完成點餐":
                    print(2)
                    text='恭喜你完成點餐\n總共是\n'
                    table=fdb.get("/"+user,"桌號")
                    o=fdb.get("/"+user+"/"+table,None)
                    print(o)
                    for k,v in o.items():
                        print(k,v)
                        if k in keywords:
                            print(text)
                            text+=k
                            text+=" "
                            text+=str(v)
                            text+="份\n"
                    cost=fdb.get("/"+user+"/"+table,"金額")
                    text+="這樣總共"
                    text+=str(cost)
                    text+="元"
                    print(text)
                    text_message = TextSendMessage(text) #"hello world"
                    line_bot_api.reply_message(tk, text_message)
                elif msg=="我要拍照":
                    f=0
                    text="正在確認桌號"
                    text_message = TextSendMessage(text) #"hello world"
                    line_bot_api.reply_message(tk, text_message)
                    table=fdb.get("/"+user,"桌號")
                    now = datetime.datetime.now()
                    now = now.strftime('%Y-%m-%d %H:%M:%S')
                    if table is None:
                        text="請先選擇桌號"
                        text_message = TextSendMessage(text) #"hello world"
                        line_bot_api.push_message(user, text_message)
                    else:
                        for i in range(10):
                            if table[i]!=now[i]:
                                f=1
                        h1=now[11]+now[12]
                        h2=table[11]+table[12]
                        m1=now[14]+now[15]
                        m2=table[14]+table[15]
                        print(h1,h2)
                        print(m1,m2)
                        clock=(int(h1)-int(h2))*60+int(m1)-int(m2)
                        print(clock)
                        if clock>120 or clock<0:
                            f=1
                        if f==1:
                            text="請先選擇桌號"
                            text_message = TextSendMessage(text) #"hello world"
                            line_bot_api.push_message(user, text_message)
                        else:
                            text="已確認桌號，開始點餐"
                            user = json_data['events'][0]['source']['userId']
                            text_message = TextSendMessage(text) #"hello world"
                            #line_bot_api.push_message(user, text_message)
                            line_bot_api.push_message(user, TemplateSendMessage(
                                alt_text='CarouselTemplate',
                                template=CarouselTemplate(
                                    columns=[
                                        CarouselColumn(
                                            title='拍照點餐',
                                            text='已確認完桌號，開始點餐',
                                            actions=[
                                                URIAction(
                                                    label='點這',
                                                    uri='https://line.me/R/nv/cameraRoll/single'
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ))
                else:
                    print(3)
                    table=fdb.get("/"+user,"桌號")
                    cost=fdb.get("/"+user+"/"+table,"金額")
                    if cost is None: 
                        if msg=="天使紅蝦":
                            fdb.put("/"+user+"/"+table,"金額",200)
                        elif msg=="干貝":
                            fdb.put("/"+user+"/"+table,"金額",150)
                        else:
                            fdb.put("/"+user+"/"+table,"金額",100)
                    else:
                        if msg=="天使紅蝦":
                            cost+=200
                            fdb.put("/"+user+"/"+table,"金額",cost)
                        elif msg=="干貝":
                            cost+=150
                            fdb.put("/"+user+"/"+table,"金額",cost)
                        else:
                            cost+=100
                            fdb.put("/"+user+"/"+table,"金額",cost)
                    num=fdb.get("/"+user+"/"+table,msg)
                    if num is not None:
                        num+=1
                    else:
                        num=1
                    fdb.put("/"+user+"/"+table,msg,num) 
        elif type=='image':
            user = json_data['events'][0]['source']['userId']
            msgID = json_data['events'][0]['message']['id']  # 取得訊息 id
            message_content = line_bot_api.get_message_content(msgID)  # 根據訊息 ID 取得訊息內容
            # 在同樣的資料夾中建立以訊息 ID 為檔名的 .jpg 檔案
            with open(f'{msgID}.jpg', 'wb') as fd:
                fd.write(message_content.content)             # 以二進位的方式寫入檔案
            text=identify(msgID).replace('\n', '')
            line_bot_api.reply_message(
            tk, TextSendMessage(text))
            table=fdb.get("/"+user,"桌號")
            cost=fdb.get("/"+user+"/"+table,"金額")
            
            if cost is None: 
                if text=="天使紅蝦":
                    fdb.put("/"+user+"/"+table,"金額",200)
                elif text=="干貝":
                    fdb.put("/"+user+"/"+table,"金額",150)
                else:
                    fdb.put("/"+user+"/"+table,"金額",100)
            else:
                if text=="天使紅蝦":
                    cost+=200
                    fdb.put("/"+user+"/"+table,"金額",cost)
                elif text=="干貝":
                    cost+=150
                    fdb.put("/"+user+"/"+table,"金額",cost)
                else:
                    cost+=100
                    fdb.put("/"+user+"/"+table,"金額",cost)
            num=fdb.get("/"+user+"/"+table,text)
            if num is not None:
                num+=1
            else:
                num=1
            fdb.put("/"+user+"/"+table,text,num)
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
    