
import time
from selenium.webdriver.common.by import By
import getpass
import multiprocessing
import random
import chrome_simplifier
import logging
from text_generator import *
from bs4 import BeautifulSoup
import threading

#We may have to have our own custom webdriver selector file with these custom options to ensure translation:
#https://stackoverflow.com/questions/54042910/how-can-i-translate-the-webpage-opened-via-selenium-webdriver-to-english-using-p
#nah we need a one off file so we can make our initial training data set
logging.basicConfig(filename='logfile.log',level=logging.WARNING)
SHOW_URL= None

#'/usr/local/bin/chromedriver',
driver =chrome_simplifier.chrome(headless=False)
CURRENTLY_STREAMING=False
spamproc=None
checkproc=None
chatproc=None
lockval=False
pagesource=None
chatarray=["This stream is great!"]

def getlatestchat():
    global driver

    #while True:
        #time.sleep(random.randint(5,25))
    page_source=driver.page_source
    if page_source is not None:
        try:
            soup=BeautifulSoup(page_source,"html.parser")
            chatdivs=soup.find_all("div", {"chat-row-wrap paddinglr-3 clickable"})

            chatelementlist = []
            for chatelement in chatdivs:
                mylist = str(chatelement.text).split('\n')
                for item in mylist:
                    if len(item.strip(' ')) > 0 and len(mylist) > 3 and len(item.strip('    :')) > 0:
                        chatelementlist.append(item.strip(' '))

            #returnarray=[]
            #for chatelement in chatdivs:
            #    chatstring=str(chatelement.text).split('\n')[-1]
            #    if chatstring != "just followed!" and len(chatstring.strip(" ")) > 0:
            #        returnarray.append(chatstring)
            return chatelementlist

            #uses the current chat at the current url to get all the text from it and returns it in an array
            #page=requests.get(url)
            #soup=BeautifulSoup(page.content,'html.parser')
            #chatdivs=soup.findAll("div", {"class": "chat-row-wrap.paddinglr-3.clickable"})
            #time.sleep(5)
            #chatelements=driver.find_elements_by_class_name("chat-row-wrap.paddinglr-3.clickable")

            #for element3 in chatelements:
            #    chatstring=str(element3.text).split('\n')[-1]
            #    if chatstring!="just followed!" and len(chatstring)>0:
            #        returnarray.append(chatstring)#how dlive formats their chat for whatever reason who knows
            #latestvalues = int(len(returnarray) * .75)
            #returnarray=returnarray[latestvalues:]
            #chatarray=returnarray

        except Exception as e1:
            print("in chatripper "+str(e1))
            #print(e1)
    else:
        print("in getlatestchat pagesource is none.")


def check_if_streaming():
    global CURRENTLY_STREAMING
    global spamproc
    #global checkproc
    #global chatproc
    global driver
    page_source=driver.page_source
    #print(page_source)
    try:
        if page_source is not None:
            soup=BeautifulSoup(page_source,"html.parser")
            mydivs = soup.find_all("div", {"class": "text-14-medium text-white"})
            for div in mydivs:
                if "Streamer is offline" in div.text:
                    CURRENTLY_STREAMING=False
                    try:
                        spamproc.terminate()
                        #checkproc.terminate()
                        #chatproc.terminate()
                    except Exception as ea:
                        print("Nothing has started yet, waiting for stream to start...")

                    return False
            return True
        else:
            print("in check_if_streaming pagesource is None")
            return False


    except Exception as e2:

        print("In check_if_streaming: "+str(e2))


def createresponse():
    global chatarray
    print(chatarray)
    #fullripchat=ripchat(driver,SHOW_URL)
    latestvalues = int(len(chatarray) * .75)
    textprompt=random.choice(chatarray[latestvalues:])
    return returngeneratedtext(textprompt)

def textspam():
    global driver
    try:
        #print("generating the text...")
        bestresponse=createresponse()
        #print(bestresponse)
        #print("finding the input area...")
        parentelement=driver.find_element_by_class_name("v-input.textarea.height-100.v-textarea.v-textarea--no-resize.v-text-field.v-text-field--single-line.v-text-field--solo.v-text-field--enclosed.v-text-field--placeholder.v-input--hide-details.theme--dark")
        #print("finding the textarea...")
        inputelement=parentelement.find_element_by_tag_name("textarea")
        #print("generating the text and putting it in to the textarea...")
        inputelement.send_keys(bestresponse)
        #print("finding the button...")
        buttonelement = driver.find_element_by_class_name("d-btn.border-radius-3.text-14-medium.no-select.flex-all-center.text-nowrap.position-relative.text-12-medium.marginl-3.btnC.clickable")
        #print("clicking the button")
        buttonelement.click()
        #print("text spammed!")

    except Exception as e3:
        print("can't send text..."+str(e3))
        #print(e)

