import faiss
from .base_faiss_index import BaseFaissIndex
import numpy as np

class HNSWFaissIndex(BaseFaissIndex):
    # M is the degree of each node in the HNSW graph
    def __init__(self, index_name:str, dimension:int, use_gpu:bool=False, M:int=32, index_output_path:str='./indices/'):
        super().__init__(index_name, dimension, use_gpu, index_output_path)
        self.M = M

    def create_index(self, embeddings:np.ndarray):
        print('Creating HNSW index...')
        self.index = faiss.IndexHNSWFlat(self.dimension, self.M)
        self.move_to_gpu()
        self.index.add(embeddings)
        print('Index created!')
        self.move_to_cpu()
        self.save_index()