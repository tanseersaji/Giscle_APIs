import base64
import requests
import time,cv2

g_url = 'http://api.giscle.ml'


img_path = 'input/test.jpg'
frame = cv2.imread(img_path)

img = open(img_path, "rb").read()
img = base64.b64encode(img)

token = "Paste Your Token"

payload = {'image': img }

r = requests.post(g_url + ':80/image', files=payload, headers={'token': token})

if r.ok:
    #print(r.json())
    preds =r.json()
    print("{}".format(preds['Data']))
    while True:
        font = cv2.FONT_HERSHEY_SIMPLEX
        if len(preds.keys()) and preds['Data'][1] != 0:
            #print(preds['Data'])
            for key in preds['Data'][2].keys():
                    gender = preds['Data'][2][str(key)]['Gender']
                    x,y,h,w = preds['Data'][2][str(key)]['rect_coordinate']
                    age = preds['Data'][2][str(key)]['Age']
                    emotion = preds['Data'][2][str(key)]['Emotion']
                    #accuracy = preds['Output'][2][str(key)]['Accuracy']
                    #cv2.putText(frame,'Gender : ' + gender,(x,y-25), font, 0.5, (200,255,155), 1, cv2.LINE_AA)
                    cv2.putText(frame,'Age : ' + str(age),(x,y-50), font, 0.5, (200,255,155), 1, cv2.LINE_AA)
                    #cv2.putText(frame,'Emotion : ' + str(emotion),(x,y-75), font, 0.5, (200,255,155), 1, cv2.LINE_AA)
                    cv2.putText(frame,'Total_faces : {}'.format(preds['Data'][1]),(10,20), font, 0.5, (200,255,155), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+h,y+w), (255,255,255))
    
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print('Status: {}'.format(r.status_code))
