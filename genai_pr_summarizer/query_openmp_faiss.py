import sys, pickle, faiss, requests, numpy as np

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
FAISS_INDEX = "openmp_spec.index"
SECTIONS_PKL = "openmp_sections.pkl"

def get_embedding_ollama(text):
    resp = requests.post(OLLAMA_EMBED_URL, json={"model":"llama3", "prompt": text[:1024]})
    resp.raise_for_status()
    return resp.json().get("embedding")

def main():
    query = sys.argv[1]
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    index = faiss.read_index(FAISS_INDEX)
    with open(SECTIONS_PKL, "rb") as f:
        sections = pickle.load(f)
    vec = np.array([get_embedding_ollama(query)]).astype('float32')
    D, I = index.search(vec, k)
    for i in I[0]:
        print("----")
        print(sections[i].strip())
        print("----")

if __name__ == "__main__":
    main()