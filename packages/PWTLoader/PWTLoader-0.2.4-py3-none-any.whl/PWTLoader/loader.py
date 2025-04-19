import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from pandas.io.stata import StataReader

class PWTLoader():
    def __init__(self):
        self.data=None
        self.labels={}

    def get_metadata(self,url="https://doi.org/10.34894/QT5BCC"):
        headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        }
        try:
            #Fetch the Page
            response=requests.get(url)
            content=response.text

            #Parse HTML and extract JSON-LD Metadata
            try:
                soup=BeautifulSoup(content,"lxml")
            except:
                try:
                    soup=BeautifulSoup(content,"xml")
                except:
                    soup=BeautifulSoup(content,"html5lib")
            json_ld_tag=soup.find("script",{"type": "application/ld+json"})
            json_ld=json.loads(json_ld_tag.string)
            datasets=json_ld["distribution"]
            return datasets
        except Exception as e:
            raise ValueError(f"An error occurred while loading data: {e}")

    #Function to obtain the latest Version
    def latest_versions(self,datasets):
            versions=[]
            find=True
            for file in datasets:
                if re.findall(f"^pwt.*\.dta$",file["name"]):
                    try:
                        version_try=int(file["name"][3:7])
                        versions.append(file["name"][3:7])
                        find=False
                    except:
                         continue
            if find:
                 raise ValueError("Main File not Found")
            versions.sort(reverse=True)
            lat_version=versions[0]
            self.version=lat_version
            return lat_version
            
    #Find and load main .dta file
    def load_data(self):
        datasets=self.get_metadata()
        version=self.latest_versions(datasets)
        missing=True
        for file in datasets:
            if re.search(f"^pwt{version}.dta$",file["name"]):
                missing=False
                label_file=StataReader(file["contentUrl"])
                self.labels=label_file.variable_labels()
                data=pd.read_stata(file["contentUrl"])
                break
        if missing:
                raise ValueError("Main .dta file is missing, kindly check URL or version and try again")
        return data
    
    def additional_data(self,merge=False):                    
        datasets=self.get_metadata()
        version=self.latest_versions(datasets)

        #Creating Empty list to store additional datafiles
        addlfiles={}
        for file in datasets:
            if re.search(f"^pwt{version}.+\.dta$",file["name"]):                #Searching for Files in the form of pwt1001..... .dta
                label_file=StataReader(file["contentUrl"])
                self.labels.update(label_file.variable_labels())
                data=pd.read_stata(file["contentUrl"])
                match = re.search(f"^pwt{version}.(.*)\.dta", file["name"])
                call=match.group(1)
                call=call.lstrip("-")                                           #Obtaining name of extra data in the file
                df1={
                     "name":file["name"],
                     "description":file["description"],
                     "shape":data.shape,
                     "df":data
                     }
                addlfiles[call]=df1
        if merge:
            first_key,first_val=next(iter(addlfiles.items()))
            merged=addlfiles[first_key]["df"]
            merged_files=[]
            for i in addlfiles:                                                 #Merges all additional files
                 if i != first_key:
                      merged=pd.merge(merged,addlfiles[i]["df"],how="outer",on=["countrycode", "year"])
                      merged_files.append(i["name"])
            addlfiles.clear()
            df1={'name':"Merged.dta","shape":merged.shape,"description":f"{merged_files.join(',')}","shape":merged.shape,"df":merged}
            addlfiles["Merged"]=df1                            
        return addlfiles


    #Describes Structure and data of all additional files
    def describe_additional(self,merge=False):              #by default assumed to output separately
         addlfiles=self.additional_data(merge)
         print("\n Summary of Additional Data Files:\n" + "-" * 50)
         for key,val in addlfiles.items():
              name=val.get("name","NA")
              desc=val.get("description","no description")
              shape=val.get("shape")
              print("\n")
              print(f" Dataset Key    : {key}")
              print(f" File Name      : {name}")
              print(f" DataFrame Size : {shape[0]} rows × {shape[1]} columns")
              print(f" Description    : {desc}")
              print("-" * 50)


                