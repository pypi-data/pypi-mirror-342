import pandas as pd
from colbert_kit.embedding.sbert_embedding import SBERTEmbedding
from colbert_kit.indexing.faiss.HNSW_faiss_index import HNSWFaissIndex
from colbert_kit.retrieving.faiss_search import FaissSearch

def build_hard_triplets(
    df:pd.DataFrame,
    model_name_or_path:str,
    start_index:int,
    n_negatives:int,
    triplet_output_path:str,
    index_name:str,
    index_output_path:str='./indices/',
    use_gpu:bool=False, 

):
    """
    
    Build hard triplets (anchor, positive, hard negative) for training or evaluating 
    retrieval/ranking models using Sentence-BERT and FAISS.

    This function takes a DataFrame with sentence pairs and uses a sentence embedding model 
    to encode all positive sentences. A FAISS index is built to enable fast retrieval of 
    semantically similar sentences (hard negatives). For each anchor sentence, it retrieves 
    the top-k nearest neighbors, excludes the current sample and selects hard negatives 
    from the remaining ones. These are then saved as (query, positive, negative) triplets.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with columns 'sentence' and 'positive_sentence'.
    
    model_name_or_path : str
        Path or model name for a Sentence-BERT model to be used for encoding.
    
    start_index : int
        Index from which to start selecting hard negatives among the top retrieved results.
        This avoids selecting extremely similar (or duplicate) sentences.
    
    n_negatives : int
        Number of hard negatives to retrieve per anchor sentence.
    
    triplet_output_path : str
        File path to save the generated triplets as a CSV.
    
    index_name : str
        Name to use when creating/saving the FAISS index.
    
    index_output_path : str, optional
        Directory where the FAISS index will be saved or loaded from. Default is './indices/'.
    
    use_gpu : bool, optional
        Whether to use GPU acceleration for Sentence-BERT encoding and FAISS. Default is False.

    Returns
    -------
    None
        The function saves a CSV file with columns: 'sentence', 'positive_sentence', 'negative_sentence'.

    """
    df['index'] = df.index
    # Create a text list from overview column
    # This will be used for retrieval
    positive_sentences = df['positive_sentence'].tolist()

    device = 'cuda' if use_gpu else 'cpu'
    
    model = SBERTEmbedding(
        model_name_or_path=model_name_or_path,
        device=device
    )
    embeddings = model.encode(positive_sentences)

    # Now, we need to create FAISS index to search for nearest tokens
    dimension = embeddings.shape[1]

    faiss_index = HNSWFaissIndex(
        index_name=index_name,
        dimension=dimension,
        use_gpu=use_gpu,
        index_output_path=index_output_path
    )

    faiss_index.create_index(embeddings=embeddings)

    # Load FAISS index and retrieve
    faiss_search = FaissSearch(
        index_name=index_name,
        index_type='HNSW',
        use_gpu=use_gpu,
        index_path=index_output_path
    )

    faiss_search.load_index()

    triplets = []

    for i, row in df.iterrows():
        query = row['sentence']
        positive = row['positive_sentence']
        query_embedding = model.encode(query)

        _, faiss_indices = faiss_search.faiss_search_results(query_embedding, top_k=start_index+n_negatives+1)
        negatives = []
        for idx in list(map(int, faiss_indices[0]))[start_index:]:
            if idx != i and len(negatives) < n_negatives:
                negatives.append(df.iloc[idx]['positive_sentence'])

        for negative in negatives:
            triplets.append({
                "sentence": query,
                "positive_sentence": positive,
                "negative_sentence": negative
            })
    
    # Save triplets
    triplet_df = pd.DataFrame(triplets)
    triplet_df.to_csv(triplet_output_path, index=False)
    print("Triplets are saved successfully!")
        

    