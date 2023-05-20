
import cv2 
import numpy as np

webcam = True

if webcam:
    cap = cv2.VideoCapture() 
    ip = 'https://10.1.3.139:8080/video'
    cap.open(ip)
    
# tomate\imagens
path = 'v1/tomate/imagens/WhatsApp Image 2022-11-30 at 12.51.01 PM.jpeg'
img = cv2.imread(path)
pos = []
posElipse = []

kernel = np.ones((5, 5), np.uint8)

def Selctor(img):
    pos = cv2.selectROI(img)   
    
    with open('v1/new/pontos_regiao_interesse.txt', 'w') as f: 
            f.write(str(pos[0])+'\n')
            f.write(str(pos[1])+'\n')
            f.write(str(pos[2])+'\n')
            f.write(str(pos[3])+'\n')
    return pos
                
def limiar(img):
    
    hsv = cv2.cvtColor(img,  cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    gaussian = cv2.GaussianBlur(s, (3, 3), 0)
    limiar, bin = cv2.threshold(gaussian, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    limiar = cv2.dilate(limiar, kernel, iterations=1)

    return bin

with open('v1/new/pontos_regiao_interesse.txt', 'r') as f:
    for p in f:
        pos.append(int(p.split('\n')[0]))	



while True:
    if webcam:
        success, img = cap.read()
        # img = img[135:135+697, 228:228+2035]  

        img = img[380 : 350+700, 252: 252 +  1968]   

    imgProcessed = img.copy()
    

    if len(pos) != 4:   
        pos = Selctor(img)
    
    bin = limiar(img[pos[1]:pos[1]+pos[3],pos[0]:pos[0]+pos[2]])
    contours, _ = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    perimetros = []
    # cv2.imshow('bin', bin)
    for c in contours:      
        perimetros.append(cv2.arcLength(c, True))

    
    tomate = contours[perimetros.index(max(perimetros))]
    perimetros.pop(perimetros.index(max(perimetros)))
    posTomate = cv2.boundingRect(tomate)    
    imgTomate = img[pos[1]+posTomate[1] : pos[1]+posTomate[1]+posTomate[3] , pos[0]+posTomate[0]:pos[0]+posTomate[0]+posTomate[2]]  
    cv2.rectangle(imgProcessed, (posTomate[0]+pos[0], posTomate[1]+pos[1]), (posTomate[0]+posTomate[2]+pos[0], posTomate[1]+posTomate[3]+pos[1]), (0, 0, 0), 2)    
    cv2.putText(imgProcessed, ('Tomate'), (int(posTomate[0] + posTomate[2]/2)+pos[0], posTomate[1]+pos[1]-10),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)    
    

    if len(perimetros) > 0:
        conversor = contours[perimetros.index(max(perimetros))]
        posConversor = cv2.boundingRect(conversor)
        cv2.rectangle(imgProcessed, (posConversor[0]+pos[0], posConversor[1]+pos[1]), (posConversor[0]+posConversor[2]+pos[0], posConversor[1]+posConversor[3]+pos[1]), (0, 255, 0), 2)      
        cv2.putText(imgProcessed, ('Conversor'), (int(posConversor[0] )+pos[0], posConversor[1]+pos[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)    
        wC = (posConversor[2]*20) / posConversor[2]/10
        hC = (posConversor[3]*20) / posConversor[3]/10
        cv2.putText(imgProcessed, (f'Largura: {wC:,.2f}cm'), (int(posConversor[0] + posConversor[2]/2)+pos[0],  posConversor[1]+posConversor[3]+pos[1]+15),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)    
        cv2.putText(imgProcessed, (f'Altura: {hC:,.2f}cm'), (int(posConversor[0] + posConversor[2])+pos[0]+10, posConversor[1]+posConversor[3]+pos[1]+30),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)    

        wT =((posTomate[2]*20) / posConversor[2]) / 10
        hT = (posTomate[3]*20) / posConversor[3] / 10
        
        cv2.putText(imgProcessed, (f'Largura: {wT:,.2f}cm'), (int(posTomate[0] + posTomate[2])+pos[0]+10, pos[1]+posTomate[1]+25 ),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
        cv2.putText(imgProcessed, (f'Altura: {hT:,.2f}cm'), (int(posTomate[0] + posTomate[2])+pos[0]+10, pos[1]+posTomate[1] +45),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
        
        if len(posElipse)>0:        
            cv2.rectangle(imgProcessed, (posTomate[0]+pos[0]+posElipse[0], posTomate[1]+pos[1]+posElipse[1]), (posTomate[0]+pos[0]+posElipse[0]+posElipse[2], posTomate[1]+pos[1]+posElipse[1]+posElipse[3] ), (0, 255, 0), 2)
            wE = (posElipse[2]*20) / posConversor[2]
            hE = (posElipse[3]*20) / posConversor[3]
            firmeza = (0.491)/(0.784*(wE)*(hE)/100) 
    
            cv2.putText(imgProcessed, (f'Altura: {hE/10:,.2f}cm'), (posTomate[0]+pos[0]+posElipse[0],posTomate[1]+pos[1]+posElipse[1]+posElipse[3]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            cv2.putText(imgProcessed, (f'Largura: {wE/10:,.2f}cm'), (posTomate[0]+pos[0]+posElipse[0],posTomate[1]+pos[1]+posElipse[1]+posElipse[3]+40),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            cv2.putText(imgProcessed, (f'firmeza: {firmeza:,.2f}'), (posTomate[0]+pos[0]+posElipse[0],posTomate[1]+pos[1]+posElipse[1]+posElipse[3]+60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)




    

    cv2.imshow('imgProcessed', imgProcessed)

    key = cv2.waitKey(1) 
            
    if key == ord('r'):         
        posElipse = cv2.selectROI(imgTomate)
        print(posElipse)
    if key == ord('s'):
        pos = Selctor(img)
        print(pos)
        posElipse = []


    