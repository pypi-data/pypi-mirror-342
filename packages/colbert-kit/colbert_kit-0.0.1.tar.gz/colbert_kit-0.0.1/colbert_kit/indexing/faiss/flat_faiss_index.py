import faiss
from .base_faiss_index import BaseFaissIndex
import numpy as np

class FlatFaissIndex(BaseFaissIndex):
    def __init__(self, index_name:str, dimension:str, use_gpu:bool=False, index_output_path:str='./indices/'):
        super().__init__(index_name, dimension, use_gpu, index_output_path)
        # self.index_output_path = index_output_path
        
    def create_index(self, embeddings:np.ndarray):
        print('Creating Flat index...')
        self.index = faiss.IndexFlatL2(self.dimension)
        self.move_to_gpu()
        self.index.add(embeddings)
        print('Index created!')
        self.move_to_cpu()
        self.save_index()