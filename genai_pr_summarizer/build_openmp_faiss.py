import os
import re
import pickle
import faiss
import requests
import numpy as np
from pdfminer.high_level import extract_text

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
PDF = "OpenMP-API-Specification-6-0.pdf"
FAISS_INDEX = "openmp_spec.index"
SECTIONS_PKL = "openmp_sections.pkl"

def split_sections(text):
    section_pattern = re.compile(r'^Section\s+\d+(\.\d+)*\s+.*$', re.MULTILINE)
    starts = [m.start() for m in section_pattern.finditer(text)]
    starts.append(len(text))
    sections = []
    for i in range(len(starts)-1):
        sect = text[starts[i]:starts[i+1]].strip()
        if sect:
            sections.append(sect)
    return sections

def get_embedding_ollama(text):
    resp = requests.post(OLLAMA_EMBED_URL, json={"model":"llama3", "prompt": text[:1024]})
    resp.raise_for_status()
    emb = resp.json().get("embedding")
    return emb

if __name__ == "__main__":
    if not os.path.exists(PDF):
        print("PDF not found!")
        exit(1)
    print("Extracting text...")
    text = extract_text(PDF)
    print("Splitting sections...")
    sections = split_sections(text)
    print(f"Found {len(sections)} sections.")
    section_vectors = []
    for i, sect in enumerate(sections):
        print(f"Embedding section {i+1}/{len(sections)}...")
        vec = get_embedding_ollama(sect[:1024])
        section_vectors.append(vec)
    print("Building FAISS index...")
    dim = len(section_vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(section_vectors).astype('float32'))
    faiss.write_index(index, FAISS_INDEX)
    with open(SECTIONS_PKL, "wb") as f:
        pickle.dump(sections, f)
    print("Done. Saved openmp_spec.index and openmp_sections.pkl")