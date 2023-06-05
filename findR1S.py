from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import pyperclip
import time
from pushover import Pushover
from datetime import datetime
import pdb
import json

def findR1S(driver,rivUser,rivPass, poKey, poUser):
    print("Logging In")

    url = "https://rivian.com/account?dest=/vehicle-shop/list"
    driver.get(url)
    driver.set_window_size(1920, 1080)

    time.sleep(2)
    pyperclip.copy(driver.page_source)
    print("\tLoading Page")
    ele = driver.find_element(By.XPATH, '//button[text()="Accept"]')
    driver.execute_script("arguments[0].click();",ele)

    print("\taccepted cookies")
    e = driver.find_element(By.ID,"react-container")
    e.send_keys("\t")
    time.sleep(0.2)
    e.send_keys(rivUser)
    e.send_keys("\t")
    time.sleep(0.2)
    e.send_keys(rivPass)
    e.send_keys("\t")
    print("\t\tForm Data Signed In")

    driver.save_screenshot("sign_in.png")

    eleSignIn = driver.find_element(By.CLASS_NAME,"StyledButton--1iolf8y")
    driver.execute_script("arguments[0].click();",eleSignIn)
    print("\t\tClicked Sign In")

    print("\t\tWaiting for Trucks to Load")
    time.sleep(8)

    ####Close Explore StyledButton
    driver.save_screenshot("veh_before.png")
    try:
        ele = driver.find_element(By.XPATH, '//button[text()="Explore"]')
        driver.execute_script("arguments[0].click();",ele)
        print("\t\tClicked Explore")
    except Exception:
        print("error in clicking Explore")
    time.sleep(2)
    driver.save_screenshot("veh_after.png")

    #pyperclip.copy(driver.page_source)
    print("\t\tLooking For R1S")
    bFound = 0
    eleWAO_text = ""
    try:
        eleWAO = driver.find_element(By.CLASS_NAME,"css-0")
        eleWAO_text = eleWAO.text
        print("\t\tCC-0 node found")
    except Exception:
        eleWAO_text = ""
        print("\t\tNo CC-0 node found")

    #driver.save_screenshot("last_veh.png")
    #print("\t\tSaved Screenshot")

    if eleWAO_text == "We’re all out for now.Check back tomorrow — we refresh availability daily.":
        print("... All Out, check back Later")
        #po = Pushover("aun44pn9uspcsg7h7n3virt98nq7ff")
        #po.user("ui6kr1gtm42mpu4mo7zqn15bvabw1i")
        #msg = po.msg("nothing found")
        #msg.set("title", "Script is working")
        #po.send(msg)
    else:
        print("We Found Some R1S!!!!!")

        po = Pushover(poKey)

        eddType = driver.find_elements(By.CLASS_NAME,"css-e6wt1r")
        eddMotor = driver.find_elements(By.CLASS_NAME,"css-llqneu")
        eddCost = driver.find_elements(By.CLASS_NAME,"css-7y5vrb")

        eddExt = driver.find_elements_by_xpath("//*[contains(text(), 'exterior color')]")
        eddWheel = driver.find_elements_by_xpath("//*[contains(text(), 'wheel and tire')]")
        eddInt = driver.find_elements_by_xpath("//*[contains(text(), 'interior')]")

        count = 0
        mss = "Searched"

        with open('foundLast.json', 'r') as openfile:
            rivListLast = json.load(openfile)

        rivListNew = {"r1s":[]}


        cFind = 0
        for e in eddExt:
            tt = eddType[count].text + "\r\n"+ eddMotor[count].text + "\r\n"+eddCost[count].text + "\r\n"+eddExt[count].text +"\r\n"+eddWheel[count].text +"\r\n"+eddInt[count].text +"\r\n\r\n"
            rivListNew["r1s"].append(tt)
            if tt in rivListLast["r1s"]:
                print(tt + "\r\n was in last found")
            else:
                mss = mss + tt
                cFind = cFind + 1
            count = count + 1

        print('Cfind = '+ str(cFind))
        json_object = json.dumps(rivListNew, indent=4)

        # Writing to sample.json
        with open("foundLast.json", "w") as outfile:
            outfile.write(json_object)

        if cFind > 0:
            po.user(poUser)
            msg = po.msg(mss)
            msg.set("title", "Found "+str(cFind)+" R1S")
            po.send(msg)
            print("Sent Pushover")
        else:
            print("Nothing new to Pushover")

        now = datetime.now()
        ct = now.strftime("saved/%Y-%b-%d-%H_%M_%S.html")
        print(ct)
        txt = open(ct,"w")
        n = txt.write(driver.page_source)
        txt.close()
        print("saved page")
        ctI = now.strftime("saved/%Y-%b-%d-%H_%M_%S.png")
        driver.save_screenshot(ctI)
        print("took screen shot")
        #pdb.set_trace()



        driver.close()
        return 1



    print("Done")
    driver.close()
    return 0
