import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, strftime
from captcha.captcha import CaptchaClient
import base64
import time

def waituntil(s):
    while strftime('%H:%M:%S') < s:
        print strftime('%H:%M:%S')
        sleep(1)

def login():
    driver.get('https://www.irctc.co.in/eticketing/loginHome.jsf')
    cp = get_captcha(LOGIN_CAPTCHA_URL, driver.get_cookies())
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, 'j_username'))
        ).send_keys(IRCTC_USERNAME)
    driver.find_element_by_name('j_password').send_keys(IRCTC_PASSWORD)
    driver.find_element_by_name('j_captcha').send_keys(cp)
    driver.find_element_by_id('loginbutton').click()


def get_captcha(url, cookies_list=None):
    cookies = dict([(k['name'], k['value']) for k in cookies_list]) if cookies_list else {}    
    k = requests.get(url, cookies=cookies)
    cookies = k.cookies.get_dict()
    captcha_client = CaptchaClient(CAPTCHA_API_KEY)
    captcha_b64 = base64.b64encode(k.content)
    cap_id = captcha_client.submit_captcha_b64(captcha_b64)
    time.sleep(6)
    cp = captcha_client.get_solved_captcha(cap_id).upper() 
    print "Captcha is " + cp
    return cp


def planjourney():
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'jpform:fromStation'))
        ).send_keys(FROM_STATION)
    driver.find_element_by_id('jpform:toStation').send_keys(TO_STATION)
    driver.find_element_by_id('jpform:journeyDateInputDate').send_keys(DATE)    
    driver.find_element_by_id('jpform:jpsubmit').click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.NAME, 'quota'))
        )[0].click()    
    driver.find_element_by_id('cllink-%s-%s-%s' % (TRAIN_NO, CLASS, CLASS_INDEX)).click()
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.ID, '%s-%s-GN-0' % (TRAIN_NO, CLASS)))
        )[-1].click()

def filldetails():
    WebDriverWait(driver, 60).until(EC.title_contains('Book Ticket'))
    name_elements = driver.find_elements_by_class_name('psgn-name')
    age_el = driver.find_elements_by_class_name('psgn-age')
    gender =  driver.find_elements_by_class_name('psgn-gender')
    berth = driver.find_elements_by_class_name('psgn-berth-choice')    

    for i, psg in enumerate(PASSENGERS):
        print psg
        name_elements[i].send_keys(psg['name'])
        age_el[i].send_keys(psg['age'])
        Select(gender[i]).select_by_value(psg['gender'])
        Select(berth[i]).select_by_value(psg['berth'])

    mob_el = driver.find_element_by_id("addPassengerForm:mobileNo")
    mob_el.clear()
    mob_el.send_keys(MOBILE_NUMBER)    
    print "Set Mobile Number ", MOBILE_NUMBER, driver.find_element_by_id("addPassengerForm:mobileNo").get_attribute("value")
    cp = "Vivo V5"
    driver.find_element_by_id('addPassengerForm:autoUpgrade').click()    
    driver.find_element_by_id("nlpAnswer").send_keys(cp)
    driver.find_element_by_id("addPassengerForm:travelInsurance:1").click()
    driver.find_element_by_id("validate").click()

def initiate_payment():
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.ID, 'PREFERRED'))
        )[0].click()
    driver.find_element_by_id('validate').click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'debit'))
        ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, 'Ecom_Payment_Card_Number'))
        ).send_keys("12345")

    Select(driver.find_element_by_name('Ecom_Payment_Card_ExpDate_Month')).select_by_value("5")
    Select(driver.find_element_by_name('Ecom_Payment_Card_ExpDate_Year')).select_by_value("2020")
    driver.find_element_by_name('Ecom_Payment_Card_Name').send_keys("Ritesh")
    driver.find_element_by_name('Ecom_Payment_Pin').send_keys("1234")
    driver.find_element_by_id("SubmitBtn").click()


IRCTC_USERNAME = 'ritesh_85'
IRCTC_PASSWORD = 'Micks_com'
FROM_STATION = 'SURAT - ST'
FROM_STATION_CODE = 'BDTS'
TO_STATION = 'RANCHI - RNC'
TO_STATION_CODE = 'RNC'
DATE = '19-12-2016'
TRAIN_NO = '13426'
CLASS = '3A'
CLASS_INDEX = '1'
PASSENGERS = [
    {
        "name": "Bhusan Tuli",
        "age": 18,
        "gender": "M",
        "berth": "LB"
    }
]

MOBILE_NUMBER = '9824587433'


SBI_USERNAME = 'SBI_USERNAME'
SBI_PASSWORD = 'SBI_PASSWORD'
CAPTCHA_API_KEY = '82868d30e4365251d3345d809cbef7cb'
LOGIN_CAPTCHA_URL = 'https://www.irctc.co.in/eticketing/captchaImage'


if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/riteshkadmawala/Downloads/chromedriver')
    login()
    planjourney()
    filldetails()
    initiate_payment()
    # sbi()
