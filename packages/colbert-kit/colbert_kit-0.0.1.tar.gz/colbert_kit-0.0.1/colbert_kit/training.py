import pandas as pd
from tqdm import tqdm
from colbert_kit.utils import get_normalized_token_embeddings, compute_max_similarity
from colbert_kit.dataloader import TripletDataset
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import torch
import os
import time


class ColBERTTrainer:
    def __init__(self, 
                 model_name_or_path:str, 
                 triplets:list[(str, str, str)]=None, 
                 triplets_path:str=None, 
                 device:str='cpu', 
                 batch_size:int=256, 
                 lr:float=2e-5, 
                 num_epochs:int=2, 
                 checkpoint_dir:str='../models/checkpoints/', 
                 checkpoint_path:str=None):
        '''
        Input data could be in 2 formats:
            - triplets: list[(sentence, positive, negative)], or
            - triplets_path: csv file path with triplets, with EXACTLY these 3 columns ['sentence', 'positive_sentence', 'negative_sentence']
        '''
        self.device = device
        print(f"Using device: {self.device}")
        
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.checkpoint_dir = checkpoint_dir
        
        # Load triplets
        if triplets_path:
            self.triplets = self._load_triplets(triplets_path)
        elif triplets:
            self.triplets = triplets
        else:
            raise('Input data is missing. Use either csv file or triplets.')
        
        # Create dataset and dataloader
        self.dataset = TripletDataset(self.triplets)
        self.data_loader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModel.from_pretrained(model_name_or_path).to(self.device)
        
        # Initialize optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        
        # Load checkpoint if provided
        self.start_epoch = 0
        if checkpoint_path:
            self.start_epoch, self.last_loss = self.load_checkpoint(checkpoint_path)
            print(f"Resuming from epoch {self.start_epoch} with loss {self.last_loss}")
    
    def _load_triplets(self, triplets_path:str):
        df = pd.read_csv(triplets_path, sep='\t')
        triplets = [(entry['sentence'], entry['positive_sentence'], entry['negative_sentence']) for _, entry in tqdm(df.iterrows(), total=len(df))]
        return triplets
    
    def load_checkpoint(self, checkpoint_path:str):
        checkpoint = torch.load(checkpoint_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return checkpoint['epoch'], checkpoint['loss']
    
    def train(self):
        for epoch in range(self.start_epoch, self.start_epoch + self.num_epochs):
            total_loss = 0
            epoch_start_time = time.time()
            
            for batch in self.data_loader:
                queries, positive_docs, negative_docs = batch
                
                # Compute embeddings
                query_embeddings = [get_normalized_token_embeddings(query, self.tokenizer, self.model, self.device) for query in queries]
                positive_embeddings = [get_normalized_token_embeddings(positive_doc, self.tokenizer, self.model, self.device) for positive_doc in positive_docs]
                negative_embeddings = [get_normalized_token_embeddings(negative_doc, self.tokenizer, self.model, self.device) for negative_doc in negative_docs]
                
                # Compute similarity scores
                positive_scores = [compute_max_similarity(q_emb, p_emb) for q_emb, p_emb in zip(query_embeddings, positive_embeddings)]
                negative_scores = [compute_max_similarity(q_emb, n_emb) for q_emb, n_emb in zip(query_embeddings, negative_embeddings)]
                
                # Stack scores
                scores = torch.stack([torch.stack([pos, neg]) for pos, neg in zip(positive_scores, negative_scores)]).to(self.device)
                labels = torch.zeros(len(scores), dtype=torch.long).to(self.device)
                
                # Compute loss
                loss = F.cross_entropy(scores, labels)
                
                # Backpropagation
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
            
            epoch_end_time = time.time()
            print(f"Epoch {epoch+1}, Loss: {total_loss}")
            print(f"Training time per epoch: {epoch_end_time - epoch_start_time} seconds")
            
            # Save checkpoint
            self._save_checkpoint(epoch, total_loss)
    
    def _save_checkpoint(self, epoch, loss):
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        checkpoint = {
            'epoch': epoch + 1,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'loss': loss
        }
        checkpoint_path = os.path.join(self.checkpoint_dir, f'checkpoint_epoch_{epoch+1}.pth')
        torch.save(checkpoint, checkpoint_path)
        print(f'Checkpoint saved at {checkpoint_path}')
    
    def save_model(self, save_path:str):
        os.makedirs(save_path, exist_ok=True)
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)
        print(f'Model and tokenizer saved at {save_path}')