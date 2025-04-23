import faiss
import numpy as np
import json

class VectorDatabase:
    def __init__(self, dimension=512):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance
        self.product_ids = []

    def add_product(self, embedding, product_id):
        embedding = np.array(embedding).astype('float32').reshape(1, -1)
        assert embedding.shape[1] == self.dimension, "Embedding dimension mismatch."
        self.index.add(embedding)
        self.product_ids.append(product_id)

    def search(self, query_embedding, k=5):
        query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)
        k = min(k, self.index.ntotal)
        if k == 0:
            return []
        distances, indices = self.index.search(query_embedding, k)
        return [(self.product_ids[i], float(dist)) for i, dist in zip(indices[0], distances[0]) if i != -1]
    
    def save(self, index_path="vector.index", ids_path="product_ids.json"):
        faiss.write_index(self.index, index_path)
        with open(ids_path, "w") as f:
            json.dump(self.product_ids, f)

    def load(self, index_path="vector.index", ids_path="product_ids.json"):
        self.index = faiss.read_index(index_path)
        with open(ids_path, "r") as f:
            self.product_ids = json.load(f)
