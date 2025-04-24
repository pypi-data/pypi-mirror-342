from transformers import AutoTokenizer, AutoModel
import torch
import json
import numpy as np
from colbert_kit.retrieving.faiss_search import FaissSearch
from collections import defaultdict
from typing import List, Tuple

"""
There are three steps for retrieving with colBERT
Phase 1: for each token in the query, search for nearest tokens
Phase 2: map tokens back to their original documents
Phase 3: compute maxsim score between query and documents

Here are parameters for the __init__ function
model_name_or_path: we need to load the model in order to compute maxim scores
index_path, index_name, index_type: those to load and search with FAISS index
token_to_doc_map name and path: place where we save mapping from tokens to docs
doc_dict name and path: place where we save index of the form {'index': text}
"""

class colBERTSearchFaiss:
    def __init__(self,
                 model_name_or_path:str,
                 index_path:str,
                 index_name:str,
                 index_type:str,
                 use_gpu:bool=False,
                 token_to_doc_map_name:str="token_to_doc_map.npy",
                 doc_dict_name:str="documents.json", 
                 token_to_doc_map_path:str='./indices/',
                 doc_dict_path:str='./indices/',
                 device:str="cuda"
    ):
        
        self.token_to_doc_map_path = token_to_doc_map_path + token_to_doc_map_name
        self.doc_dict_path = doc_dict_path + doc_dict_name
        self.device = device
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        print("Loading model...")
        self.model = AutoModel.from_pretrained(model_name_or_path).to(self.device)
        self.use_gpu = use_gpu

        self.faiss_search = FaissSearch(index_name=index_name, 
                                        index_type=index_type, 
                                        use_gpu=self.use_gpu, 
                                        index_path=index_path
                            )

    def load_index_map_and_dict(self):
        # Load the index
        print("Loading index...")
        self.faiss_search.load_index()
        # Load the token_to_doc_map
        with open(self.token_to_doc_map_path, 'rb') as file:
            self.token_to_doc_map = np.load(file)
        print('Token to doc map loaded sucessfully')

        # Load the doc dict
        with open(self.doc_dict_path, 'r') as file:
            self.documents_dict = json.load(file)
        print("Documents dictionary loaded sucessfully")
    
    def normalize_embeddings(self, embeddings:torch.Tensor) -> torch.Tensor:
        norms = torch.norm(embeddings, p=2, dim=1, keepdim=True)
        normalized_embeddings = embeddings / norms
        return normalized_embeddings

    def get_token_embeddings(self, text:str) -> Tuple[np.ndarray, int]:
        tokens = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True).to(self.device)
        tokens_length = tokens['input_ids'][0].shape[0]
        with torch.no_grad():
            outputs = self.model(**tokens)
        token_embeddings = outputs.last_hidden_state.squeeze(0)
        return self.normalize_embeddings(token_embeddings).cpu().numpy(), tokens_length
    
    def compute_max_similarity(self, query_embeddings:torch.Tensor, doc_embeddings:torch.Tensor) -> torch.Tensor:
        # Compute cosine similarity between all query tokens and document tokens
        similarity_matrix = torch.matmul(query_embeddings, doc_embeddings.T)  # Shape: [num_query_tokens, num_doc_tokens]

        # Take the maximum similarity for each query token across all document tokens
        max_similarities = torch.max(similarity_matrix, dim=1)[0]  # Shape: [num_query_tokens]

        # Sum the maximum similarities to get a single score for the document
        score = torch.sum(max_similarities)
        return score

    def colbert_search_results(self, query:str, top_k_results:int=5, top_k_search_tokens:int=100) -> Tuple[List[float], List[int]]:
        query_embeddings, query_tokens_len = self.get_token_embeddings(query)

        # Query FAISS and retrieve relevant tokens
        D, I = self.faiss_search.faiss_search_results(query_embeddings, top_k_search_tokens)

        # Map back to documents and compute MaxSim
        
        doc_scores = defaultdict(float)

        for query_idx, neighbors in enumerate(I):
            max_scores_per_doc = defaultdict(float)

            for neighbor_pos, neighbor_idx in enumerate(neighbors):
                doc_id = self.token_to_doc_map[neighbor_idx]
                score = D[query_idx][neighbor_pos]
                max_scores_per_doc[doc_id] = max(max_scores_per_doc[doc_id], score)

            for doc_id, max_score in max_scores_per_doc.items():
                doc_scores[doc_id] += max_score

        ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
        doc_ids = []
        scores = []
        for doc_id, score in ranked_docs[:top_k_results]:
            doc_ids.append(doc_id)
            scores.append(score/query_tokens_len)
        return scores, doc_ids 