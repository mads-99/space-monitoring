
import cv2
import numpy as np
import smtplib
from email.message import EmailMessage

#cv2 is the open source library for ML and image processing
#numpy is library used to work with arrays
#smtplib defines smtp client that can be used to send mail

def email_alert(subject, body, to):
    msg= EmailMessage()
    msg.set_content(body)
    msg['subject']= subject
    msg['to']=to
    
    user="1ms18cs064@gmail.com"
    msg['from']= user
    password="qxkrwcnjhwiczxps"

    server= smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)

    server.quit

    


# Calculation of bottom center for bounding boxes
def get_transformed_points(boxes, prespective_transform):
    
    bottom_points = []
    for box in boxes:
        pnts = np.array([[[int(box[0]+(box[2]*0.5)),int(box[1]+box[3])]]] , dtype="float32")
        bd_pnt = cv2.perspectiveTransform(pnts, prespective_transform)[0][0]
        pnt = [int(bd_pnt[0]), int(bd_pnt[1])]
        bottom_points.append(pnt)
        
    return bottom_points

def cal_dis(p1, p2, distance_w, distance_h):
    
    h = abs(p2[1]-p1[1])
    w = abs(p2[0]-p1[0])
    
    dis_w = float((w/distance_w)*180)
    dis_h = float((h/distance_h)*180)
    
    return int(np.sqrt(((dis_h)**2) + ((dis_w)**2)))

# Func to obtain the euclidian dist
def get_distances(boxes1, bottom_points, distance_w, distance_h):
    

    distance_mat = []
    bxs = []
    for i in range(len(bottom_points)):
        for j in range(len(bottom_points)):
            if i != j:
                dist = cal_dis(bottom_points[i], bottom_points[j], distance_w, distance_h)
                
                if dist <= 150:
                    closeness = 0
                    distance_mat.append([bottom_points[i], bottom_points[j], closeness])
                    bxs.append([boxes1[i], boxes1[j], closeness])
                  
                elif dist > 150 and dist <=180:
                    closeness = 1
                    distance_mat.append([bottom_points[i], bottom_points[j], closeness])
                    bxs.append([boxes1[i], boxes1[j], closeness])       
                else:
                    closeness = 2
                    distance_mat.append([bottom_points[i], bottom_points[j], closeness])
                    bxs.append([boxes1[i], boxes1[j], closeness])
                
                if dist<=180:
                    email_alert("action needed!!!!","people are not following social distancing norms in the event please take action!!!!","1ms18cs064@gmail.com")
                
    return distance_mat, bxs


 
# Function gives scale for birds eye view               
def get_scale(W, H):
    
    dis_w = 400
    dis_h = 600
    
    return float(dis_w/W),float(dis_h/H)
    
# Function gives count for humans at high risk, low risk and no risk    
def get_count(distances_mat):

    r = []
    g = []
    y = []
    
    for i in range(len(distances_mat)):

        if distances_mat[i][2] == 0:
            if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                r.append(distances_mat[i][0])
            if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                r.append(distances_mat[i][1])
                
    for i in range(len(distances_mat)):

        if distances_mat[i][2] == 1:
            if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                y.append(distances_mat[i][0])
            if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                y.append(distances_mat[i][1])
        
    for i in range(len(distances_mat)):
    
        if distances_mat[i][2] == 2:
            if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                g.append(distances_mat[i][0])
            if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                g.append(distances_mat[i][1])
   
    return (len(r),len(y),len(g))






