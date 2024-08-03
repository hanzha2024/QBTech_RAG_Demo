# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
import pickle
import os

# document processing
class Document():
    def __init__(self,dir,name):
        loader = DirectoryLoader(dir,show_progress=True)
        documents = loader.load()

        # contents persistence
        if os.path.exists(os.path.join("..",".cache",f"{name}_contents.pkl")) == False:
            text_spliter = CharacterTextSplitter(chunk_size=300,chunk_overlap=50)

            split_docs = text_spliter.split_documents(documents)
            contents = [i.page_content for i in split_docs]

            with open(os.path.join("..",".cache",f"{name}_contents.pkl"),"wb") as f:
                pickle.dump(contents,f)

        else:
            with open(os.path.join("..",".cache",f"{name}_contents.pkl"),"rb") as f:
                contents = pickle.load(f)
        self.contents = contents

# to emb
class EmbModel():
    def __init__(self,emb_model_dir):
        self.model = SentenceTransformer(emb_model_dir)

    def to_emb(self,sentence):
        if isinstance(sentence,str):
            sentence = [sentence]
        return self.model.encode(sentence)







