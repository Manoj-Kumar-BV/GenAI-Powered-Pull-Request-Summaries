# GenAI PR Summarizer

A CLI tool to generate professional summaries for GitHub pull requests using LLMs (via Ollama) and OpenMP spec context.

---

## Features

- **Summarizes each file in a PR** using a local LLM (Ollama, e.g., Llama3).
- **Automatically references relevant OpenMP specification context** for more accurate and professional summaries.
- **Exports summaries** as Markdown, plain text, or JSON.
- **Works offline** after LLM model is downloaded.
- **CLI tool** (pip install) and **Standalone Windows executable** available.
- **Supports image attachments** in summaries (see Exporting & Including Images).

---

## Requirements

- **Python 3.8+** (if using the pip version)
- **Ollama LLM server** ([Download & Install Ollama](https://ollama.com/download))  
  You must have Ollama installed and running on your machine for this tool to generate AI summaries.
- **Llama3 model** (or other supported models) pulled via `ollama pull llama3`
- **GitHub Personal Access Token** (for authenticated API access)
- **Windows:** For the `.exe`, no Python is needed. For source/pip: Python 3.8+

---

## Installation

### 1. From Source (Recommended for Contributors)

Clone this repo and install locally:

```sh
git clone https://github.com/Manoj-Kumar-BV/GenAI-Powered-Pull-Request-Summaries.git
cd GenAI-Powered-Pull-Request-Summaries
pip install .
```

### 2. Editable Mode (for development)

```sh
pip install -e .
```

### 3. From GitHub (without cloning)

```sh
pip install git+https://github.com/Manoj-Kumar-BV/GenAI-Powered-Pull-Request-Summaries.git
```

> **Note:**  
> `pip install genai-pr-summarizer` will **not work** unless the package is published on [PyPI](https://pypi.org/).
> If you want to install using that command, the maintainer must first publish the package to PyPI.

---

## Ollama Installation & Setup

### **1. Download Ollama**

- Go to: [https://ollama.com/download](https://ollama.com/download)
- Download and install for your platform (Windows, Mac, Linux).

### **2. Start the Ollama Server**

Open a new terminal and run:

```sh
ollama serve
```

> Make sure this terminal stays open while you use GenAI PR Summarizer.

### **3. Pull the LLM Model**

If you have not already pulled a model (e.g. `llama3`):

```sh
ollama pull llama3
```

---

## Usage

### **Option 1: Python CLI**

1. Install the tool (see Installation above).
2. Set up your `.env` file with your GitHub token (`cp .env.example .env` and edit).
3. Start Ollama (see above).
4. Run the CLI:
   ```sh
   genai-pr-summarizer
   ```

### **Option 2: Windows Standalone (.exe)**

1. Download and extract the `genai-pr-summarizer.zip` from [GitHub Releases](https://github.com/Manoj-Kumar-BV/GenAI-Powered-Pull-Request-Summaries/releases).
2. Copy `.env.example` to `.env` and add your GitHub token.
3. Start Ollama (`ollama serve`).
4. Open Command Prompt in the extracted folder.
5. Run:
   ```sh
   genai-pr-summarizer.exe
   ```

---

## Exporting and Including Images

- When exporting summaries, you can attach images by placing them in the `summaries/` folder (created on first export).
- Images will be referenced in the Markdown export using this format:
  ```
  ![image1](image1.png)
  ```
- Number images in reverse order of upload (last image is `image1.png`, second last is `image2.png`, etc.).

---

## How OpenMP Specification Context is Used

For each file changed in a pull request, the tool:
- Extracts the code diff (patch),
- Uses a semantic search (via a helper script and FAISS) over a pre-indexed OpenMP specification,
- Retrieves the most relevant OpenMP spec sections,
- Feeds both the diff and spec context to the LLM,
- The summary references the spec, making reviews more accurate.

---

## Troubleshooting

- **Ollama not running:**  
  The CLI will check for Ollama. If not running, you'll see an error like:  
  `Error: Ollama server is not running at http://localhost:11434. Please start Ollama (see Requirements above).`

- **First-time model load:**  
  The first time a model is used, Ollama will download it. This may take several minutes.

- **No AI summaries:**  
  If Ollama is not running, or the required model is missing, the tool cannot generate summaries.

- **pip install error:**  
  If you see `ERROR: Could not find a version that satisfies the requirement genai-pr-summarizer`, it means the package is not published to PyPI. Use `pip install .` from your local directory instead.

---

## Support

For issues, please open an [issue in this repository](https://github.com/Manoj-Kumar-BV/GenAI-Powered-Pull-Request-Summaries/issues).

---