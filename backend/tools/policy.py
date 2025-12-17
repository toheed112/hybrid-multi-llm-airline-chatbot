# policy.py - RAG for company policies using OpenAI embeddings + FAISS
from dotenv import load_dotenv
import os, numpy as np, faiss, requests, re
load_dotenv()
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fetch FAQ
response = requests.get("https://storage.googleapis.com/benchmarks-artifacts/travel-db/swiss_faq.md")
faq_text = response.text
docs = [{"page_content": txt.strip()} for txt in re.split(r"(?=\n##)", faq_text) if txt.strip()]

class VectorStoreRetriever:
    def __init__(self, docs, vectors, oai_client):
        self._docs = docs
        self._arr = vectors
        self._client = oai_client
        self.dimension = vectors.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(vectors)

    @classmethod
    def from_docs(cls, docs, oai_client):
        embeddings = oai_client.embeddings.create(
            model="text-embedding-3-small", input=[doc["page_content"] for doc in docs]
        )
        vectors = np.array([emb.embedding for emb in embeddings.data])
        return cls(docs, vectors, oai_client)

    def query(self, query, k=5):
        embed = self._client.embeddings.create(model="text-embedding-3-small", input=[query])
        query_emb = np.array([embed.data[0].embedding])
        _, indices = self.index.search(query_emb, k)
        scores = np.dot(query_emb, self._arr.T)[0]
        return [{"page_content": self._docs[i]["page_content"], "similarity": scores[i]} for i in indices[0]]

retriever = VectorStoreRetriever.from_docs(docs, client)

def lookup_policy(query):
    """Lookup company policies via embeddings."""
    retrieved_docs = retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in retrieved_docs])