import torch
import torch.nn.functional as F
import numpy as np


def get_normalized_token_embeddings(text:str, tokenizer, model, device) -> torch.Tensor:
    tokens = tokenizer(text, return_tensors='pt', padding=True, truncation=True).to(device)
    outputs = model(**tokens)
    token_embeddings = outputs.last_hidden_state.squeeze(0)  # Shape: [num_tokens, 768]

    # Normalize embeddings for cosine similarity
    normalized_embeddings = F.normalize(token_embeddings, p=2, dim=1)  # L2 normalize along the token dimension
    return normalized_embeddings


def compute_max_similarity(query_embeddings:torch.Tensor, doc_embeddings:torch.Tensor) -> torch.Tensor:
    # Compute cosine similarity between all query tokens and document tokens
    similarity_matrix = torch.matmul(query_embeddings, doc_embeddings.T)  # Shape: [num_query_tokens, num_doc_tokens]

    # Take the maximum similarity for each query token across all document tokens
    max_similarities = torch.max(similarity_matrix, dim=1)[0]  # Shape: [num_query_tokens]

    # Sum the maximum similarities to get a single score for the document
    score = torch.sum(max_similarities)
    return score