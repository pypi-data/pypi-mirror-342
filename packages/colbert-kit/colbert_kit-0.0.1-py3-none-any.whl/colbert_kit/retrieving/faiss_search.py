import faiss
import numpy as np
from typing import Tuple

class FaissSearch:
    def __init__(self, index_name:str, index_type:str, use_gpu:bool=False, index_path:str='./indices/'):
        """
        Initialize FaissSearch for loading and querying a FAISS index.
        index_name: The name of the saved FAISS index file.
        use_gpu: Boolean indicating whether to use GPU for searching.
        index_type: either flat, or HNSW or IVF
        """
        self.index_name = index_name
        self.use_gpu = use_gpu
        self.index = None
        self.index_type = index_type
        self.index_path = index_path

    def load_index(self):
        """
        Load the FAISS index from file.
        :return: None
        """
        print(f"Loading index from {self.index_path + self.index_name}...")
        self.index = faiss.read_index(self.index_path + self.index_name)
        
        # Move to GPU for search
        if self.use_gpu:
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)
        
        print(f"Index loaded successfully!")

    # Search with flat index
    def _FlatSearch(self, query_embedding:np.ndarray, top_k:int=5) -> Tuple[np.ndarray, np.ndarray]:
        distances, indices = self.index.search(query_embedding, top_k)
        return distances, indices

    # Search with flat index
    def _HNSWSearch(self, query_embedding:np.ndarray, top_k:int=5) -> Tuple[np.ndarray, np.ndarray]:
        distances, indices = self.index.search(query_embedding, top_k)
        return distances, indices

    def _IVFSearch(self, query_embedding:np.ndarray, nprobes:int, top_k:int=5) -> Tuple[np.ndarray, np.ndarray]:
        # Set the number of clusters to search
        self.index.nprobe = nprobes 
        distances, indices = self.index.search(query_embedding, top_k)
        return distances, indices
    
    def faiss_search_results(self, query_embedding, top_k, nprobes=5) -> Tuple[np.ndarray, np.ndarray]:
        if self.index_type == 'flat':
            return self._FlatSearch(query_embedding, top_k)
        if self.index_type == 'HNSW':
            return self._HNSWSearch(query_embedding, top_k)
        if self.index_type == 'IVF':
            self.nprobes = nprobes
            return self._IVFSearch(query_embedding, self.nprobes, top_k)