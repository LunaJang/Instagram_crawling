#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding:utf-8 -*-

import os
import json
import time


# In[2]:


class ProcessData:
    def set_address(self):
        check = True
        clear = lambda: os.system('cls')
        
        while True:
            json_file = input("\n** 전처리를 진행할 .json 파일의 경로를 입력하세요: \n>>> ") 
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
                
        while True:
            img_folder = input("\n** 전처리를 진행할 이미지 폴더의 경로를 입력하세요: \n>>>")
            img_folder_exist = os.path.isdir(img_folder)
            
            if img_folder_exist:
                self.img_folder = img_folder
                print("경로를 저장하였습니다.")
                break
            else:
                print("이미지 폴더의 경로를 잘못입력하셨습니다.")  
                print("다시 입력해 주세요.")
                time.sleep(3)
                
            clear()    
            
    def get_json(self):
        self.labels = []
        with open(self.json_file, encoding='UTF-16') as feedsjson:
            self.labels.extend(json.load(feedsjson))
        
    def delete_duplicate(self):
        page_urls = []
        self.new_labels = [] # 전처리 된 labels
        self.new_img_names = [] # 전처리 된 img names 
        duplicate_img_name = [] # 중복 데이터들의 img name
        print("\n중복 데이터 검색을 시작합니다.")
        
        for label in self.labels:   
            if label[0]["page_url"] not in page_urls:
                self.new_labels.extend([label])
                page_urls.append(label[0]["page_url"])
                self.new_img_names.append(label[0]["img_name"])
            else:
                index = page_urls.index(label[0]["page_url"])
                name = self.new_img_names[index]
                print(label[0]["img_name"], "가 ", name, "과 중복됩니다.")
                duplicate_img_name.append(label[0]["img_name"])
                
        print("중복된 파일 : ", duplicate_img_name)
        user_select = input("**중복된 파일을 삭제하시겠습니까? (1.예 2. 아니오)\n>>> ")
        
        if(user_select == "1"):        
            for img_name in duplicate_img_name:
                file = self.img_folder + "/" + str(img_name) + ".jpg"
                if os.path.isfile(file):
                    os.remove(file)

            with open(self.json_file, mode='w', encoding='UTF-16', errors='ignore') as f:
                feed = json.dumps(self.new_labels, ensure_ascii=False, indent=2)
                f.write(feed)

            print("총 ", len(duplicate_img_name), "개의 중복 데이터를 삭제하였습니다.")
        else:
            self.new_labels = self.labels
            self.new_img_names = []
            for label in self.labels:
                self.new_img_names.append(label[0]["img_name"])
            print("중복 데이터를 삭제하지 않습니다.")
        
    def delete_selected_data(self, select):
        file = self.img_folder + "/" + select + ".jpg"        
        img_exist = os.path.isfile(file)
        select = int(select)
        if img_exist and (select in self.new_img_names):
            os.remove(file)
            index = self.new_img_names.index(select)
                
            del self.new_img_names[index]
            del self.new_labels[index]
                
            with open(self.json_file, mode='w', encoding='UTF-16', errors='ignore') as f:
                feed = json.dumps(self.new_labels, ensure_ascii=False, indent=2)
                f.write(feed)
            return True
        elif img_exist:
            print(self.json_file, "에 해당 데이터가 존재하지 않습니다.")
            return False            
        elif select in self.new_img_names:
            print(file, " 파일이 존재하지 않습니다.")
            return False
        else:
            print(file, " 파일이 존재하지 않습니다.")
            print(self.json_file, "에 해당 데이터가 존재하지 않습니다.")
            return False
        
        
    def delete_data(self):
        print("\n사용자가 선택한 데이터의 삭제를 시작합니다.")
        print("삭제할 데이터의 이미지 번호를 입력하고 엔터를 치세요.")
        print("\n프로그램을 끝내려면 숫자가 아닌 아무 키나 입력하세요.")
        print("\n!!!주의!!!")
        print("삭제된 이미지 데이터는 휴지통으로 들어가지 않습니다. (=복구하기 어렵습니다.)\n")
        
        select = input("\n>>> ")
        while(True):
            try:
                temp = int(select)                
                if(self.delete_selected_data(select)):
                    print(select, " 삭제 완료")
                else:
                    print("확인 후 다시 입력해 주세요.")
                select = input("\n>>> ")
            except ValueError:
                break;
                
        print("프로그램을 종료합니다.")


# In[3]:


pd = ProcessData()

pd.set_address()


# In[4]:


pd.get_json()


# In[5]:


pd.delete_duplicate()


# In[6]:


pd.delete_data()

