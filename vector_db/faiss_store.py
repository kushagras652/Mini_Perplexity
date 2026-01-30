import faiss
import numpy as np
import pickle
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

DB_PATH='vector_db/faiss.index'
META_PATH='vector_db/meta.pkl'

embeddings=OpenAIEmbeddings(model='text-embedding-3-small')

class VectorDB:
    def __init__(self,dim=1536):
        self.dim=dim
        self.index=None
        self.meta=[]

        if Path(DB_PATH).exists():
            self.index=faiss.read_index(DB_PATH)
            self.meta=pickle.load(open(META_PATH,'rb'))
        else:
            self.index=faiss.IndexFlatL2(dim)

    def add_documents(self,texts,metadata):
        vectors=embeddings.embed_documents(texts)
        vecs=np.array(vectors).astype('float32')

        self.index.add(vecs)
        self.meta.extend(metadata)

        faiss.write_index(self.index,DB_PATH)
        pickle.dump(self.meta,open(META_PATH
                                   ,'wb'))
        

    def search(self,query,k=5):
        q_vec=embeddings.embed_query(query)
        q_vec=np.array([q_vec]).astype('float32')


        D,I=self.index.search(q_vec,k)
        return [self.meta[i] for i in I[0]]
    

    def add(self, text, meta):
        vec = embeddings.embed_documents([text])
        self.index.add(np.array(vec).astype("float32"))
        self.meta.append(meta)
        faiss.write_index(self.index, DB_PATH)
        pickle.dump(self.meta, open(META_PATH, "wb"))