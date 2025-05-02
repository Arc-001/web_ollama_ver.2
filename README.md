# Web Ollama Ver.2

A better web crawler, inspired from the version 1.
This is actually a toy copy of perplexity... 
why?? because it is fun :) 

## Features

- Efficient web crawling by multhreaded fetches
- Improved data extraction by custom tag decomposition
- Enhanced error handling(eeh kinda but it is something)
- Support for text-to-speech (TTS) functionalities (uses kokoro which is local)

## How it Works

When you run `faster_crawler.py` and provide a query:

1.  **Web Search:** The script uses DuckDuckGo (`duckduckgo_search`) to find relevant web pages based on your query.
2.  **Parallel Crawling:** It fetches the content from the top search results concurrently using Python's `concurrent.futures`. The `crawler.py` script handles fetching and parsing HTML, extracting the title, headings, and main content while removing scripts, styles, and navigation elements.
3.  **Content Processing & Embedding:** The extracted text content from all crawled pages is processed. An embedding model (e.g., `mxbai-embed-large` via `langchain-ollama`) is used to create vector representations of the text chunks. These embeddings are stored in an in-memory vector store (`langchain_core.vectorstores.InMemoryVectorStore`).
4.  **Similarity Search:** The script performs a similarity search within the vector store using your original query to find the most relevant text chunks from the crawled content.
5.  **LLM Query:** The retrieved relevant text chunks are combined and passed as context, along with your original query, to a large language model (LLM) hosted by Ollama (e.g., `llama3.2:3b`). The `langchain` library orchestrates this process.
6.  **Response Generation:** The LLM generates a response based on the provided context and query.
7.  **Text-to-Speech (Optional):** The generated text response is then converted into speech using the Kokoro TTS library (`tts.py`) and played back using `sounddevice`.

## Installation

To get started with Web Ollama Ver.2, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Arc-001/web_ollama_ver.2.git
   cd web_ollama_ver.2
   ```

2. Set up a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. For the text-to-speech (TTS) functionality to work properly, you need to install `portaudio-devel`:

   - On Ubuntu/Debian:

     ```bash
     sudo apt-get install portaudio19-dev
     ```

   - On Fedora:

     ```bash
     sudo dnf install portaudio-devel
     ```

   - On macOS:

     ```bash
     brew install portaudio
     ```

## Usage

To use the web crawler and query interface, run the `faster_crawler.py` script:

```bash
python faster_crawler.py
```

The script will prompt you to enter a query. It will then perform a web search, crawl the results, process the content using Ollama, and optionally provide a text-to-speech output of the final answer.

You can configure the crawling parameters and models used within the Python scripts (`crawler.py`, `faster_crawler.py`, `embedding.py`).

## Contributing

We welcome contributions to improve Web Ollama Ver.2. If you have any ideas, suggestions, or issues, please open an issue or submit a pull request.

