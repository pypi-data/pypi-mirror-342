from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import json
from tqdm import tqdm

class colBERTEmbedding:
    def __init__(self, 
                 model_name_or_path:str, 
                 token_to_doc_map_name:str='token_to_doc_map.npy',
                 doc_dict_name:str='documents.json', 
                 token_to_doc_map_path:str='./indices/',
                 doc_dict_path:str='./indices/',
                 device:str="cuda"
                 ):
        self.model = AutoModel.from_pretrained(model_name_or_path).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.token_to_doc_map_path = token_to_doc_map_path + token_to_doc_map_name
        self.doc_dict_path = doc_dict_path + doc_dict_name
        self.device = device
    
    def normalize_embeddings(self, embeddings:torch.Tensor) -> torch.Tensor:
        norms = torch.norm(embeddings, p=2, dim=1, keepdim=True)
        normalized_embeddings = embeddings / norms
        return normalized_embeddings
    
    def get_token_embeddings(self, text:str) -> torch.Tensor:
        tokens = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**tokens)
        token_embeddings = outputs.last_hidden_state.squeeze(0)
        return self.normalize_embeddings(token_embeddings)
    
    def encode(self, texts: list[str]) -> np.ndarray:
        self.model.eval()
        # doc_embeddings is a dict, to save token_embedding with corresponding doc_id
        doc_embeddings = {}

        documents_dict = {}
        for idx, text in enumerate(texts):
            documents_dict[idx] = text

        for doc_id, text in tqdm(documents_dict.items(), total=len(documents_dict), desc="colBERT embedding is in progress"):
            doc_embeddings[doc_id] = self.get_token_embeddings(text)

        # token_to_doc_map is to map a token back to the corresponding document
        token_to_doc_map = []
        token_embeddings_list = []

        for doc_id, token_embeddings in doc_embeddings.items():
            for token_embedding in token_embeddings:
                token_to_doc_map.append(doc_id)
                token_embeddings_list.append(token_embedding)

        token_embeddings_tensor = torch.stack(token_embeddings_list)
        token_embeddings_np = token_embeddings_tensor.cpu().numpy()

        # Save the token_to_doc_map
        token_to_doc_map_np = np.array(token_to_doc_map)
        np.save(self.token_to_doc_map_path, token_to_doc_map_np)
        print("Token to doc map is saved to ", self.token_to_doc_map_path)

        # Save the document dict
        with open(self.doc_dict_path, 'w') as file:
            json.dump(documents_dict, file)
        print("Documents dictionary is saved to ", self.doc_dict_path)
        
        return token_embeddings_np