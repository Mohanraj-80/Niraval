import cv2
from num2words import num2words
import numpy as np
from datetime import date
import copy

class writeWithdraw:


    def __init__(self,img_path):

        self.keys = ['account no' , 'phone' , 'name' , 'branch code' , 'amount']
        self.functions = { 'account no' : self.writeaccno , 'phone' : self.writephone , "name" : self.writename ,
                          
                           'branch code' : self.writebranch , 'amount' :self.writeammount}
        
        self.img = cv2.imread(img_path)
        self.temp = copy.deepcopy(self.img)


    def write(self,details):

        self.img = copy.deepcopy(self.temp)

        for key in self.keys:

            if(details[key] != None):
                self.functions[key](details[key])

        return self.img
            


    def writeaccno(self,detail):

        x = 865
        y = 430

        detail = '  '.join(detail)
        cv2.putText(self.img, detail, (x,y), cv2.FONT_HERSHEY_DUPLEX , 1, (0,0,0), 2 , cv2.LINE_8)
        

    def writephone(self,detail):


        x = 1240
        y = 150
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_ITALIC   , 1.1 , (0,0,0), 2 , cv2.LINE_8)


    def writename(self,detail):

        x = 470
        y = 150
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_HERSHEY_DUPLEX   , 1.1 , (0,0,0), 2 , cv2.LINE_8)


    def writebranch(self,detail):

        x = 1240
        y = 270
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_ITALIC   , 1.1 , (0,0,0), 2 , cv2.LINE_8)


    def writeammount(self,detail):

        x1 = 1230
        y1 = 610
        detail = str(detail)
        cv2.putText(self.img , detail , (x1,y1) , cv2.FONT_HERSHEY_DUPLEX   , 1.4 , (0,0,0), 2, cv2.LINE_8)

        x2 = 660
        y2 = 495

        detail = num2words(detail,lang = 'en_IN')
        detail = str(detail).title()
        detail += " only."

        detail = detail.split(" ")

        if(len(detail) > 4):
            cv2.putText(self.img , " ".join(detail[4:]) , (x2 - 600,y2 + 45) , cv2.FONT_HERSHEY_DUPLEX   , 1.4 , (0,0,0), 2, cv2.LINE_8)


        cv2.putText(self.img , " ".join(detail[:4]) , (x2,y2) , cv2.FONT_HERSHEY_DUPLEX   , 1.4 , (0,0,0), 2, cv2.LINE_8)






