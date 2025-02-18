# Web Ollama Ver.2

A better web crawler, inspired from the version 1.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Web Ollama Ver.2 is an advanced web crawler built entirely using Python. This project is a significant improvement over its predecessor, incorporating new features and optimizations for better performance and ease of use.

## Features

- Efficient web crawling
- Improved data extraction
- Enhanced error handling
- Support for text-to-speech (TTS) functionalities

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

To use the web crawler, run the following command:

```bash
python main.py
```

You can configure the crawling parameters in the `config.json` file.

## Contributing

We welcome contributions to improve Web Ollama Ver.2. If you have any ideas, suggestions, or issues, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
