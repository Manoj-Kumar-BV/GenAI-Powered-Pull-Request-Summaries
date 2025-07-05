# GenAI PR Summarizer

A CLI tool to generate professional summaries for GitHub pull requests using LLMs and OpenMP spec context.

---

## Requirements

- **Python 3.8+** (if using the pip version)
- **Ollama LLM server** ([Download & Install Ollama](https://ollama.com/download))  
  You must have Ollama installed and running on your machine for this tool to generate AI summaries.
- **GitHub Personal Access Token** (for authenticated API access)

---

## Ollama Installation

### **1. Download Ollama**

- Go to: [https://ollama.com/download](https://ollama.com/download)
- Download and install for your platform (Windows, Mac, Linux).

### **2. Start the Ollama Server**

Open a new terminal and run:

```sh
ollama serve
```

> Make sure this terminal stays open while you use GenAI PR Summarizer.

### **3. (Optional) Pull the LLM Model**

If you have not already pulled a model (e.g. `llama3`):

```sh
ollama pull llama3
```

---

## Usage

### **Option 1: Python CLI (pip)**

1. Install the tool:
   ```sh
   pip install genai-pr-summarizer
   ```
2. Set up your `.env` file with your GitHub token.
3. Start Ollama (see above).
4. Run the CLI:
   ```sh
   genai-pr-summarizer
   ```

### **Option 2: Windows Standalone (.exe)**

1. Download and extract the `genai-pr-summarizer-win.zip`.
2. Set up your `.env` as above.
3. Start Ollama (`ollama serve`).
4. Open Command Prompt in the extracted folder.
5. Run:
   ```sh
   genai-pr-summarizer.exe
   ```

---

## Troubleshooting

- **Ollama not running:**  
  The CLI will check for Ollama. If not running, you'll see an error like:  
  `Error: Ollama server is not running at http://localhost:11434. Please start Ollama (see Requirements above).`

- **First-time model load:**  
  The first time a model is used, Ollama will download it. This may take several minutes.

- **No AI summaries:**  
  If Ollama is not running, or the required model is missing, the tool cannot generate summaries.

---

## Support

For issues, please open an issue in this repository.