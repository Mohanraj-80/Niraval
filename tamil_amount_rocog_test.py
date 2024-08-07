import speech_recognition as sr
from googletrans import Translator
from word2number import w2n
import gtts as gs
import os
from pygame import mixer
import time
import app
from threading import Thread

if(__name__ == "__main__"):
    import sys
    sys.stdout.reconfigure(encoding='utf-8')


class speechManuplate:


    def __init__(self):
        self.r = sr.Recognizer()
        self.translator = Translator()
    
    def recoganize_voice(self,language = 'en',text = "Say something"):  
    
        with sr.Microphone() as source :
            self.r.pause_threscold = 0.8
            voice_data = "Nothing"
    
            try:
                print("....\n")
                app.ChatBot.addAppMsg("....")
                audio = self.r.listen(source,timeout=5)
                voice_data = self.r.recognize_google(audio,language=language)
                app.ChatBot.addUserMsg(voice_data)
                print(f"You said {language} : {voice_data}")
    
            except sr.UnknownValueError:
                #print("Google Cloud Speech-to-Text could not understand the audio.")
                return -1
    
            except sr.RequestError as e:
                #print(f"Could not request results from Google Cloud Speech-to-Text API; {e}")
                return -1

            except:
                 return voice_data

        return voice_data
    
        
    
    def translate_from_text(self,text,language_from = 'ta'):

        if(not text == "" ):
            result = self.translator.translate(text,src=language_from,dest='en')
            return result.text.lower()
        
        return text
    
    
    def getAmount(self):

    
        text = self.recoganize_voice('ta')
        if(text == -1 or text == ""):
            return -1
        text = text.replace(',','')
        text = text.replace('₹','')
        text = text.split()
        digits = [0]
        nextmul = [None]
        for t in text:
            digit = None

            if(t == "நாலு"):
                digit = 4     
                digits.append(digit)
                nextmul.append(False)
                continue
            try:
                digit = int(t)
                digits.append(digit)
                nextmul.append(False)
    
            except ValueError:
                try:
                    numeric = self.translate_from_text(t,"ta")
    
                    numeric = numeric.lower()
    
                    if(numeric == 'lakh'):
                        digit = 100000
                    else:
                        digit = w2n.word_to_num(numeric)
                
                    digits.append(digit)
                    nextmul[-1] = True
                    nextmul.append(False)
                
                except:
                    if(t.find("ஞ்") != -1):
                        digits.append(5)
                        nextmul.append(False)
                    elif(t.find('ஒரு') != -1):
                        digits.append(1)
                        nextmul.append(False)
                    elif(t.find("மூணு") != -1):
                        digits.append(3)
                        nextmul.append(False)
                    else:
                        pass
                        #print("cannot recogonizeeeeee")
        
            except:
                pass
                #print("cannot recogonize")
        
        i = 1
        total_amount = 0  
        while(i < len(nextmul)):
            if(nextmul[i]):
                total_amount += (digits[i]*digits[i+1])
                i+=1
            else:
                total_amount += digits[i]
        
            i+=1
    
        return total_amount 
    











class getAmountDetails: 

    def __init__(self):

        mixer.init()
        self.speak = speechManuplate()
        self.i = 0
        self.amount = -1
        
        
        self.notes_dict = {2000 : 0 , 500 : 0 , 200 : 0 , 100 : 0 , 50 : 0}
        self.notes = [2000,500,200,100,50]

    def intro(self):

        self.say("வணக்கம்")

        self.say("நோட்டு எண்ணிக்கையின் விவரங்களை சொல்லவும்")

    def say(self,text):

    
        print("\n",text,"\n")
        app.ChatBot.addAppMsg(text)
        file_name =  f"text{self.i}.mp3"
        audio = gs.gTTS(text,lang='ta')
        audio.save(file_name)

        mixer.music.load(file_name)
        mixer.music.play()
        
        
        while mixer.music.get_busy():
            continue

        mixer.music.stop()
        if(self.i != 0):
                os.remove(f"text{self.i -1}.mp3")
        self.i +=1


    def yesorno(self):
        

        text  = self.speak.recoganize_voice("ta-IN")
        if(isinstance(text,int)):
            textenglish = "no"
        else:
            textenglish = self.speak.translate_from_text(text,"ta")
        if("goo" in textenglish or 'grow' in textenglish or "yes" in textenglish or "right" in textenglish or "rig" in textenglish ):
            return True
        return False
    
        
    def sayNote(self,note,count):
        text = f"{note} ரூபாய் நோட்டுகள் மொத்தம் {count} ,சரி என்றால் சரி அல்லது நன்று என்று சொல்லவும் ,தவறு என்றால் தவறு என்று சொல்லவும்."  
        self.say(text)  


    def sayAmount(self,amount):
        text = f" நீங்கள் கூறிய தொகை {amount} , சரி என்றால் சரி அல்லது நன்று என்று சொல்லவும் ,தவறு என்றால் தவறு என்று சொல்லவும்"  
        self.say(text) 
    
    

    def askCount(self,note):
        text = f"எத்தனை {note} ரூபாய் நோட்டுகள் என சொல்லவும்"
        self.say(text)


    def askNoteCounts(self):
        n = 5
        i = 0
        total = 0

        while(self.notes[i] > self.amount):
            self.notes_dict[self.notes[i]] = 0
            i+=1

        while(i<n and total < self.amount):
            self.notes_dict[self.notes[i]] = 0
            self.askCount(self.notes[i])
            count  = self.speak.getAmount()
            if(isinstance(count,int)):
                count =  count if count != -1 else 0
                self.notes_dict[self.notes[i]] = count
                total += (count*self.notes[i])
                
            time.sleep(3)
            i+=1
        
        if(total != self.amount):
            self.say(" நீங்கள் அளித்த தகவலை சரிபார்க்கவும்")

        return self.notes_dict
            

    def isDeposit(self):

        text = "பணம் செலுத்த வேண்டும் என்றால் சரி அல்லது நன்று  என சொல்லவும்."
        self.say(text)

        self.deposit = self.yesorno()

        return self.deposit
    

    def askAmount(self):


        while(self.amount <= 0):

            text = "மொத்தத் தொகையை சொல்லவும்"
            result = False
            self.say(text)
            self.amount = self.speak.getAmount()
            if(self.amount==-1):
                self.say("தயவுசெய்து பதிலளிக்கவும்")
            else:
                self.sayAmount(self.amount)
                result = self.yesorno()
                print(result)
            
            
            if(not result):
                self.amount = -1
        return self.amount
    
    def startChatBot(self):
        t1 = Thread(target= app.ChatBot.start)
        t1.start()
        while not app.ChatBot.started:
            time.sleep(0.5)
        self.say("நிரவல் தங்களை அன்புடன் வரவேற்கிறது !")
            

        
            

    def getTotal(self,say = False):

        total = 0
        for key in self.notes_dict.keys:

            total += (key * self.notes_dict[key])
        
        if(say):
            self.say(f"மொத்தம் {total} ரூபாய்")
        
        return total
    





if (__name__ == "__main__"):

    amountDetails = getAmountDetails()
    amountDetails.askAmount()
    amountDetails.askNoteCounts()
    print("Total_amount :" ,amountDetails.amount)
    print("Amount_count :  " , amountDetails.notes_dict)