def stickerSpam():
    global driver
    try:
        emotebutton = driver.find_element_by_class_name("emote-btn.height-100.flex-all-center.clickable")
        emotebutton.click()
        time.sleep(random.random()+2)
        stickertabs=driver.find_elements_by_class_name("tab-parent.clickable")
        time.sleep(random.random()+2)
        mystickertab=None
        for tab in stickertabs:
            if "Sticker" in str(tab.text):
                mystickertab=tab
        mystickertab.click()
        time.sleep(random.random()+2)
        myemotes = driver.find_elements_by_class_name("emote-item.position-relative")
        if len(myemotes) < 2:
            raise ValueError("YOU NEED MORE STICKERS FOR THIS TO WORK")
        time.sleep(random.random()+2)
        random.choice(myemotes).click()

    except Exception as e4:
        print("can't find sticker..."+str(e4))
        #print(e)

def inputsimulator():
    while True:
        starttime=time.time()
        simplechoice=random.randint(0,100)
        if simplechoice<80:
            print("debug: trying text spam now")
            textspam()
        else:
            print("debug: trying sticker spam now")
            stickerSpam()
        endtime=time.time()
        endvalue=0
        if endtime-starttime<33:
            endvalue=endtime-starttime
        randomdelay=random.randint(0,5)+endvalue
        #textspam()
        #stickerSpam()
        #randomdelay = random.randint(0, 5) + 33

        time.sleep(randomdelay)

def signIn(emailaddress,mypassword):
    global driver
    driver.get(SHOW_URL)
    driver.find_element(By.CSS_SELECTOR, ".sign-in-button span").click()
    #emailbox = driver.find_element_by_xpath("//input[@placeholder='Email Address']")
    #passbox=driver.find_element_by_xpath("//input[@placeholder='Password']")
    #emailbox.send_keys(emailaddress)
    #passbox.send_keys(mypassword)
    #driver.find_element(By.CSS_SELECTOR, ".clickable:nth-child(4) > .d-btn-content").click()
    ##Note that I'll find a way to get this to bypass captcha so that it can work headless mode, but for now...
    checking = input("Hit enter on this screen once successfully logged in!")

###IT WORKS!!!
def checkForChest():
    global driver

    #while True:
    page_source=driver.page_source
    #time.sleep(5)
    if page_source is not None:
        try:
            soup=BeautifulSoup(page_source,"html.parser")
            chestdivs=soup.find_all("div",{"treasure-chest-popup"})
            if len(chestdivs)>0:
                chestdiv=driver.find_element_by_class_name("treasure-chest-popup")
                mychestelements=chestdiv.find_elements_by_tag_name('span')
                for chestelement in mychestelements:
                    if len(str(chestelement.text)) > 0:
                        if "Collect Rewards" in str(chestelement.text):
                            chestelement.click()
                            print("GOT THEM LEMS NIBBA")
                            #time.sleep(20)
        except Exception as e5:
            print("in checkforchest: "+str(e5))
            #print(e)


def mainfunction():


    #modify these for future use when we can bypass captcha and auto login
    emailaddress = "dummy"#input("Please enter your email address: >")
    dlivepass="dummy"#getpass.getpass(prompt="Please enter your dlive password (it will not be shown!) >", stream=None)

    signIn(emailaddress,dlivepass)

    #monitorproc = multiprocessing.Process(target=monitorthread)
    #print("starting monitoring...")
    #monitorproc.start()

    while True:
        global CURRENTLY_STREAMING
        global spamproc
        global checkproc
        global chatarray
        # only run when hambone is streaming
        #global pagesource
        #print(pagesource)
        #pagesource = driver.page_source
        time.sleep(1)
        checkForChest()

        chatarray=getlatestchat()

        if (check_if_streaming()):
            if not CURRENTLY_STREAMING:
                print("target is streaming... starting now")
                # now comes the magic. Begin the spam routine...

                #checkproc = multiprocessing.Process(target=checkForChest)
                #spamproc = multiprocessing.Process(target=inputsimulator)
                #chatproc=multiprocessing.Process(target=getlatestchat)
                #checkproc = threading.Thread(target=checkForChest)
                spamproc = threading.Thread(target=inputsimulator)
                #chatproc=threading.Thread(target=getlatestchat)
                #print("starting checkproc")
                #checkproc.start()
                print("starting spamproc")
                spamproc.start()
                #print("starting chatproc...")
                #chatproc.start()
                CURRENTLY_STREAMING = True

if __name__ == '__main__':
    SHOW_URL = input("Enter the url for the DLive Stream >")
    mainfunction()
