# colbert-kit (version 0.0.1)

**colbert-kit** is a Python package designed for building, training, and evaluating ColBERT-style retrieval models. It supports GPU-accelerated re-ranking, indexing, and training workflows for information retrieval tasks.

---

## Features

- **Indexing and retrieving**: Efficient document indexing and retrieving using FAISS.
- **Batch Re-ranking**: Accelerated re-ranking with batching on GPU.
- **Training Support**: Train from scratch or from checkpoints with a flexible training script.
- **Evaluation**: Compute core IR metrics such as **Recall** and **NDCG** for both **ColBERT** and **BM25**.
- **Negative Sampling Utilities**:
  - **Random Negatives**: Given a DataFrame with columns `sentence` and `positive_sentence`, randomly sample negatives from the dataset.
  - **Hard Negatives**: Use a sentence-transformer model to retrieve semantically similar (but incorrect) negatives.

More detail about usage can be found in our [documentation](https://github.com/thuongtuandang/colbert-kit/tree/main/documentation) and [Git repository](https://github.com/thuongtuandang/colbert-kit).
 
---

## Installation

To install the package, you have three options depending on your FAISS and CUDA setup. The key difference between the options lies in whether you want to use FAISS on CPU or GPU, and which CUDA version your system supports.

If you are **not using CUDA 11.x or 12.x**, or if you do **not need GPU acceleration** for indexing and searching, install the CPU version:
```bash
pip install colbert-kit[cpu]
```
If you are using **CUDA 11.x** and want to enable FAISS GPU support:
```bash
pip install colbert-kit[gpu-cu11]
```
If you are using **CUDA 12.x**, install the version built for CUDA 12:
```bash
pip install colbert-kit[gpu-cu12]
```
**Note:** HNSW indexing is not supported on GPU in FAISS in those versions. GPU acceleration works well for Flat and IVF-based indexes.

## Quick start
```bash
    from colbert_kit.reranking.colbert_batch_reranker import colBERTReRankerBatch 
    embedding_model_name = "thuongtuandang/german-colbert" 
    batchreranker = colBERTReRankerBatch(model_name_or_path=embedding_model_name, device='cpu') 
    query = "Was ist die Hauptstadt von Frankreich?" 
    doc_candidates = [
    "Paris ist die Hauptstadt von Frankreich.", 
    "Berlin ist die Hauptstadt von Deutschland.", 
    "Frankreich hat viele schöne Städte." 
    ] 
    candidate_idx = list(range(len(doc_candidates))) 
    top_scores, top_indices = batchreranker.reranker(query, doc_candidates, candidate_idx, batch_size=1, top_n=2 ) 
    print("Top Scores:", top_scores) print("Top Indices:", top_indices) 
    for idx in top_indices: 
        print(doc_candidates[idx])
```

<pre> <details> 
<summary><strong>Example Output</strong></summary> 
```text Top Scores: [0.9633049368858337, 0.9230972528457642] Top Indices: [0, 2] Paris ist die Hauptstadt von Frankreich. Frankreich hat viele schöne Städte. ```
 </details> </pre>