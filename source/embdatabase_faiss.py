# -*- coding: utf-8 -*-
import os
import pickle

import faiss
from pypinyin import lazy_pinyin
from document_emb import *


# covert name to pinyin for Milvus can't use Chinese Character
def cover_name(name):
    return "_".join(lazy_pinyin(name))

# emb database(faiss & local)
class EmbDataBase_Faiss():
    def __init__(self, emb_model_dir, contents, name, recreate_database=False):
        global milvs_client
        self.emb_model = EmbModel(emb_model_dir)
        # self.name = cover_name(name)

        if (recreate_database) or (os.path.exists(os.path.join("..",".cache",f"{name}_faiss_index.pkl")) == False):
            if os.path.exists(os.path.join("..",".cache",f"{name}_faiss_index.pkl")) :
                os.remove(os.path.join("..",".cache",f"{name}_faiss_index.pkl"))

            index = faiss.IndexFlatL2(self.emb_model.model.get_sentence_embedding_dimension())
            embs = self.emb_model.to_emb(contents)
            index.add(embs)

            with open(os.path.join("..",".cache",f"{name}_faiss_index.pkl"),"wb") as f:
                pickle.dump(index,f)

        else: # (recreate_database==false) and (os.path.exists(os.path.join("..",".cache",f"{name}_faiss_index.pkl")) == True):
            with open(os.path.join("..",".cache",f"{name}_faiss_index.pkl"),"rb") as f:
                index = pickle.load(f)

        self.index = index
        self.contents = contents

    # def add(self,emb):
    #     self.index.add(emb)

    def search(self,content,topn=3):
        if isinstance(content,str):
            content = self.emb_model.to_emb(content)

        dis,idx = self.index.search(content,topn)   #milvus
        results = [self.contents[i] for i in idx[0]]

        return results


