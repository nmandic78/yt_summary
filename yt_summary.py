"""
YouTube Audio Downloader and Transcription Tool

This script allows users to download the audio from a YouTube video, transcribe it using a Whisper model,
and generate a concise summary using a language model via a local llama.cpp server. The summary includes
the title, a summary, main topics with descriptions and sources, and a conclusion, all formatted in Markdown.

Dependencies:
    - yt_dlp (requires ffmpeg to be installed)
    - faster_whisper
    - openai
    - tiktoken
    - rich

Usage:
    First start llama cpp server with model of your choice: ./llama-server -m /mnt/disk2/LLM_MODELS/models/gemma-2-9b-it-Q8_0.gguf -ngl 99 -c 8192
    python yt_summary.py --video_url <YouTube_URL> [--mp3_dir <MP3_DIRECTORY>] [--transcript_dir <TRANSCRIPT_DIRECTORY>]
"""

import yt_dlp
import os, sys
import argparse
from faster_whisper import WhisperModel
import openai
import tiktoken
from rich.console import Console
from rich.markdown import Markdown


# Initialize the Whisper model
model_path = "Systran/faster-distil-whisper-large-v3" # will download the model from huggingface on first run or you download manually and put in some folder
faster_whisper_model = WhisperModel(model_path, device="cuda", compute_type="bfloat16")

console = Console()

client = openai.OpenAI(
    base_url="http://localhost:8080/v1", # server started with llama.cpp server
    api_key = "sk-no-key-required"
)

system_prompt = """You are an expert consultant who has years of experience in journalism, management summaries creation, and analyses of different topics. You pride yourself on incredible accuracy and attention to detail. You always stick to the facts in the sources provided, and never make up new facts.

Now look at the transcription of youtube video below, and write the following in concise and informative way using Markdown formating.

The title.
Summary.
Main covered topics and facts with short description and source or citation if suitable.
Conclusion.

Transcription: """

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_brief(transcript: str) -> str:
    """
    Generate a concise summary of the transcript using the language model.

    Args:
        transcript (str): The transcription text from the audio.

    Returns:
        str: The generated summary in Markdown format.
    """
    messages = [
        {
            "role": "system",
            "content": f"{system_prompt}"
        },
        {
            "role": "user",
            "content": f"{transcript}"
        }
    ]
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, temperature=0.1, max_tokens=2048)
    response = completion.choices[0].message.content

    return response

def download_audio(video_url: str, output_dir: str) -> tuple:
    """
    Download audio from a YouTube video URL and save it as an MP3 file.

    Args:
        video_url (str): The URL of the YouTube video.
        output_dir (str): The directory to save the MP3 file.

    Returns:
        tuple: A tuple containing the absolute path to the MP3 file and the original filename.

    Raises:
        SystemExit: If the download fails or an unexpected error occurs.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,    # Only keep the audio
            'audioformat': 'mp3',    # Convert to mp3
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Save to the custom directory with the video title as filename
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'nooverwrites': True,
            'quiet': True,  # Suppress download messages
            'noplaylist': True,  # Only download a single video, no playlists
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            mp3_file = file_name.rsplit('.', 1)[0] + '.mp3'
            return os.path.abspath(mp3_file), file_name
    except yt_dlp.utils.DownloadError as e:
        console.print(f"[red]Download failed: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        sys.exit(1)


def transcribe_audio_faster(audio: str) -> str:
    """
    Transcribe the given audio file using the Faster Whisper model.

    Args:
        audio (str): The path to the audio file to transcribe.

    Returns:
        str: The transcribed text.
    """
    segments, _ = faster_whisper_model.transcribe(audio, task="transcribe", language='en', without_timestamps=True)
    transcription = ''.join([segment.text for segment in segments])
    return transcription


def main():
    """
    Main function to handle argument parsing and orchestrate the download, transcription,
    token counting, and summary generation processes. Change the default paths to your liking or set with argument
    """
    parser = argparse.ArgumentParser(description='Download YouTube video audio as MP3, transcribe it, and generate a summary.')
    parser.add_argument('-v', '--video_url', required=True, help='YouTube video URL')
    parser.add_argument('-m', '--mp3_dir', default='.', help='Directory to save MP3 file')
    parser.add_argument('-t', '--transcript_dir', default='.', help='Directory to save transcription text file')

    args = parser.parse_args()

    # Download the audio from YouTube
    mp3_file_path, filename = download_audio(args.video_url, args.mp3_dir)

    print(f"Downloaded MP3 file at: {mp3_file_path}")

    # Transcribe the downloaded audio
    transcription = transcribe_audio_faster(mp3_file_path)
    transcript_dir = args.transcript_dir

    # Prepare the output filename for the transcription
    output_filename = os.path.splitext(filename)[0] + "_transcript.txt"
    output_path = os.path.join(transcript_dir, output_filename)

    # Save the transcription to a text file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(transcription)
    print(f"Transcribed '{mp3_file_path}' to '{output_filename}'")

    # Count the number of tokens in the transcription
    num_tokens = num_tokens_from_string(transcription, "cl100k_base")
    print('Number of tokens in transcript: ', num_tokens)

    # Generate and display the summary using the language model
    brief_txt = get_brief(transcription)
    console.print(Markdown(brief_txt))

if __name__ == '__main__':
    main()
