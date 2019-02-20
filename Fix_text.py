
# coding: utf-8

# In[1]:


import requests, os
import bs4
from bs4 import BeautifulSoup

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from urllib import parse
import re
import lxml
import json
import sys
import os

# error url = https://www.instagram.com/p/BrkU-yYFtug/


# In[ ]:


class FixText:
    def __init__(self):
        print("이미지 및 .json 파일 내의 텍스트 데이터를 수정하는 프로그램입니다.")
        print("사용 전 반드시 원본 파일을 복사해 두시기 바랍니다.")
        print("")
        
    def set_info(self):
        check = True
        clear = lambda: os.system('cls')
        
        while True:
            json_file = input("\n** 텍스트를 수정할 .json 파일의 경로를 입력하세요: \n>>> ") 
            json_exist = os.path.isfile(json_file)
            x, ext = os.path.splitext(json_file)

            if json_exist: 
                if ext == ".json":
                    self.json_file = json_file
                    print("경로를 저장하였습니다.")
                    break
                else:
                    print("입력한 파일의 확장자가 .json이 아닙니다.") 
                    print("다시 입력해 주세요.")
                time.sleep(3)
            else:
                print(".json 파일의 경로를 잘못입력하셨습니다.")
                print("다시 입력해 주세요.")
                time.sleep(3)
                
            clear()    
            
    def get_newText(self, url):
        hashtag = []
        text = "deleted post,2015112222LunaJang"
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.execute_script("return document.documentElement.innerHTML")
        time.sleep(2)
        soup = BeautifulSoup(html, "lxml")
        
        title = soup.find("title").text
        title = title.strip()
        
        if(title == "페이지를 찾을 수 없습니다 • Instagram" or title == "Page Not Found • Instagram"):
            print(" 해당 게시물은 삭제되어 더 이상 접근할 수 없습니다.")
        else: 
            source = soup.find("li", {"class": "gElp9 "})
            source = source.find("span")

            hashtag_source = source.find_all("a")

            for hs in hashtag_source:
                hashtag.append(hs.string)

            text = source.text

        return text, hashtag

    def get_json(self):
        self.labels = []
        with open(self.json_file, encoding='UTF-16') as feedsjson:
            self.labels.extend(json.load(feedsjson))
    
    def fix(self):
        print(" 텍스트 데이터를 변경합니다.")
        
        for label in self.labels:   
            print(label[0]["img_name"], ":", label[0]["page_url"])
            text, hashtag = self.get_newText(label[0]["page_url"])
            
            if(text == "deleted post,2015112222LunaJang"):
                print(" ", label[0]["img_name"], "번 이미지")
            else:
            
                label[0]["text"] = text
                label[0]["hashtag"] = hashtag

                with open(self.json_file, mode='w', encoding='UTF-16', errors='ignore') as f:
                        feed = json.dumps(self.labels, ensure_ascii=False, indent=2)
                        f.write(feed)
        
        print(" 데이터를 모두 수정하였습니다.")


# In[ ]:


FT = FixText()

FT.set_info()
FT.get_json()

FT.fix()

