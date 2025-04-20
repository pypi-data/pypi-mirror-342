import json
import time
from time import sleep

import requests

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class kakaoapi:
    def __init__(self, api_key, redirect_uri ,kakaoId, kaakaoPw):
        self.api_key = api_key
        self.redirect_uri = redirect_uri
        self.kakaoId = kakaoId
        self.kakaoPw = kaakaoPw
        self.code = None
        self.access_token = None
        self.get_token_url = 'https://kauth.kakao.com/oauth/token'
        self.send_message_url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'

    def get_code_from_kakaoauth(self):

        print("In Process of getting code from Kakao Auth...")
        url = f"https://kauth.kakao.com/oauth/authorize?client_id={self.api_key}&redirect_uri={self.redirect_uri}&response_type=code"

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, 'loginId')))

        kakao_id_input = driver.find_element(By.NAME, 'loginId')
        kakao_id_input.send_keys(self.kakaoId)
        kakao_pw_input = driver.find_element(By.NAME, 'password')
        kakao_pw_input.send_keys(self.kakaoPw)
        kakao_login_button = driver.find_element(By.CSS_SELECTOR, '#mainContent > div > div > form > div.confirm_btn > button.btn_g.highlight.submit')
        kakao_login_button.click()

        print("Waiting for Kakao Login...")
        try:
            wait = WebDriverWait(driver, 3)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#line_ctr > label > span.ico_agree.ico_chk')))

            agreement_btn = driver.find_element(By.CSS_SELECTOR, '#line_ctr > label > span.ico_agree.ico_chk')
            agreement_btn.click()
            agree_continue_btn = driver.find_element(By.CSS_SELECTOR, '#txt_accept_button_agree')
            agree_continue_btn.click()
        except Exception as e:
            print("")

        try:
            # Wait for the user to log in and authorize the app
            WebDriverWait(driver, 10).until(EC.url_contains(self.redirect_uri))
            self.code = driver.current_url.split('code=')[1]
            # print(f"Authorization code: {self.code}")
        except Exception as e:
            print(f"Error: {e.__class__}")
        finally:
            driver.quit()

    def get_new_token(self):
        print("In Process of getting new token...")
        url = self.get_token_url
        data = {
            "grant_type": "authorization_code",
            "client_id": self.api_key,
            "redirect_uri": self.redirect_uri,
            "code": self.code
        }

        response = requests.post(url, data=data)
        res_json = response.json()

        # print(res_json)
        try:
            self.access_token = res_json['access_token']
        except KeyError:
            print("Error: 'access_token' not found in the response.")
            self.access_token = None

    def send_text_msg(self, text_):
        self.get_code_from_kakaoauth()
        self.get_new_token()
        print("Sending message...")
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

        # print("Access Token: ", self.access_token)
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        data = {
            "object_type": "text",
            "text": text_,
            "link": {
            },
        }
        data = {"template_object": json.dumps(data)}
        response = requests.post(url, headers=headers, data=data)

        print(f"response status : {response.status_code}")
