
# coding: utf-8

# In[1]:


import os
import json
import time


# In[2]:


class RenameData:
    def __init__(self):
        print("이미지 및 .json 파일 내의 데이터의 번호를 다시 매기는 프로그램입니다.")
        print("사용 전 반드시 원본 파일을 복사해 두시기 바랍니다.")
        print("")
        
    def set_info(self):
        check = True
        clear = lambda: os.system('cls')
        
        while True:
            json_file = input("\n** 번호를 다시 붙일 .json 파일의 경로를 입력하세요: \n>>> ") 
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
            img_folder = input("\n** 번호를 다시 붙일 이미지 폴더의 경로를 입력하세요: \n>>>")
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
            
        while True:
            new_start = input("\n** 새로 시작할 번호를 입력하세요: \n>>>")
            
            if new_start.isdigit():
                self.new_start = int(new_start)
                print("번호를 저장하였습니다.")
                break
            else:
                print("정수를 입력해 주시기 바랍니다.")  
                time.sleep(3)
            
    def get_json(self):
        self.labels = []
        with open(self.json_file, encoding='UTF-16') as feedsjson:
            self.labels.extend(json.load(feedsjson))
        
    def match_data(self):
        page_urls = []
        self.new_labels = [] # 전처리 된 labels
        self.new_img_names = [] # 전처리 된 img names 
        duplicate_img_name = [] # 중복 데이터들의 img name
        print("\n.json 파일 내의 텍스트 데이터와 이미지 폴더 내의 데이터의 비교를 시작 합니다.")
        
        wrong_name = []
        
        for label in self.labels:   
            
            img_exist = os.path.isfile(self.img_folder + "/" + str(label[0]["img_name"]) + ".jpg")
            
            if img_exist == False:
                wrong_name.append(str(label[0]["img_name"]))
                
            
        print(" 데이터의 비교를 완료하였습니다.\n")
        
        if len(wrong_name) == 0:
            return True
        else:            
            print(" ", end="")
            for w in wrong_name:
                print(w, end =" ")
            print("\n " + "위의 데이터는 .json에는 존재하나 이미지 폴더에는 존재하지 않습니다.")
            print(" " + "데이터를 확인 후 다시 실행해 주세요")
            return False
        
        return True
        
    def rename_data(self):
        print(" 데이터의 이름을 변경합니다.")
        
        cnt = 0
        for label in self.labels:   
            old_name = self.img_folder + "/" + str(label[0]["img_name"]) + ".jpg"
            new_name = self.img_folder + "/" + str(cnt) + "a.jpg"
            
            os.rename(old_name, new_name)
            label[0]["img_name"] = cnt
            
            cnt += 1
        
        for i in range(0,cnt):   
            old_name = self.img_folder + "/" + str(i) + "a.jpg"            
            new_name = self.img_folder + "/" + str(i) + ".jpg"
            
            os.rename(old_name, new_name)
        
        
        with open(self.json_file, mode='w', encoding='UTF-16', errors='ignore') as f:
                feed = json.dumps(self.labels, ensure_ascii=False, indent=2)
                f.write(feed)
        
        cnt -= 1
        print(" 데이터의 이름을 모두 변경하였습니다.")
        print("마지막 데이터의 번호는 " + str(cnt) + "입니다.")
        


# In[3]:


RD = RenameData()

RD.set_info()
RD.get_json()

if RD.match_data():
    RD.rename_data()

