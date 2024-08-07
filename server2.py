from fastapi import FastAPI , UploadFile , File
import uvicorn
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
from scanimg import Scanner
from content_writer import writeDeposit
from content_writer import writeWithdraw
import multiprocessing


scanner = Scanner()

app = FastAPI()
info_dict =     {'account no': '',
'phone': '',
'branch code': "",
'name': '',
"amount" : 0,
"pan no" : '' ,
"amount_list" : {2000 : 0 , 500 :0 , 200 : 0 , 100 : 0, 50 : 0 } }
   
amount = None

def generateinfo(img):

    img = BytesIO(img)
    img = Image.open(img)
    global info_dict 
    info_dict = scanner.scan(img)
    return info_dict

@app.get("/")
async def welocme():
    return "Welcome to Challan Printer"



@app.get("/getamount")
async def getamount(amount : int = 0) :
    global info_dict
    info_dict["amount"] = None
    return amount



@app.post("/getimage")
async def getimage(image : UploadFile = File(...)):

    info = generateinfo(await image.read())
    return info


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host= "192.168.185.3", port=8000)