import easyocr
import re
import cv2
import matplotlib.pyplot as plt
from pytesseract import *
from PIL import Image 
import numpy as np
import pandas as pd

class Scanner:

    def __init__(self):

        
        pytesseract.tesseract_cmd =  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        self.text_info_keywords = ["account no" , "phone" , "mobile" , "branch code" ,"name" , "pan no"]

        self.keyword_functions_dic = { "account no" : self.findaccno , "phone" : self.findmumber , "mobile" :self.findmumber 
                                      , "branch code"  :self.findbranchcode , "name" : self.getname , "pan no" :self.findpanno}
        
        self.info_dict =  {'account no': '',
'phone': '',
'branch code': "",
'name': '',
"amount" : 0,
"pan no" : '' ,
"amount_list" : {2000 : 0 , 500 :0 , 200 : 0 , 100 : 0, 50 : 0 } }
   
            

    def scan(self,img):
        
        self.dict = dict()        
        self.text = pytesseract.image_to_string(img ,config =   r'--oem 3 --psm 6' )
        self.data = pytesseract.image_to_data(img , output_type=Output.DICT ,config =   r'--oem 3 --psm 6' )

        self.text = self.prerocessor(self.text)

        self.getinfo(self.text,self.data,img)
        self.processinfo()

        return self.info_dict



        
    
    
    def prerocessor(self , text):

        text = text.lower()
        text = re.sub("\s\s+"," ",text)
        text = re.sub("\n"," ",text)
        
        text = re.sub("_","",text)
        text = re.sub("[^A-Za-z\d\s]","",text)
        
        text= re.sub("[A-Za-z]\d+[A-Za-z]","",text)
       
       
       

        #space_bw_numbers
        matches = re.findall(r'\d\s+\d', text)
        for match in matches:
            idx = re.search(match,text)
            (i , j) = idx.span()
            text = text[:i+1] + text[j-1:]
            
        return text



    def getinfo(self,text,data,img):

        

        self.curr_text  = text
        self.curr_img  = img
        self.curr_data = data

        for key in self.text_info_keywords:

            self.info_dict[key] = None
            
            if(key == "name" or key == "pan no"):
                self.info_dict[key] = self.keyword_functions_dic[key]()
                continue
                
            for idx in re.finditer(key , self.curr_text ):
                if(idx != None):
                    if(self.info_dict.get(key,None) == None):
                        self.info_dict[key] = self.keyword_functions_dic[key](idx)



    def processinfo(self):

        if(len(self.info_dict) == 0 ):

            return self.info_dict

        phone = self.info_dict["phone"]

        if(phone == None):
            self.info_dict["phone"] = self.info_dict["mobile"]

        del self.info_dict["mobile"]
        
            

            

    
    def getname(self):

        data = self.filterdata( self.curr_data)
        if(len(data) == 0):
            return None
            
        self.w , self.h = self.curr_img.size
        roi_t , roi_l , roi_w , roi_h = int(data["top"].iloc[0]) ,  int(data["left"].iloc[0]), int(data["width"].iloc[0]), int(data["height"].iloc[0])
        
        img = self.curr_img.crop((roi_l, roi_t - 5 ,self.w, roi_t + roi_h + 15  ))
        name = pytesseract.image_to_string(img, config= '--oem 3 --psm 1', lang='eng', output_type=pytesseract.Output.STRING)

        name = name.strip()
        name = re.sub("[nN][aA][Mm][Ee][\S]*","",name)
        
        name = re.sub("\n"," ",name)
        idx = re.search("\s{3,}",name)
        
        if(idx != None):
            i,j = idx.span()
            name = name[:i]
            
        return name
        

    def filterdata(self , data):

        data = pd.DataFrame(data)

        def iscontainname(x):
            x = x.lower()
            return (x=="pan" or x.find("name") != -1)
        
        temp = data["text"].apply(iscontainname)
        data = data[temp]

        data.index = data["text"].apply(lambda x : x.lower())

        self.data = data
    
        return data
            
    


    def findmumber(self,idx):

        i , j = idx.span()

        inx = re.search("[+]*[\d]{10,12}",self.curr_text[j : j+20])

        if(inx == None):
            return None
            
        k, m = inx.span()

        return self.curr_text[j+k:j+m]

    


    def findbranchcode(self,idx):

        i , j = idx.span()

        inx = re.search("[\d]{4,7}",self.curr_text[j : j+20])

        if(inx == None):
            return None
            
        k, m = inx.span()

        return self.curr_text[j+k:j+m]

        
        
    def findaccno(self,idx):

        i , j = idx.span()

        inx = re.search("[\d]{10,15}",self.curr_text[j : j+25])

        if(inx == None):
            return None
            
        k, m = inx.span()

        return self.curr_text[j+k:j+m]
    
    def findpanno(self):

        try:
            roi_l , roi_t =  self.data.loc["pan"].loc["left"] , self.data.loc["pan"].loc["top"] 
            roi_w , roi_h =  self.data.loc["pan"].loc["width"] , self.data.loc["pan"].loc["height"]

            image = self.curr_img.crop((roi_l,roi_t - 10,self.w , roi_t + roi_h + 10))
            text = pytesseract.image_to_string(image, config= '--oem 3 --psm 1', lang='eng', output_type=pytesseract.Output.STRING)
            text = re.findall("pan\s*no:*\s*([A-Za-z]{4}[1-9A-Za-z]{0,})", text.lower())[0].upper()

            return text


        except:

            return None
            

if(__name__ == "__main__"):
    
    img_path = r"C:\codes\python\newwwwwwwwww\images\test1.jpg"
    img = Image.open(img_path)
    scanner = Scanner()
    info = scanner.scan(img)
    print(info)