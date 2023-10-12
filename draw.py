import cv2
import json
import numpy as np

c1 = ["國小生","帶小孩顧客","銀髮族","上班族","菜籃族","國高中生"]
c2 = {"國小生":"type1","帶小孩顧客":"type2","銀髮族":"type3","上班族":"type4","菜籃族":"type5","國高中生":"type6"}

def drawAiData(frame, name, data, point_x, point_y, color):
    shift = 15
    textsize = 0.5
    point_y += shift
    cv2.putText(frame, name, (int(point_x), int(point_y)), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, color, 1, cv2.LINE_AA)
    
    if type(data) == list:
        for item in data:  # yolo格式
            if 'conf' in item and 'name' in item:
                drawname = item['name']
                if item['name'] in c1:
                    drawname = c2[item['name']]
                point_y += shift
                cv2.putText(frame, drawname+":"+str(round(item['conf'], 2)), (int(point_x), int(
                    point_y)), cv2.FONT_HERSHEY_SIMPLEX, textsize, color, 1, cv2.LINE_AA)
                
            elif 'point' in item and 'bottom' in item['point']:  # 服飾分類
                for key in item:
                    if key != 'point':
                        point_y += shift
                        cv2.putText(frame, key, (int(point_x), int(
                            point_y)), cv2.FONT_HERSHEY_SIMPLEX, textsize, color, 1, cv2.LINE_AA)
            else:
                if 'facebox' in item:
                    point_y += shift
                    cv2.putText(frame, "pitch"+str(round(item['pitch'], 2))+" roll"+str(round(item['roll'], 2))+" yaw"+str(round(
                        item['yaw'], 2)), (int(point_x), int(point_y)), cv2.FONT_HERSHEY_SIMPLEX, textsize, color, 1, cv2.LINE_AA)
            
    elif type(data) == dict:
        
        for item in data:
            point_y += shift
            cv2.putText(frame, "age:"+str(data[item]['age'])+" gender:"+str(data[item]['gender']), (int(point_x), int(point_y)), cv2.FONT_HERSHEY_SIMPLEX, textsize, color, 1, cv2.LINE_AA)
            point_y += shift
            cv2.putText(frame, "emotion:"+str(data[item]['dominant_emotion'])+" race:"+str(data[item]['dominant_race']), (int(point_x), int(point_y)), cv2.FONT_HERSHEY_SIMPLEX, textsize, color, 1, cv2.LINE_AA)
        else:
            print("未知格式")
    else:
        print("未知格式")
    return point_y

def yolobbox2bbox(x, y, w, h):
    x1, y1 = x-w/2, y-h/2
    x2, y2 = x+w/2, y+h/2
    return x1, y1, x2, y2
