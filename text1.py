import re
from googletrans import Translator
import json
import os


        


class Jam_File_Translate:
    def __init__(self,path):
        self.text=None
        self.time=None
        self.time_text=[]
        self.open_data(path)
        self.set_time()
        self.set_text()
        self.trans_text()
        self.sort_data()
        self.connect_time_text()
        self.write_in_txt()

    def open_data(self,path):
        with open(path,"r",encoding="utf-8") as file:
            self.data=json.loads(file.read())

    def is_have_time(self):
        if self.time!=None:
            return True
        else:
            return False
    
    def is_have_text(self):
        if self.text!=None:
            return True
        else:
            return False
        
    def trans(self,word):
        transword=Translator().translate(text=word,src="zh-cn",dest="zh-tw")
        return transword.text

    def set_time(self):
        data=self.data["tracks"]
        time_list=[]
        for i in data:
            if i["type"]!="text": continue
            text_line=i["segments"]
            for j in text_line:
                time_info=j["target_timerange"]["start"]
                time_list.append(time_info//100000*3+time_info%100000//33333)
        if time_list==[]:
            self.time=None
            return
        self.time=time_list
    
    def set_text(self):
        if self.is_have_time():
            data=self.data["materials"]["texts"]
            text_list=[]
            count=0
            self.word=0
            for i in data:
                text_tag=i["content"]
                text_tag=re.sub(pattern='<(.|\n)+?>',repl='',string=text_tag)
                text_tag=text_tag.replace('[','')
                text_tag=text_tag.replace(']','')
                self.word+=len(text_tag)
                text_list.append(text_tag)
                print(f"Reading Line : No.{count+1:>6}")
                count+=1
            self.text=text_list
            print("Read Finish !!")
    
    def trans_text(self):
        count=0
        after_trans=[]
        while count<len(self.text):
            need_trans_word=""
            while count<len(self.text) and len(need_trans_word)<700:
                if need_trans_word=="": need_trans_word+=self.text[count]
                else:
                    need_trans_word+="@"+self.text[count]
                print(f"Translating Line : No.{count+1:>6}")
                count+=1
            word=self.trans(need_trans_word).split("@")
            after_trans.extend(word)
        self.text=after_trans
        print("Translate Finish !!")

    def sort_data(self):
        if self.is_have_time() and self.is_have_text():
            sort_text=[]
            sort_time=[]
            count=0
            for i in range(len(self.time)):
                smallval=min(self.time)
                smallvalpos=self.time.index(smallval)
                sort_text.append(self.text.pop(smallvalpos))
                sort_time.append(self.time.pop(smallvalpos))
                print(f"Sorting Line : No.{count+1:>6}")
                count+=1
            self.text=sort_text
            self.time=sort_time
            print("Sort Finish !!")
    
    def connect_time_text(self):
        for i in range(len(self.time)):
            print(f"Connecting Data :No. {i+1:>6}")
            ms,s,m,h=0,0,0,0
            ms=self.time[i]
            s,ms=ms//30,ms%30
            m,s=s//60,s%60
            h,m=m//60,m%60
            self.time_text.append(f"No.{i+1:>6}    [ {h:{0}>2}:{m:{0}>2}:{s:{0}>2}:{ms:{0}>2} ]   {self.text[i]}")
        print("Connect Finish !!")
    
    def write_in_txt(self):
        with open(os.path.expanduser("~")+"/Desktop/save_jam_word.txt","w",encoding="utf-8") as savefile:
            count=0
            for i in self.time_text:
                print(f"Saving Word : No.{count+1:>6}")
                savefile.write(i+"\n\n")
                count+=1
        print("Save Finish !!")

if __name__=="__main__":
    jam=Jam_File_Translate("draft_content.json")