class writeDeposit:

    def __init__(self,img_path):


        self.keys = ['account no' , "phone" , "name" , "branch code" , "pan no" , "amount" , "amount_list"]
        self.functions = { 'account no' : self.writeaccno , "phone" : self.writephone , "name" : self.writename 
                          , "branch code" : self.writebranch , "pan no" : self.writepan , "amount" : self.writeamount , "amount_list": self.writeamountlist}
        
        self.img = cv2.imread(img_path)
        self.temp = np.array(self.img)


    def write(self,details):

        self.img = np.array(self.temp)

        for key in self.keys:
            if(details[key] != None):
                self.functions[key](details[key])
        
        self.writedate()
        return self.img
    
    
    def writeaccno(self,detail):

        x = 750
        y = 225

        detail = '  '.join(detail)
        cv2.putText(self.img, detail, (x,y), cv2.FONT_HERSHEY_DUPLEX , 0.6, (0,0,0), 1 , cv2.LINE_8)

        x = 63
        y = 265
        cv2.putText(self.img, detail, (x,y), cv2.FONT_HERSHEY_DUPLEX , 0.4, (0,0,0), 1 , cv2.LINE_8)



    def writephone(self,detail):

        x = 970
        y = 278
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_ITALIC   , 0.5 , (0,0,0), 1, cv2.LINE_8)

        x = 200
        y = 309
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_HERSHEY_DUPLEX   , 0.5 , (0,0,0), 1 , cv2.LINE_8)


    
    def writename(self,detail):

        x = 840
        y = 250
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_HERSHEY_DUPLEX   , 0.5 , (0,0,0),  1, cv2.LINE_8)

        x = 170
        y = 290
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_HERSHEY_DUPLEX   , 0.5 , (0,0,0), 1 , cv2.LINE_8)


    
    def writebranch(self,detail):

        x = 910
        y = 160
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_ITALIC   , 0.65 , (0,0,0), 1 , cv2.LINE_8)

        x = 160
        y = 193
        cv2.putText(self.img , detail , (x,y) , cv2.FONT_HERSHEY_DUPLEX   , 0.5 , (0,0,0), 1 , cv2.LINE_8)

    

    def writepan(self,detail):

        x = 530
        y = 185

        detail = " ".join(detail)
        cv2.putText(self.img, detail, (x,y), cv2.FONT_HERSHEY_DUPLEX , 0.5, (0,0,0), 1 , cv2.LINE_8)



    def writeamount(self,detail):

        x1 = 1120
        y1 = 355
        self.amount = detail

        detail = str(detail)
        cv2.putText(self.img , detail , (x1,y1) , cv2.FONT_HERSHEY_DUPLEX   , 0.7, (0,0,0), 1, cv2.LINE_8)

        x1 = 130
        y1 = 346

        detail = str(detail)
        cv2.putText(self.img , detail , (x1,y1) , cv2.FONT_HERSHEY_DUPLEX   , 0.7, (0,0,0), 1, cv2.LINE_8)


        x2 = 955
        y2 = 330

        detail = num2words(detail,lang = 'en_IN')
        detail = str(detail).title()

        detail += " only."
        detail = detail.split(" ")

        if(len(detail) > 5):
            pass
            cv2.putText(self.img , " ".join(detail[5:]) , (x2 - 200 , y2+30) , cv2.FONT_HERSHEY_DUPLEX   , 0.5, (0,0,0), 1, cv2.LINE_8)

        cv2.putText(self.img , " ".join(detail[:5]) , (x2,y2) , cv2.FONT_HERSHEY_DUPLEX   , 0.5, (0,0,0), 1, cv2.LINE_8)



    def writeamountlist(self,detail):
        
        sum = 0
        x = 505 
        y = 260
        yinc = 20

        for i in detail.keys(): 
            cv2.putText(self.img , str(detail[i]) , (x,y) , cv2.FONT_HERSHEY_TRIPLEX  , 0.5 , (0,0,0) , 1 , cv2.LINE_8)
            cv2.putText(self.img,  str(int(detail[i]) * int(i)) ,  (x+59 ,y) , cv2.FONT_HERSHEY_TRIPLEX , 0.5 , (0,0,0) ,1, cv2.LINE_8)
            y+=yinc
            sum +=int(detail[i]) * int(i)

        cv2.putText(self.img, str(sum) ,  (x+59 ,y + 1*yinc - 5) ,cv2.FONT_HERSHEY_TRIPLEX  , 0.5 , (0,0,0) , 1, cv2.LINE_8)



    def writedate(self):

        d = str(date.today()).replace("-","")
        d = " ".join(d)
        
        x  = 1095
        y = 155

        cv2.putText(self.img, d ,  (x ,y) , cv2. FONT_ITALIC  , 0.56, (0,0,0) , 1 , cv2.LINE_8)
        x = 105 
        y = 215 
        cv2.putText(self.img, d ,  (x ,y) , cv2. FONT_ITALIC  , 0.5, (0,0,0),1 ,  cv2.LINE_8)


class Writer:

    def __init__(self , withdrawChallanPath , depositChallanPath):

        self.writeWithdraw = writeWithdraw(withdrawChallanPath)
        self.writeDeposit = writeDeposit(depositChallanPath)

    def write(self , info , isWithDraw):

        if(isWithDraw):

            return self.writeWithdraw.write(info)
        
        return self.writeDeposit.write(info)
    




if __name__ == "__main__":

    details = {'account no': '110077739383',
 'phone': '917810028722',
 'branch code': "99999",
 'name': 'PRAGATHEESH INDIRAN',
 "amount" : 806534322,
 "pan no" : 'HPLPP3753G' ,
 "amount_list" : {2000 : 3 , 500 : 2 , 200 : 4 , 100 : 2 , 50 : 1 , 10 : 1,5 : 1}}
    
