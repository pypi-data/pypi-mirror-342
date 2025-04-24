'''
We want to choose negatives from a dataset with only positives (for example, thumb-up from RAG systems)

Input: pairs of (sentence, positive_sentence) or df with two columns ['sentence', 'positive_sentence'], 
method='random' or 'hard_negative', n_negatives, sentence_transformer_model, 

Output: Triplet dataset with output file path or triplets
'''
import random
import pandas as pd

def build_random_triplets(
    df: pd.DataFrame,
    n_negatives: int,
    triplet_output_path: str
):
    """
    For each (sentence, positive_sentence) pair in df, choose n_negatives random
    negative examples (that are not the positive_sentence itself) from other rows.

    Returns a DataFrame of triplets with columns: sentence, positive, negative.
    Saves the result to triplet_output_path.
    """
    
    all_positive_sentences = df['positive_sentence'].tolist()
    triplets = []

    for idx, row in df.iterrows():
        anchor = row['sentence']
        positive = row['positive_sentence']

        # Exclude the current positive from the negative pool
        negative_candidates = [sent for sent in all_positive_sentences if sent != positive]

        # Handle the case where there are fewer candidates than n_negatives
        if len(negative_candidates) < n_negatives:
            negatives = random.choices(negative_candidates, k=n_negatives)
        else:
            negatives = random.sample(negative_candidates, n_negatives)

        for negative in negatives:
            triplets.append({
                "sentence": anchor,
                "positive_sentence": positive,
                "negative_sentence": negative
            })

    triplet_df = pd.DataFrame(triplets)
    triplet_df.to_csv(triplet_output_path, index=False)
    print("Triplets are saved successfully!")