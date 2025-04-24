from torch.utils.data import Dataset

class TripletDataset(Dataset):
    def __init__(self, triplets:list[(str, str, str)]):
        self.triplets = triplets

    def __len__(self):
        return len(self.triplets)

    def __getitem__(self, idx):
        # Each item is a tuple (query, positive_doc, negative_doc)
        query, positive_doc, negative_doc = self.triplets[idx]
        return query, positive_doc, negative_doc