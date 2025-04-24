import numpy as np
import pandas as pd

"""
This is a class for IR evaluation
A standard dataset for IR has 3 components:
docs with doc_id and text for us to query from
queries with query_id and text
qrels with query_id, doc_id and their relevant score

To compute IR metrics, we just need two parameters:
df_qrels
k: to compute IR metrics at k, for example, NDCG@k or recall@k
"""
class IREvaluation:
    def __init__(self):
        pass

    # Metric calculations
    def precision_at_k(self, actual, predicted, k):
        relevant_in_predicted = [doc for doc in predicted[:k] if doc in actual]
        return len(relevant_in_predicted) / k

    def recall_at_k(self, actual, predicted, k):
        relevant_in_predicted = [doc for doc in predicted[:k] if doc in actual]
        return len(relevant_in_predicted) / len(actual) if len(actual) > 0 else 0

    def dcg_at_k(self, relevance_scores, k):
        dcg = 0.0
        for i in range(min(len(relevance_scores), k)):
            dcg += (relevance_scores[i] / np.log2(i + 2))
        return dcg

    def ndcg_at_k(self, actual_relevance, predicted, k):
        predicted_relevance_scores = [actual_relevance.get(doc_id, 0) for doc_id in predicted[:k]]
        ideal_relevance_scores = sorted(actual_relevance.values(), reverse=True)
        ideal_relevance_scores = ideal_relevance_scores[:k] + [0] * (k - len(ideal_relevance_scores))

        dcg = self.dcg_at_k(predicted_relevance_scores, k)
        idcg = self.dcg_at_k(ideal_relevance_scores, k)
        return dcg / idcg if idcg > 0 else 0.0

    """
    To compute metrics, we need df_results, a data frame of search results of this information:
    query_id
    doc_id
    rank: this is the rank of the doc for a given query returned by the retrieval system
    """
    def compute_evaluation_metrics(self, df_qrels, df_results, k=20):
        evaluation_results = []

        for query_id, group in df_results.groupby('query_id'):
            actual_relevance = df_qrels[df_qrels['query_id'] == query_id].set_index('doc_id')['relevance'].to_dict()
            actual_relevance = {doc_id: relevance for doc_id, relevance in actual_relevance.items() if relevance >= 1}

            predicted_docs = group.sort_values(by='rank')['doc_id'].tolist()
            actual_docs = list(actual_relevance.keys())

            recall = self.recall_at_k(actual_docs, predicted_docs, k)
            ndcg = self.ndcg_at_k(actual_relevance, predicted_docs, k)

            evaluation_results.append({'query_id': query_id, 'ndcg': ndcg, 'recall': recall})

        df_evaluation = pd.DataFrame(evaluation_results)
        average_ndcg = df_evaluation['ndcg'].mean()
        average_recall = df_evaluation['recall'].mean()

        print(f"Average Recall@{k}: {average_recall}")
        print(f"Average NDCG@{k}: {average_ndcg}")
