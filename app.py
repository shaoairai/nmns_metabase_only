from flask import Flask, render_template,request,Blueprint
# from flask_admin impdockedrort Admin
import json
import requests
import json
# app = Flask(__name__)

# 上傳檔案、辨識
import os
from flaskapp import app
from api import callapi,callxcreen,getimage
import urllib.request
from queue import Queue
import time
# from draw import draw,drawxcreen,cv2ImgAddText
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template
import threading
# import numpy as np
# import cv2
import json
import pathlib

import jwt
import time

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# find_face = Blueprint("find_face", __name__, template_folder="../find_face/templates",
#                    static_folder="../find_face/static")

@app.route("/")
@app.route("/main")
def main():
    # You'll need to install PyJWT via pip 'pip install PyJWT' or your project packages file


    METABASE_SITE_URL = "http://nmnsmetabase.intemotech.com"
    METABASE_SECRET_KEY = "df5f5d311d42a873024850f111be452f525b83c8e1cc2c5e0a74f4acf9db3bef"

    payload = {
    "resource": {"dashboard": 40},
    "params": {
        
    },
    "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"

    return render_template("main.html",iframeUrl=iframeUrl)

# # 上傳檔案、辨識
# @app.route('/uploadcustomfile', methods=['POST'])
# def upload_image():
#     # 取得目前檔案所在的資料夾 
#     SRC_PATH =  pathlib.Path(__file__).parent.absolute() # SRC_PATH 值為 '/app'
#     UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads') # UPLOAD_FOLDER 值為 '/app/static/uploads'

#     try:
#         file = request.files['sendfile'] # 取得 AJAX 傳來的整張圖片
#         file_names = []
#         file_names.append(file.filename)
#         if file.filename != '': # 如果取得到圖片的檔名
#             # 驗證檔案型態
#             isAllowedExtensions = allowed_file(file.filename)
#             # 驗證成功
#             if isAllowedExtensions:
#                 file.save(os.path.join(UPLOAD_FOLDER, file.filename)) # 圖片儲存路徑
#                 return {'states': "success",'msg':"上傳成功","data":file_names},200
#             else:
#                 return {'states': "error",'msg':"不支援上傳此副檔名"},400
#     except BaseException as e:
#         return {'states': 'error','msg':"{}".format(e)},400


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# saas_demo 原有的 POST 方法
# @app.route('/uploadfilev1', methods=['POST'])
# def upload_image_v1():
#     q = Queue()
#     if 'files[]' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     apikey = ""
#     files = request.files.getlist('files[]')
#     selecttype = request.form.getlist('type')
#     apikey = request.form.get('apikey')
#     file_names = []
#     filethread = []
#     apidatalist = []
#     if 'clear' in selecttype:
#         for i in range(10):
#             thread = threading.Thread(
#             target=callxcreen, args=('clear.png', ['xcreen'], q,apikey))
#             thread.start()
#             filethread.append(thread)
#         for item in filethread:
#             item.join()
#             apidatalist.append(q.get())
#         apidatalist = []
#         filethread = []
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = str(time.time())+secure_filename(file.filename)
#             file_names.append(filename)
#             path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(path)

#             thread = threading.Thread(
#                 target=callapi, args=(path, selecttype, q,apikey))
#             thread.start()
#             filethread.append(thread)
#             if 'xcreen' in selecttype:
#                 thread = threading.Thread(
#                 target=callxcreen, args=(path, selecttype, q,apikey))
#                 thread.start()
#                 filethread.append(thread)
#                 thread.join()

#     for item in filethread:
#         item.join()
#         apidatalist.append(q.get())

#     for item in apidatalist:
#         mydata = json.loads(item['data'])
#         if 'data' in mydata:
#             for mydataitem in mydata['data']:
#                 if 'super_resolution_data' in mydataitem:
#                     superresolution = mydataitem['super_resolution_data']
#                     for superresolutionkey in superresolution:
#                         for url in superresolution[superresolutionkey]:
#                             name = getimage(url)
#                             file_names.append(name)



#         if item['type'] == 'yolor':
#             print(item['data'])
#             # draw(path=item['path'], data=item['data'])
#             json.loads(item['data'])
        
#     print(item['data'])
#     return {"data": item['data']},200
        # elif item['type'] == 'xcreen' and 'data' in item:
        #     drawxcreen(path=item['path'], data=item['data'])
            
        #     # 繪製九宮格
        #     colorlist = [(0, 255, 255), (0, 0, 255), (0, 0, 0), (255, 255, 255),
        #      (255, 0, 255), (255, 0, 0), (255, 255, 0), (128, 128, 128)]
            
        #     img = cv2.imread(path)
        #     # 建立一張 512x512 的 RGB 圖片（黑色）
        #     img = np.zeros((img.shape[0]+200,img.shape[1],img.shape[2]), np.uint8)
            
        #     img.fill(200)
        #     h = img.shape[0]
        #     w = img.shape[1]
        #     # 直版 3X4
        #     # 1 2 3
        #     # 4 5 6
        #     # 7 8 9
        #     # 101112
        #     # 口口口
        #     # 口口口
        #     # 口口口
        #     # 口口口
        #     if 'advertising_wall' in json.loads(item['data']):
        #         data = json.loads(item['data'])['advertising_wall']
                
        #         xcount = 3
        #         ycount = 4
        #         for i in range(xcount*ycount):
        #             pointx = int(w / xcount)*int(i%xcount),int(w / xcount)*int((i%xcount)+1)
        #             pointy = int((h / ycount)*int(i/xcount)),int((h / ycount)*(int(i/xcount)+1))

        #             print(str(pointy))
        #             cv2.rectangle(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), colorlist[i%len(colorlist)], 1)
        #             adname = "無廣告"
        #             if len(data) > i:
        #                 adname = data[i]['name']
        #                 if 'aiscore' in data[i]:
        #                     adname = adname+" score:"+str(data[i]['aiscore'])

        #             img = cv2ImgAddText(img,adname, pointx[0],pointy[0],colorlist[i%len(colorlist)], 32)
                    
        #             if len(data) > i and "userai" not in data[i]:
                        
        #                 cv2.line(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), (0, 0, 255), 5)
        #                 cv2.line(img, (pointx[1],pointy[0]), (pointx[0],pointy[1]), (0, 0, 255), 5)


        #         # 橫板 2X5
        #         # 1 2 3 4 5
        #         # 6 7 8 9 10
        #         # 口口口口口
        #         # 口口口口口
        #         # ((0.0,307.2),0,1024.0) ((307.2,614.4),(0,1024.0))
        #         # data = json.loads(item['data'])['advertising_wall']
                
        #         # for i in range(10):
                    
        #         #     if i < 5:
        #         #         pointy = 0,int(((h / 2)))
        #         #         pointx = int(((w / 5) * i)),int(((w / 5) * (i+1)))
        #         #     else:
        #         #         pointx = int(((w / 5) * (i-5))),int(((w / 5) * (i-4)))
        #         #         pointy = int(((h / 2))),int(((h / 2))*2)
        #         #     cv2.rectangle(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), colorlist[i%len(colorlist)], 1)
        #         #     adname = "無廣告"
        #         #     if len(data) > i:
        #         #         adname = data[i]['name']
        #         #     img = cv2ImgAddText(img,adname, pointx[0],pointy[0],colorlist[i%len(colorlist)], 32)
                    
        #         #     if len(data) > i and "userai" not in data[i]:
                        
        #         #         cv2.line(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), (0, 0, 255), 5)
        #         #         cv2.line(img, (pointx[1],pointy[0]), (pointx[0],pointy[1]), (0, 0, 255), 5)
                    
        #         img = cv2ImgAddText(img,"廣告牆:advertising_wall", w/2,h,colorlist[i%len(colorlist)], 64)
        #         filename = str(time.time())+'_showimg.jpg'
        #         cv2.imwrite('static/uploads/'+filename,img)
        #         file_names.append(filename)

        #         # 廣告列表
        #         img = np.zeros((img.shape[0]+200,img.shape[1],img.shape[2]), np.uint8)
        #         img.fill(200)
        #         shifty = 0
        #         data = json.loads(item['data'])['idle_carousel']
        #         for dataitem in data:
        #             img = cv2ImgAddText(img,dataitem['name']+" score:"+str(dataitem['aiscore']), 0,shifty,colorlist[i%len(colorlist)], 32)
        #             shifty += 32
                
                
        #         img = cv2ImgAddText(img,"閒置輪播:idle_carousel", w/2,h,colorlist[i%len(colorlist)], 64)
        #         cv2.imwrite('static/uploads/'+"idle_carousel"+filename,img)
        #         file_names.append("idle_carousel"+filename)
        #         # 跑馬燈
        #         img = np.zeros((img.shape[0]+200,img.shape[1],img.shape[2]), np.uint8)
        #         img.fill(200)
        #         shifty = 0
        #         data = json.loads(item['data'])['banner']
        #         for dataitem in data:
        #             img = cv2ImgAddText(img,dataitem['name']+" score:"+str(dataitem['aiscore']), 0,shifty,colorlist[i%len(colorlist)], 32)
        #             shifty += 32
                
                
        #         img = cv2ImgAddText(img,"跑馬燈:banner", w/2,h,colorlist[i%len(colorlist)], 64)
        #         cv2.imwrite('static/uploads/'+"banner"+filename,img)
        #         file_names.append("banner"+filename)

    # return render_template('upload.html', filenames=file_names,apikey=apikey)

if __name__ == "__main__":
    app.run()
