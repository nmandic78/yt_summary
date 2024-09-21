
# YouTube Audio Transcription and Summarization Tool

A Python-based tool to download audio from YouTube videos, transcribe the audio using Faster Whisper, and generate concise summaries with a locally hosted LLaMA language model.

## Table of Contents

- Features
- Prerequisites
- Installation
- Setting Up llama.cpp Server
- Downloading the Language Model
- Usage
- Example
- Troubleshooting
- Contributing
- License

## Features

- **Download Audio**: Extracts audio from YouTube videos in MP3 format.
- **Transcription**: Utilizes Faster Whisper with GPU acceleration for efficient and accurate transcription.
- **Summarization**: Generates concise summaries using a locally hosted LLaMA language model.
- **Token Counting**: Provides the number of tokens in the transcription for API usage management.
- **User-Friendly Output**: Displays summaries in Markdown format using the rich library for enhanced readability.

## Prerequisites

Before using this tool, ensure you have the following installed on your system:

- **Python 3.8+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org).

- **FFmpeg**: Required for audio processing.
    - Ubuntu/Debian:
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```
    - macOS (using Homebrew):
    ```bash
    brew install ffmpeg
    ```
    - Windows:
        Download the latest FFmpeg build from [FFmpeg Downloads](https://ffmpeg.org/download.html).
        Follow the installation instructions for your system.

- **CUDA**: If you have an NVIDIA GPU and wish to utilize GPU acceleration for Faster Whisper, ensure CUDA is installed and properly configured. Refer to the [CUDA Installation Guide](https://developer.nvidia.com/cuda-downloads) for details.

- **Git**: To clone repositories.
    - Ubuntu/Debian:
    ```bash
    sudo apt install git
    ```
    - macOS (using Homebrew):
    ```bash
    brew install git
    ```
    - Windows:
        Download and install Git from [git-scm.com](https://git-scm.com).

## Installation

### Clone the Repository
```bash
git clone https://github.com/yourusername/yt-audio-transcriber.git
cd yt-audio-transcriber
```

### Create a Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Python Dependencies

Ensure you have pip updated:
```bash
pip install --upgrade pip
```

Install the required packages:
```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt, you can install dependencies manually:
```bash
pip install yt-dlp faster-whisper openai tiktoken rich
```

## Setting Up llama.cpp Server

To generate summaries, the tool relies on a locally hosted LLaMA language model using llama.cpp. Follow the steps below to set up the server.

### Clone the llama.cpp Repository
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```

### Build the Server

Ensure you have the necessary build tools installed (e.g., make, gcc).
```bash
make
```

This will compile the llama-server executable.

### Download a LLaMA Model from Hugging Face

- Visit the [Hugging Face Models](https://huggingface.co/models) page.
- Search for a compatible LLaMA model, such as gemma-2-9b-it-Q8_0.gguf.
- Download the model and place it in a directory of your choice, e.g., /mnt/disk2/LLM_MODELS/models/gemma-2-9b-it-Q8_0.gguf.

Note: Ensure you have the rights and necessary permissions to use the model.

### Run the llama.cpp Server

Execute the server with your chosen model:
```bash
./llama-server -m /mnt/disk2/LLM_MODELS/models/gemma-2-9b-it-Q8_0.gguf -ngl 99 -c 8192
```

Parameters Explained:
- `-m`: Path to the model file.
- `-ngl`: Number of GPU layers (adjust based on your GPU capabilities).
- `-c`: Context size in tokens (adjust as needed).

The server will start and listen on http://localhost:8080/v1.

## Downloading the Language Model

If you haven't downloaded a LLaMA model yet, follow the steps in the **Setting Up llama.cpp Server** section to obtain a compatible model from Hugging Face.

## Usage

Once you have set up the llama.cpp server and installed all dependencies, you can use the transcription and summarization tool.

### Command-Line Arguments

- `-v, --video_url`: (Required) YouTube video URL to download and transcribe.
- `-m, --mp3_dir`: (Optional) Directory to save the downloaded MP3 file. Default: /home/yourusername/Music/YT_AUDIOS/
- `-t, --transcript_dir`: (Optional) Directory to save the transcription text file. Default: /home/yourusername/Music/YT_AUDIOS/

### Running the Script
```bash
python your_script_name.py -v <YouTube_Video_URL> [options]
```

Example:
```bash
python transcribe_and_summarize.py -v https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

This command will:
- Download the audio from the provided YouTube video URL and save it as an MP3 file in the default directory.
- Transcribe the audio using Faster Whisper.
- Generate a summary using the locally hosted LLaMA model.
- Display the summary in the console and save the transcription to a text file.

### Specifying Custom Directories

You can specify custom directories for saving MP3 files and transcriptions:
```bash
python transcribe_and_summarize.py -v <YouTube_Video_URL> -m /path/to/mp3_dir -t /path/to/transcript_dir
```

## Troubleshooting

- **FFmpeg Not Found**: Ensure FFmpeg is installed and added to your system's PATH.
- **CUDA Issues**: Verify that CUDA is correctly installed and that your GPU supports the required operations.
- **llama.cpp Server Not Running**: Ensure the server is running before executing the transcription script. Verify the server URL and port.
- **Missing Dependencies**: Ensure all Python packages are installed. Re-run `pip install -r requirements.txt` if necessary.
- **Insufficient Permissions**: Check directory permissions for saving MP3 and transcription files.

## Contributing

Contributions are welcome! Please follow these steps:

### Fork the Repository

### Create a Feature Branch
```bash
git checkout -b feature/YourFeature
```

### Commit Your Changes
```bash
git commit -m "Add YourFeature"
```

### Push to the Branch
```bash
git push origin feature/YourFeature
```

### Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate documentation.

## License

This project is licensed under the MIT License.

Developed by Your Name