def drawxcreen(path, data):
    colorlist = [(0, 255, 255), (0, 0, 255), (0, 0, 0), (255, 255, 255),
             (255, 0, 255), (255, 0, 0), (255, 255, 0), (128, 128, 128)]
    frame = cv2.imread(path)
    data = json.loads(data)
    if data != None and 'ai' in data:

        for userid in data['ai']["userdata"]:
            userdataitem = data['ai']["userdata"][userid]
            yolopointy = 10
            color = colorlist[int(userdataitem['id']) % len(colorlist)]

            itemdatarect = userdataitem['rect']
            if len(itemdatarect) == 0:
                continue
            centroid = data['ai']["userdata"][userid]['centroid']
            x = itemdatarect[0]
            y = itemdatarect[1] - 10
            if userdataitem['focus']:
                cv2.putText(frame, str(userdataitem['id'])+"_focus", (int(centroid[0]), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                            2, color, 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, str(userdataitem['id']), (int(centroid[0]), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                            1, color, 1, cv2.LINE_AA)
            
            y = itemdatarect[1] + 20
            cv2.rectangle(frame, (itemdatarect[0], itemdatarect[1]),
                          (itemdatarect[2], itemdatarect[3]), color, 1)
            
            if 'p_type_detection' in data['ai']["userdata"][userid]:
                userdata = data['ai']["userdata"][userid]['p_type_detection']
                y = drawAiData(frame, 'p_type_detection', userdata, x, y, color)
            
            if 'clothing_50' in data['ai']["userdata"][userid]:
                userdata = data['ai']["userdata"][userid]['clothing_50']
                y = drawAiData(frame, 'clothing_50', userdata, x, y, color)

            if 'head_pose_estimation' in data['ai']['userdata'][userid]:
                userdata = data['ai']['userdata'][userid]['head_pose_estimation']
                y = drawAiData(frame, 'head_pose_estimation',
                               userdata, x, y, color)
            if 'clothing_detection' in data['ai']['userdata'][userid]:
                userdata = data['ai']['userdata'][userid]['clothing_detection']
                y = drawAiData(frame, 'clothing_detection',
                               userdata, x, y, color)
            if 'object_detection' in data['ai']['userdata'][userid]:
                userdata = data['ai']['userdata'][userid]['object_detection']
                y = drawAiData(frame, 'object_detection',
                               userdata, x, y, color)
            if 'face_detection' in data['ai']['userdata'][userid]:
                userdata = data['ai']['userdata'][userid]['face_detection']
                y = drawAiData(frame, 'face_detection', userdata, x, y, color)
            if 'object_30_detection' in data['ai']['userdata'][userid]:
                userdata = data['ai']['userdata'][userid]['object_30_detection']
                y = drawAiData(frame, 'object_30_detection',
                               userdata, x, y, color)
    cv2.imwrite(path, frame)
def draw(path, data):
    img = cv2.imread(path)
    font = cv2.FONT_HERSHEY_COMPLEX
    colorlist = [(0, 255, 0),(255, 0, 0),(0, 0, 255),(127, 127, 127)]
    drawdata = json.loads(data)["data"]
    for drawitem in drawdata:
        
        
        if "object_30_data" in drawitem or "object_detection" in drawitem or "clothing_50" in drawitem or "helm_detection" in drawitem or "playingcards_data" in drawitem or "p_type_data" in drawitem or "fireandsmoke_detection" in drawitem or "car_license" in drawitem:
            if "car_license" in drawitem:
                objlist = drawitem["car_license"]
            if "playingcards_data" in drawitem:
                objlist = drawitem["playingcards_data"]
            if "object_30_data" in drawitem:
                objlist = drawitem["object_30_data"]
            if "object_detection" in drawitem:
                objlist = drawitem["object_detection"]
            if "clothing_50" in drawitem:
                objlist = drawitem["clothing_50"]
            if "fireandsmoke_detection" in drawitem:
                objlist = drawitem["fireandsmoke_detection"]
            if "helm_detection" in drawitem:
                objlist = drawitem["helm_detection"]
            if "p_type_data" in drawitem:
                objlist = drawitem["p_type_data"]
            shift = 30
            colorcount = 0
            for item in objlist:
                x, y, w, h = 0,0,0,0
                if 'xywh' in item:
                    x, y, w, h = item['xywh']
                xyxy = yolobbox2bbox(x, y, w, h)
                cv2.rectangle(img, (int(xyxy[0]*img.shape[1]), int(xyxy[1]*img.shape[0])), (int(
                    xyxy[2]*img.shape[1]), int(xyxy[3]*img.shape[0])), colorlist[colorcount%len(colorlist)], 2)
                colorcount += 1
            colorcount = 0
            for item in objlist:
                x, y, w, h = 0,0,0,0
                if 'xywh' in item:
                    x, y, w, h = item['xywh']
                xyxy = yolobbox2bbox(x, y, w, h)
                drawname = item['name']
                if item['name'] in c1:
                    drawname = c2[item['name']]
                cv2.putText(img, drawname+":"+str(round(item['conf'],2)), (int(xyxy[0]*img.shape[1]), int(
                    xyxy[1]*img.shape[0])+shift), font, 1, colorlist[colorcount%len(colorlist)], 4, cv2.LINE_AA)
                # shift += 30
                colorcount += 1

        if "clothing_detection" in drawitem:
            shift = 0
            for item in drawitem["clothing_detection"]:
                bottom = item['point']['bottom']
                left = item['point']['left']
                right = item['point']['right']
                top = item['point']['top']
                cv2.rectangle(img, (left, top), (right,
                                                 bottom), (0, 255, 0), 2)
                for key in item:
                    if key != "point":
                        cv2.putText(img, key+":"+str(round(item[key], 2)), (left, top+shift), font, 1,
                                    (255, 255, 255), 2, cv2.LINE_AA)
                        shift += 30
        if "face_detection" in drawitem:
            shift = 30
            for item in drawitem["face_detection"]:
                for key in drawitem["face_detection"]:
                    data = drawitem["face_detection"][key]
                    if type(data) == dict:
                        age = data['age']
                        dominant_emotion = data['dominant_emotion']
                        dominant_race = data['dominant_race']
                        gender = data['gender']
                        x = data['region']["x"]
                        y = data['region']["y"]
                        w = data['region']["w"]
                        h = data['region']["h"]
                        cv2.rectangle(img, (x, y), (x+w,
                                                    y+h), (0, 255, 0), 2)
                        cv2.putText(img, "face_detection", (x, y+shift), font, 0.8,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        shift += 20
                        cv2.putText(img, "age:"+str(age), (x, y+shift), font, 0.5,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        shift += 20
                        cv2.putText(img, "gender:"+str(gender), (x, y+shift), font, 0.5,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        shift += 20
                        cv2.putText(img, "dominant_emotion:"+dominant_emotion, (x, y+shift), font, 0.5,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        shift += 20
                        cv2.putText(img, "dominant_race:"+dominant_race, (x, y+shift), font, 0.5,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        shift += 20
                        cv2.putText(img, "dominant_race:"+dominant_race, (x, y+shift), font, 0.5,
                                    (255, 255, 255), 1, cv2.LINE_AA)

        if "head_pose_estimation" in drawitem:
            shift = 30
            for item in drawitem["head_pose_estimation"]:
                x, y, x1, y1 = item["facebox"]
                pitch = item["pitch"]
                roll = item["roll"]
                yaw = item["yaw"]
                cv2.rectangle(img, (x, y), (x1,
                                            y1), (0, 255, 0), 2)
                cv2.putText(img, "head_pose_estimation", (x1, y+shift), font, 0.8,
                            (255, 255, 255), 1, cv2.LINE_AA)
                shift += 20
                cv2.putText(img, "pitch:"+str(pitch), (x1, y+shift), font, 0.5,
                            (255, 255, 255), 1, cv2.LINE_AA)
                shift += 20
                cv2.putText(img, "roll:"+str(roll), (x1, y+shift), font, 0.5,
                            (255, 255, 255), 1, cv2.LINE_AA)
                shift += 20
                cv2.putText(img, "yaw:"+str(yaw), (x1, y+shift), font, 0.5,
                            (255, 255, 255), 1, cv2.LINE_AA)
        if "centroidtracker" in drawitem:
            print([item['centroid'] for item in drawitem['centroidtracker']['id']])
            shift = 30
            for item in drawitem["centroidtracker"]:
                if item == "id":
                    for findid in drawitem["centroidtracker"]['id']:
                        centroid = findid['centroid']
                        cv2.putText(img, str(findid['id']), (int(centroid[0]), int(centroid[1])), font, 0.5,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                if item == "rect":
                    for rect in drawitem["centroidtracker"]['rect']:
                        cv2.rectangle(img, (rect[0], rect[1]), (rect[2],
                                                                rect[3]), (0, 255, 0), 2)
        # if "helm_detection" in drawitem:
        #     shift = 30
        #     for item in drawitem["helm_detection"]:
        #         x, y, w, h = item['xywh']
        #         xyxy = yolobbox2bbox(x, y, w, h)
        #         cv2.rectangle(img, (int(xyxy[0]*img.shape[1]), int(xyxy[1]*img.shape[0])), (int(
        #             xyxy[2]*img.shape[1]), int(xyxy[3]*img.shape[0])), (0, 255, 0), 2)
        #         cv2.putText(img, str(item['name']), (int(xyxy[0]*img.shape[1]), int(xyxy[1]*img.shape[0])), font, 0.5,
        #                     (255, 255, 255), 1, cv2.LINE_AA)
        if "find_face" in drawitem:
            for item in drawitem["find_face"]:
                point = item['point']
                bottom = point['bottom']
                left = point['left']
                right = point['right']
                top = point['top']
                data = point['data']

                cv2.rectangle(img, (left, top), (right,
                                                 bottom), (0, 255, 0), 2)
                if len(data) > 0 and data[0]['p'] < 0.4:
                    cv2.putText(img, "id:"+str(data[0]['id']), (left+5, top+30), font, 0.5,
                                (255, 255, 255), 1, cv2.LINE_AA)
                else:
                    cv2.putText(img, "unknow", (left+5, top+30), font, 0.5,
                                (255, 255, 255), 1, cv2.LINE_AA)
        
    cv2.imwrite(path, img)


from PIL import Image, ImageDraw, ImageFont



def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):

    if (isinstance(img, np.ndarray)):  #判断是否OpenCV图片类型

        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(img)

    fontText = ImageFont.truetype(

        "font/simsun.ttc", textSize, encoding="utf-8")

    draw.text((left, top), text, textColor, font=fontText)

    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)