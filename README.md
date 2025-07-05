OpenMP PR Summarizer
A Python-based, offline, GenAI-powered tool that generates structured summaries for GitHub pull requests related to OpenMP in the LLVM/Clang ecosystem.
The tool uses:

Ollama (offline LLM) for natural language generation,
FAISS (vector database) for semantic search in the OpenMP specification,
And integrates with the GitHub API to fetch PR diffs and context.
This enables reviewers and researchers to quickly understand the impact and OpenMP-spec relevance of code changes, even without internet access or cloud LLMs.