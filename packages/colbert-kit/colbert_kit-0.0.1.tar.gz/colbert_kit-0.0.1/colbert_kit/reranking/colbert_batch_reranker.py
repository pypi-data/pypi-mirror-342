from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class colBERTReRankerBatch:
    def __init__(self, model_name_or_path:str, device:str="cuda"):
        self.device = device
        self.model = AutoModel.from_pretrained(model_name_or_path).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

    def normalize_embeddings(self, embeddings:torch.Tensor) -> torch.Tensor:
        norms = torch.norm(embeddings, p=2, dim=2, keepdim=True)
        normalized_embeddings = embeddings / norms
        return normalized_embeddings
    
    def get_token_embeddings(self, texts: list[str]) -> torch.Tensor:
        tokens = self.tokenizer(texts, return_tensors='pt', padding='max_length', truncation=True, max_length=250).to(self.device)

        with torch.no_grad():
            outputs = self.model(**tokens)
        token_embeddings = outputs.last_hidden_state  # Shape: [batch_size, token_length, embedding_dim]
        return self.normalize_embeddings(token_embeddings), tokens['input_ids'].size(1)
    
    def compute_max_similarity(self, query_embeddings:torch.Tensor, doc_embeddings:torch.Tensor) -> torch.Tensor:
        # query_embeddings is of shape [1, query_token_length, embedding_dim]
        # doc_embeddings is of shape batch_size x token_length x embedding_dim
        # doc_embeddings.permute(0, 2, 1) is of shape batch_size x embedding_dim x token_length
        # Similarity matrix of shape batch_size x query_token_length x doc_token_length
        similarity_matrix = torch.matmul(query_embeddings, doc_embeddings.permute(0, 2, 1))
        
        # Take the max similarity along the doc_token dimension
        # Shape: [batch_size, query_token_length]
        max_similarities, _ = torch.max(similarity_matrix, dim=2) 
         
        # We now sum along the query_token dimension
        # Shape: [batch_size]
        scores = torch.sum(max_similarities, dim=1)  

        return scores

    def reranker(self, query:str, doc_candidates:list[str], candidate_idx:list[str], batch_size:int=1, top_n:int=5):
        # Get query embeddings
        # query_embeddings is of shape [1, query_token_length, embedding_dim]
        query_embeddings, token_length = self.get_token_embeddings([query])

        # Process documents in batches
        scores = []
        for i in range(0, len(doc_candidates), batch_size):
            batch_docs = doc_candidates[i:i + batch_size]
            doc_embeddings, _ = self.get_token_embeddings(batch_docs)
            batch_scores = self.compute_max_similarity(query_embeddings, doc_embeddings) / token_length
            scores.extend(batch_score for batch_score in batch_scores.tolist())

        # Pair scores with indices and sort
        score_idx_pairs = list(zip(scores, candidate_idx))
        sorted_scores_with_idx = sorted(score_idx_pairs, key=lambda x: x[0], reverse=True)

        # Select top_n
        sorted_scores = [score for score, _ in sorted_scores_with_idx[:top_n]]
        sorted_indices = [idx for _, idx in sorted_scores_with_idx[:top_n]]

        return sorted_scores, sorted_indices
