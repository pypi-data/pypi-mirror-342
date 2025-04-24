import faiss
from .base_faiss_index import BaseFaissIndex
import numpy as np

class IVFFaissIndex(BaseFaissIndex):
    def __init__(self, index_name:str, dimension:int, nlist:int=20, nprobes:int=10, use_gpu:bool=False, index_output_path:str='./indices/'):
        super().__init__(index_name, dimension, use_gpu, index_output_path)
        # nlist is the number of cluster
        self.nlist = nlist
        # nprobes is the number of clusters for search
        self.nprobes = nprobes

    def create_index(self, embeddings:np.ndarray):
        print('Creating IVF index...')
        quantizer = faiss.IndexFlatL2(self.dimension)
        self.index = faiss.IndexIVFFlat(quantizer, self.dimension, self.nlist)
        self.index.train(embeddings)
        self.move_to_gpu()
        self.index.add(embeddings)
        print('Index created!')
        self.move_to_cpu()
        self.save_index()