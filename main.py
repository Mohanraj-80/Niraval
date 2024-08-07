import scanimg
import content_writer
import tamil_amount_rocog_test
from PIL import Image
import cv2
import sys
sys.stdout.reconfigure(encoding='utf-8')



class Process:

    def __init__(self) -> None:

        depositChallanPath = r"images\deposit_challan.jpg"
        withdrawChallanPath = r"images\withdraw_challan.jpg"

        self.scanner = scanimg.Scanner()
        self.tamil = tamil_amount_rocog_test.getAmountDetails()


        self.writerDeposit = content_writer.writeDeposit(r"images\deposit_challan.jpg")
        self.writeWithdraw =content_writer.writeWithdraw(r"images\withdraw_challan.jpg")

        self.amount = 0
       
        self.isDeposit = True

        self.info_dict = dict()
    
    def getImage(self):

        imgPath= r"" + input("Enter the img path : ")
        self.img = Image.open(imgPath)

    def askMode(self):
        print("Withdraw or ")
        
    def scanAndPrint(self):

        print("Scanning the image....\n\n")
        self.info_dict = self.scanner.scan(self.img)
        print("Scanning successful\n\n")
        print("************************************************************************************")
        print("\n\nscanned information\n\n")

        for (key,value) in self.info_dict.items():
            print(key , " : " , value)


    def getAmount(self):

        self.info_dict["amount_list"] = {2000: 0, 500: 0, 200: 0, 100: 0, 50: 0}

        self.tamil.amount = 0
        self.amount = self.tamil.askAmount()
        self.info_dict["amount"] = self.amount

        self.isDeposit = self.tamil.isDeposit()

        if(self.isDeposit):
            self.info_dict["amount_list"] = self.tamil.askNoteCounts()

    def writeChallan(self):

        if(self.isDeposit):
            
            written_challan = self.writerDeposit.write(self.info_dict)
        
        else:

            written_challan = self.writeWithdraw.write(self.info_dict)

        cv2.imshow("Challan" , written_challan)
        if(cv2.waitKey(0) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
        cv2.destroyAllWindows() 

        
if(__name__ == "__main__"):

    flow = Process()
    flow.getImage()
    flow.scanAndPrint()