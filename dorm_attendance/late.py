def students():
    xxx=[]
    xx=[]
    from firebase import firebase
    import datetime
    url = 'https://linebot-10933-default-rtdb.firebaseio.com/'
    fdb = firebase.FirebaseApplication(url, None)
    user_data = fdb.get('/',None)
    for  k,v in user_data.items():
        xx.append(v["時間"])
        x="2"
        x+=v["樓層"][0]
        x+=v["房號"]
        x+="-"
        x+=v["床號"]
        print(x)
        xxx.append(x)
    #     for types, values in v.items():
    print(xx)
    print(xxx)
            
    import pandas as pd

    # 创建一个示例 DataFrame
    df = pd.DataFrame({
        'time': xx,
        'room': xxx
    })

    # 指定要写入的 Excel 文件路径
    file_path = 'dorm.xlsx'

    # 使用 ExcelWriter 写入新的工作表
    today = datetime.datetime.now()
    today = today.strftime('%Y-%m-%d'+"點名紀錄")
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=today, index=False)

    print(f"New sheet 'NewSheet' added to {file_path}")


# import os
# import openpyxl
# if os.path.exists('dorm.xlsx')!=True:
#     wb = openpyxl.Workbook()    # 建立空白的 Excel 活頁簿物件
#     wb.save('dorm.xlsx') 
# wb = openpyxl.load_workbook('dorm.xlsx', data_only=True)

# s3 = wb.create_sheet('工作表1')     # 新增工作表 3
# data = xxx  # 二維陣列資料
# for i in data:
#     s3.append(i)                   # 逐筆添加到最後一列

# wb.save('dorm.xlsx')
# x=""
# for user in user_ids:
#     x+= fdb.get('/','樓層')
#     x+= fdb.get('/','房號')
#     x+= fdb.get('/','床號')
# print(x) #?