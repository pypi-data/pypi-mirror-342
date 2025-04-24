# Embedding class with SentenceTransformer

from sentence_transformers import SentenceTransformer
import torch
import numpy as np

class SBERTEmbedding:
    def __init__(self, model_name_or_path:str, device:str='cuda'):
        self.model = SentenceTransformer(model_name_or_path)
        print(self.model)
        self.device = device
        self.model = self.model.to(self.device)
    
    def normalize_embeddings(self, embeddings:torch.Tensor) -> torch.Tensor:
        norms = torch.norm(embeddings, p=2, dim=1, keepdim=True)
        normalized_embeddings = embeddings / norms
        return normalized_embeddings

    def encode(self, texts:list[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, convert_to_tensor=True)
        if embeddings.dim() == 1:
            # Single embedding, convert to 2D by adding an extra dimension (for consistency)
            embeddings = embeddings.unsqueeze(0)
        # Return torch tensor of shape len(texts) x 768
        return self.normalize_embeddings(embeddings).cpu().numpy()