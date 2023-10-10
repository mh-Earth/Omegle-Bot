from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from win10toast import ToastNotifier
import re

class OmegleBot():
    def __init__(self) -> None:
        self.toast = ToastNotifier()
        self.driver = webdriver.Chrome()
        self.isChatting:bool = True
        self.isStrangerActive:bool = True
        self.textboxClass:str = "chatmsg"
        self.disconnectBtnClass = "disconnectbtn"
        self.sendBntClass:str = "sendbtn"
        self.newChatBtnClass = "newchatbtnwrapper"
        self.strangerMessageClass = "strangermsg"
        self.strangerReplyWaitingCoolDown:int = 20

    def matchRegex(text:str):
        # regex F_ _ ,f_ _
        pattern = re.compile(r"[F,f]\d{2}") 
        return True if pattern.match(text) else False
    
    def send_notification(self):
        self.toast.show_toast(
        "Notification",
        "It's a f",
        duration = 20,
        threaded = True,
        )

    
    def startOmegle(self):

        self.driver.get("https://www.omegle.com")
        self.driver.find_element(By.ID,"textbtn").click()
        # open omegel
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))
            )
        except:
            self.driver.quit()

        checkBoxs = self.driver.find_elements(By.XPATH , "//input[@type='checkbox']" )
        for checkBox in checkBoxs:
            try:
                checkBox.click()
                # time.sleep(1)
            except Exception as e :
                pass
        self.driver.find_element(By.XPATH,"//input[@value='Confirm & continue']").click()

    def checkForReCAPTCHA(self):
# check for reCAPTCHA
        while True:
            try:
                reCAPTCHA = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']"))
            )
                # reCAPTCHA = self.driver.find_element(By.XPATH , )

                if reCAPTCHA:
                    print("Clear reCAPTCHA please!!!",end='\r')
                else:
                    break
            except:
                break

        # click message area and send masssage
        time.sleep(.5)
    
    def Chat(self,messages:list) -> None:

        try:
            message_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, self.textboxClass))
            )
        except:
            print("quitting now")
            self.driver.quit()

        # start chatting

        while True:
            self.isChatting = False if self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass).text.split("\n")[0] == "New" else True
            # wait for to coonect to stranger for 120s 
            message_area = WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, self.textboxClass)))
            # check 
            if self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass).text.split("\n")[0] == "New":
                disconnectbtn = self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass)
                time.sleep(1)
                disconnectbtn.click()

                
            if self.isChatting:
                # sending first message
                send_bnt = self.driver.find_element(By.CLASS_NAME , self.sendBntClass)
                for message in messages:
                    message_area.send_keys(message)
                    send_bnt.click()

                try:
                    # wait fro stranger reply .If disconnected than next stranger
                    try:
                        # wait for stranger reply for 20s
                        print("[+] New stranger connected")
                        # element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, self.strangerMessageClass)))
                        # wait
                        self.strangermsg = WebDriverWait(self.driver, self.strangerReplyWaitingCoolDown).until(EC.presence_of_element_located((By.CLASS_NAME, self.strangerMessageClass)))


                    except:
                        # Go to next stranger

                        if self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass).text.split("\n")[0] == "New":
                            print("[+] Stranger disconnected")
                            newchatbtnwrapper = self.driver.find_element(By.CLASS_NAME , self.newChatBtnClass)
                            newchatbtnwrapper.click()
                        else:
                            print("[+] Skipping stranger for not reply in 20s")
                            # if stanger dont reply in 20s than skip him
                            disconnectbtn = self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass)
                            disconnectbtn.click()
                            time.sleep(1)
                            disconnectbtn.click()
                            time.sleep(1)
                            disconnectbtn.click()

                    self.past_strangermsg = self.driver.find_element(By.CLASS_NAME,self.strangerMessageClass).text

                    if "m" in self.past_strangermsg.lower().split(" ") or "male" in self.past_strangermsg.lower().split(" "):
                        print("[+] Skipping for being a male")
                        self.isStrangerActive=False
                        disconnectbtn = self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass)

                        disconnectbtn.click()
                        time.sleep(.5)
                        disconnectbtn.click()
                        time.sleep(.5)
                        disconnectbtn.click()
                        self.past_strangermsg = ""
                        time.sleep(1)

                    else:
                        if "f" in self.past_strangermsg.lower().split(" "):
                            self.send_notification()
                        elif self.matchRegex(self.past_strangermsg.lower().split(" ")):
                            self.send_notification()
                        

                except:
                    pass
                    


                while self.isStrangerActive:
                    # chcek if stranger has diconnected . If disconnected than go for new 
                    if self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass).text.split("\n")[0] == "New":
                        print("[+] Stranger disconnected")
                        disconnectbtn = self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass)
                        time.sleep(1)
                        disconnectbtn.click()
                        break
                    # if not disconnected than keep chating until any one quits
                    try:
                        self.new_strangermsg = self.driver.find_elements(By.CLASS_NAME , self.strangerMessageClass)[-1].text
                    except Exception as e:
                        break
                        


                    if self.past_strangermsg == self.new_strangermsg:
                        print(self.new_strangermsg)
                        continue
                    else:
                        # if the stranger male than diconnect ()
                        self.past_strangermsg = self.new_strangermsg
                        if "m" in self.new_strangermsg.lower().split(" ") or "male" in self.new_strangermsg.lower().split(" "):
                            disconnectbtn = self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass)

                            disconnectbtn.click()
                            time.sleep(.5)
                            disconnectbtn.click()
                            time.sleep(.5)
                            disconnectbtn.click()
                            self.past_strangermsg = ""
                            break
                else:
                    self.isStrangerActive = True

            else:
                self.isStrangerActive = True
                disconnectbtn = self.driver.find_element(By.CLASS_NAME , self.disconnectBtnClass)
                disconnectbtn.click()
                time.sleep(.5)
                disconnectbtn.click()
                time.sleep(.5)
                disconnectbtn.click()  
                self.past_strangermsg = "" 
                time.sleep(1)


if __name__ == "__main__":
    a = OmegleBot()

    a.startOmegle()
    a.checkForReCAPTCHA()
    a.Chat(["M 19"])