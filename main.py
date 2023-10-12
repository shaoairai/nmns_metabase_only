import os
from flaskapp import app
from api import callapi,callxcreen,getimage
import urllib.request
from queue import Queue
import time
from draw import draw,drawxcreen,cv2ImgAddText
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template
import threading
import numpy as np
import cv2
import json

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    
    return render_template('upload.html',apikey="")


@app.route('/', methods=['POST'])
def upload_image():
    q = Queue()
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    apikey = ""
    files = request.files.getlist('files[]')
    selecttype = request.form.getlist('type')
    apikey = request.form.get('apikey')
    file_names = []
    filethread = []
    apidatalist = []
    if 'clear' in selecttype:
        for i in range(10):
            thread = threading.Thread(
            target=callxcreen, args=('clear.png', ['xcreen'], q,apikey))
            thread.start()
            filethread.append(thread)
        for item in filethread:
            item.join()
            apidatalist.append(q.get())
        apidatalist = []
        filethread = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = str(time.time())+secure_filename(file.filename)
            file_names.append(filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            thread = threading.Thread(
                target=callapi, args=(path, selecttype, q,apikey))
            thread.start()
            filethread.append(thread)
            if 'xcreen' in selecttype:
                thread = threading.Thread(
                target=callxcreen, args=(path, selecttype, q,apikey))
                thread.start()
                filethread.append(thread)
                thread.join()

    for item in filethread:
        item.join()
        apidatalist.append(q.get())

    for item in apidatalist:
        # 內部測試頁 https://saas_demo.intemotech.com/ 未付款回傳寫在 try 當中
        try:
            if json.loads(item['data'])['msg'] == 'api pay failed':
                return render_template('upload.html', filenames=file_names,apikey=apikey,ispay='使用者尚未付款')
        except:
            mydata = json.loads(item['data'])
            if 'data' in mydata:
                for mydataitem in mydata['data']:
                    if 'super_resolution_data' in mydataitem:
                        superresolution = mydataitem['super_resolution_data']
                        for superresolutionkey in superresolution:
                            for url in superresolution[superresolutionkey]:
                                name = getimage(url)
                                file_names.append(name)



        if item['type'] == 'yolor':
            draw(path=item['path'], data=item['data'])
            json.loads(item['data'])
            
        elif item['type'] == 'xcreen' and 'data' in item:
            drawxcreen(path=item['path'], data=item['data'])
            
            # 繪製九宮格
            colorlist = [(0, 255, 255), (0, 0, 255), (0, 0, 0), (255, 255, 255),
             (255, 0, 255), (255, 0, 0), (255, 255, 0), (128, 128, 128)]
            
            img = cv2.imread(path)
            # 建立一張 512x512 的 RGB 圖片（黑色）
            img = np.zeros((img.shape[0]+200,img.shape[1],img.shape[2]), np.uint8)
            
            img.fill(200)
            h = img.shape[0]
            w = img.shape[1]
            # 直版 3X4
            # 1 2 3
            # 4 5 6
            # 7 8 9
            # 101112
            # 口口口
            # 口口口
            # 口口口
            # 口口口
            if 'advertising_wall' in json.loads(item['data']):
                data = json.loads(item['data'])['advertising_wall']
                
                xcount = 3
                ycount = 4
                for i in range(xcount*ycount):
                    pointx = int(w / xcount)*int(i%xcount),int(w / xcount)*int((i%xcount)+1)
                    pointy = int((h / ycount)*int(i/xcount)),int((h / ycount)*(int(i/xcount)+1))

                    print(str(pointy))
                    cv2.rectangle(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), colorlist[i%len(colorlist)], 1)
                    adname = "無廣告"
                    if len(data) > i:
                        adname = data[i]['name']
                        if 'aiscore' in data[i]:
                            adname = adname+" score:"+str(data[i]['aiscore'])

                    img = cv2ImgAddText(img,adname, pointx[0],pointy[0],colorlist[i%len(colorlist)], 32)
                    
                    if len(data) > i and "userai" not in data[i]:
                        
                        cv2.line(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), (0, 0, 255), 5)
                        cv2.line(img, (pointx[1],pointy[0]), (pointx[0],pointy[1]), (0, 0, 255), 5)


                # 橫板 2X5
                # 1 2 3 4 5
                # 6 7 8 9 10
                # 口口口口口
                # 口口口口口
                # ((0.0,307.2),0,1024.0) ((307.2,614.4),(0,1024.0))
                # data = json.loads(item['data'])['advertising_wall']
                
                # for i in range(10):
                    
                #     if i < 5:
                #         pointy = 0,int(((h / 2)))
                #         pointx = int(((w / 5) * i)),int(((w / 5) * (i+1)))
                #     else:
                #         pointx = int(((w / 5) * (i-5))),int(((w / 5) * (i-4)))
                #         pointy = int(((h / 2))),int(((h / 2))*2)
                #     cv2.rectangle(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), colorlist[i%len(colorlist)], 1)
                #     adname = "無廣告"
                #     if len(data) > i:
                #         adname = data[i]['name']
                #     img = cv2ImgAddText(img,adname, pointx[0],pointy[0],colorlist[i%len(colorlist)], 32)
                    
                #     if len(data) > i and "userai" not in data[i]:
                        
                #         cv2.line(img, (pointx[0],pointy[0]), (pointx[1],pointy[1]), (0, 0, 255), 5)
                #         cv2.line(img, (pointx[1],pointy[0]), (pointx[0],pointy[1]), (0, 0, 255), 5)
                    
                img = cv2ImgAddText(img,"廣告牆:advertising_wall", w/2,h,colorlist[i%len(colorlist)], 64)
                filename = str(time.time())+'_showimg.jpg'
                cv2.imwrite('static/uploads/'+filename,img)
                file_names.append(filename)

                # 廣告列表
                img = np.zeros((img.shape[0]+200,img.shape[1],img.shape[2]), np.uint8)
                img.fill(200)
                shifty = 0
                data = json.loads(item['data'])['idle_carousel']
                for dataitem in data:
                    img = cv2ImgAddText(img,dataitem['name']+" score:"+str(dataitem['aiscore']), 0,shifty,colorlist[i%len(colorlist)], 32)
                    shifty += 32
                
                
                img = cv2ImgAddText(img,"閒置輪播:idle_carousel", w/2,h,colorlist[i%len(colorlist)], 64)
                cv2.imwrite('static/uploads/'+"idle_carousel"+filename,img)
                file_names.append("idle_carousel"+filename)
                # 跑馬燈
                img = np.zeros((img.shape[0]+200,img.shape[1],img.shape[2]), np.uint8)
                img.fill(200)
                shifty = 0
                data = json.loads(item['data'])['banner']
                for dataitem in data:
                    img = cv2ImgAddText(img,dataitem['name']+" score:"+str(dataitem['aiscore']), 0,shifty,colorlist[i%len(colorlist)], 32)
                    shifty += 32
                
                
                img = cv2ImgAddText(img,"跑馬燈:banner", w/2,h,colorlist[i%len(colorlist)], 64)
                cv2.imwrite('static/uploads/'+"banner"+filename,img)
                file_names.append("banner"+filename)

    return render_template('upload.html', filenames=file_names,apikey=apikey)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
