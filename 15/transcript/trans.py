import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# 1. Load environment and initialize Groq client
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)

# 2. Directory containing your 4 audio files
AUDIO_DIR = Path("/home/sunan/Documents/Course/AI/15/file")
OUTPUT_FILE = "video_transcripts.json"


def format_timestamp(seconds: float) -> str:
    """Converts seconds (e.g. 75.4) to HH:MM:SS format (e.g. 00:01:15)."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"


def transcribe_single_file(file_path: Path):
    print(f"\nProcessing: {file_path.name}")
    
    with open(file_path, "rb") as f:
        # Request verbose_json to receive start and end timestamps per segment
        response = client.audio.transcriptions.create(
            file=(file_path.name, f.read()),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    # Handle object or dict response safely
    segments = response.segments if hasattr(response, "segments") else response["segments"]

    chunks = []
    video_title = file_path.stem  # File name without the .mp3 extension

    for seg in segments:
        seg_dict = seg if isinstance(seg, dict) else seg.__dict__
        text = seg_dict.get("text", "").strip()

        if not text:
            continue

        start_sec = float(seg_dict.get("start", 0.0))
        end_sec = float(seg_dict.get("end", 0.0))

        chunks.append({
            "video_name": video_title,
            "text": text,
            "start_time": start_sec,
            "end_time": end_sec,
            "timestamp": format_timestamp(start_sec)
        })

    return chunks


def main():
    # Find all mp3 files in the folder sorted by name
    mp3_files = sorted(list(AUDIO_DIR.glob("*.mp3")))

    if not mp3_files:
        print(f"No .mp3 files found in {AUDIO_DIR}")
        return

    print(f"Found {len(mp3_files)} audio files:")
    for f in mp3_files:
        print(f" - {f.name}")

    all_transcripts = []

    for file_path in mp3_files:
        records = transcribe_single_file(file_path)
        all_transcripts.extend(records)
        print(f" Extracted {len(records)} timestamped segments.")

    # Save everything to JSON for Qdrant ingestion
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_transcripts, f, indent=2, ensure_ascii=False)

    print(f"\n Done! Successfully saved {len(all_transcripts)} chunks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()