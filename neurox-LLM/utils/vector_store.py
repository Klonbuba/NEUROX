import json
import os
import numpy as np
import ollama

MEMORY_FILE = "memory.json"

class VectorStore:
    def __init__(self, model_name="phi3"):
        self.model_name = model_name
        self.memories = []
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    self.memories = json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                self.memories = []

    def _save_memory(self):
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def get_embedding(self, text):
        try:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            return response['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None

    def add_memory(self, text, metadata=None):
        embedding = self.get_embedding(text)
        if embedding:
            memory_item = {
                "text": text,
                "embedding": embedding,
                "metadata": metadata or {},
                "timestamp": str(np.datetime64('now'))
            }
            self.memories.append(memory_item)
            self._save_memory()
            print(f"Memory saved: {text[:50]}...")

    def search_memory(self, query, top_k=3, threshold=0.5):
        query_embedding = self.get_embedding(query)
        if not query_embedding or not self.memories:
            return []

        query_vec = np.array(query_embedding)
        results = []

        for mem in self.memories:
            mem_vec = np.array(mem['embedding'])
            
            # Cosine Similarity
            dot_product = np.dot(query_vec, mem_vec)
            norm_q = np.linalg.norm(query_vec)
            norm_m = np.linalg.norm(mem_vec)
            
            similarity = dot_product / (norm_q * norm_m) if norm_q * norm_m > 0 else 0
            
            if similarity >= threshold:
                results.append((similarity, mem))

        # Sort by similarity desc
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [res[1]['text'] for res in results[:top_k]]
