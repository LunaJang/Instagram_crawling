
# coding: utf-8

# In[1]:


#-*- coding:utf-8 -*-

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


# In[2]:


class Instagram_crawler:
    def crawling_data(self, tag, no_of_scroll, start_page):
        
        self.tag = tag
        self.tag_url = "www.instagram.com/explore/tags/" + self.tag
        self.tag_url = "http://" + parse.quote(self.tag_url)
        print('\n', self.tag_url, '\n')
        
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('disable-gpu')

        self.browser = webdriver.Chrome('chromedriver', options=option)

        # browser = webdriver.Chrome()
        self.browser.get(self.tag_url)
        time.sleep(3)
        
        print('start to get shortcode')
        
        for i in range(1, start_page):
            self.scroll_page()
        
        i = 0
        total_saved_data = 0
        shortcodes = []
        while i < no_of_scroll:
            # get html code
            soup = self.scroll_page()
            # get the list of shortcode
            shortcodes.extend(self.get_shortcode_list(soup))            
            print()
            i+=1
        
        print('\nstart to get data')
        shortcodes = list(set(shortcodes))
        saved_data = self.save_data(shortcodes)
        print('  saved data :', saved_data)
        
    # scroll url page num times and get html data
    def scroll_page(self):
        body = self.browser.find_element_by_tag_name("body")   
        no_of_pagedowns = 8;
        
        while no_of_pagedowns:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            no_of_pagedowns-=1

        response = self.browser.page_source
        soup = BeautifulSoup(response, 'lxml')
        print(" read the HTML file")

        return soup
    
    def create_folder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)
    
    # return the list of shortcode from html code
    def get_shortcode_list(self, soup):
        article = soup.find("article")
        href = article.find_all('a')

        shortcodes = []

        for h in href:
            shortcodes.append(h['href'])

        print(" get ", len(shortcodes) - 9, " shortcodes")

        return shortcodes[9:]


    # return the text from html code
    def get_text(self, page):
        script = page.find_all("script")[3].string
        script_split = re.split(':|,|\"|\'|\{|\}|\[|\]',script)  
        text_index = script_split.index('text') + 3
        text = script_split[text_index]  

        text = text.replace('\\n','')

        text = text.encode('utf-8', 'surrogatepass')
        text = text.decode('unicode_escape')
        
        words = text.replace("#"," #")
        words = re.split(' ',words)          
        hashtag = []        
        for w in words:
            if '#' in w:
                hashtag.append(w)
        
        return text, hashtag

    # return the user_id and number of likes from html code
    def get_id_likes(self, description):
        data = re.split('on Instagram:', description)

        data = re.split(",|\(|\)|@|Likes|Comments|-| ",data[0])
        while '' in data : data.remove('')

        likes = data[0]
        user_id = data[-1]

        return user_id, likes

    # return the text, user_id, number of likes from html code
    def get_labels(self, page):
        for tag in page.select('meta[property*=image]'):
            image_url = tag['content']

        for tag in page.select('meta[property*=og:description]'):
            description = tag['content']

        text, hashtag = self.get_text(page)
        user_id, likes = self.get_id_likes(description)

        return text, hashtag, user_id, likes

    # save image in page
    def save_image(self, page, num):
        for tag in page.select('meta[property*=image]'):
            image_url = tag['content']

        pic_response = requests.get(image_url).content
        img_name = "./dataset/img/" + self.tag + "/"+ str(num) + ".jpg"

        with open(img_name, 'wb') as f:
            f.write(pic_response)
        print(" file saved: ", img_name)    

    # get html file of "https://www.instagram.com" + shortcode page, and get data (likes, user_id, text, hashtag)
    def save_data(self, shortcodes):
        i = 1
        saved_data = 0
        file_name = "./dataset/label_" + self.tag +  ".json"
        self.create_folder("./dataset/img/" + self.tag)
        
        if not os.path.isfile(file_name):
            saved_data = 0
        else:
            with open(file_name, encoding='UTF-16') as feedsjson:
                old_feeds = []
                old_feeds.extend(json.load(feedsjson))
                # saved_data = len(old_feeds)
                temp = old_feeds[-1]
                temp = temp[0]
                saved_data = int(temp["img_name"]) + 1
                
        
        for shortcode in shortcodes:
            print("[ ", i, ' ]')
            i = i + 1  
            label_data = []

            try:
                # get html code
                page_url = "https://www.instagram.com" + shortcode
                print(' ', page_url)
                response = requests.get(page_url).content
                page = BeautifulSoup(response, 'lxml')        

                # get label data
                text, hashtag, user_id, likes = self.get_labels(page)

                # save label data 
                output = {"page_url":page_url, "img_name":saved_data, "label":self.tag, "likes":likes, "user_id":user_id, "text":text, "hashtag":hashtag}
                label_data.append(output)

                if not os.path.isfile(file_name):
                    with open(file_name, mode='w', encoding='UTF-16', errors='ignore') as f:
                        data = []
                        data.append(label_data)
                        new_feed = json.dumps(data, ensure_ascii=False, indent=2)
                        f.write(new_feed)
                else:
                    with open(file_name, encoding='UTF-16') as feedsjson:
                        old_feeds = []
                        old_feeds.extend(json.load(feedsjson))
                    old_feeds.append(label_data)
                    with open(file_name, mode='w', encoding='UTF-16', errors='ignore') as f:
                        new_feed = json.dumps(old_feeds, ensure_ascii=False, indent=2)
                        f.write(new_feed) 

                # save image files
                self.save_image(page, saved_data)

                print(" Okay\n")
                saved_data += 1

            except:
                print(" Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
                print(" Line ", sys.exc_info()[-1].tb_lineno)
                print(" Not okay\n")

        return saved_data


# In[3]:


tag = input("\n** 원하는 태그를 입력하세요: \n>>> ")
no_of_scroll = input("\n** 스크롤 할 페이지 수를 입력하세요.\n 한 페이지마다 약 35~40개의 데이터가 획득됩니다: \n>>> ")
start_page = input("\n** 스크롤을 시작할 페이지 번호를 입력하세요.\n 맨 처음 데이터부터 가져오고 싶다면 1을 입력하세요: \n>>> ")


# In[4]:


ic = Instagram_crawler()

start = time.time()

ic.crawling_data(tag, int(no_of_scroll), int(start_page))

end = time.time()
seconds = int(end - start)
minutes, seconds = divmod(seconds, 60)
print('  take ', minutes, 'mim', seconds, 'sec')

