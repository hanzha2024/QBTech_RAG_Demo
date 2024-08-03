# -*- coding: utf-8 -*-
from embdatabase_milvus import *
from embdatabase_faiss import *
import pandas as pd
from config import *


class Porject_DataBase():
    def __init__(self,path,name=None):
        global database_type
        if name is None:
            name = path

        if os.path.exists(os.path.join(path,"txt"))  == False:
            print(f"知识库{name}txt文件夹不存在,可能是不完整的知识库")
            exit(-999)
        if os.path.exists(os.path.join(path,"prompt.xlsx"))  == False:
            print(f"知识库{name}的prompt文件不存在,可能是不完整的知识库")
            exit(-998)
        if os.path.exists(".cache") == False:
            os.mkdir(".cache")

        self.prompt_data = pd.read_excel(os.path.join(path,"prompt.xlsx"),engine="openpyxl")

        self.document = Document(os.path.join(path,"txt"),name)

        if database_type == "Milvus":
            self.emb_database = EmbDataBase_Milvus(os.path.join("..","moka-ai_m3e-base"), self.document.contents,name)
        elif database_type == "Faiss":
            self.emb_database = EmbDataBase_Faiss(os.path.join("..","moka-ai_m3e-base"), self.document.contents, name)
        else: # default : faiss
            self.emb_database = EmbDataBase_Faiss(os.path.join("..","moka-ai_m3e-base"), self.document.contents, name)

    def search(self,text,topn=3):
        return self.emb_database.search(text,topn)


# ------------------------------ DataBase load ---------------------------------------#
def load_database(dir_path=os.path.join("..","database_dir")):
    dirs = [name for name in os.listdir(dir_path) if os.path.isdir(f"{dir_path}/{name}")]

    for dir in dirs:
        database = Porject_DataBase(os.path.join(f"{dir_path}",f"{dir}"),dir)
        database_list.append(database)
        database_namelist.append(dir)

    return database_list,database_namelist