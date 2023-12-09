import json
from pathlib import Path
from audio_extractor import AudioExtractor
from audio_splitter import AudioSplitter

from audio_transcriptor import AudioTranscriptor
from text_corrector import TextCorrector

dot = Path(".")

video_dir = dot / "data/video/"
audio_dir = dot / "data/audio/"
chunk_dir = dot / "data/chunks/"
transcript_dir = dot / "data/transcripts/"
corrections_dir = dot / "data/corrections/"

def iterate_over(dir: Path, extension: str):
    for item in sorted(list(dir.iterdir())):
        if item.suffix == extension:
            yield item


def extract_audio(video_filepath: Path) -> Path:
    audio_filepath = Path(audio_dir) / (video_filepath.stem + ".wav")
    AudioExtractor(video_filepath, str(audio_filepath)).extract_audio()
    return audio_filepath


def split_audio(audio_filepath: Path) -> Path:
    chunk_sub_dir = Path(chunk_dir) / audio_filepath.stem
    chunk_sub_dir.mkdir(parents=True, exist_ok=True)
    AudioSplitter(audio_filepath, str(chunk_sub_dir)).split_on_silence()
    return chunk_sub_dir


def transcribe_audio(chunk_sub_dir: Path):
    transcript_sub_dir = Path(transcript_dir) / Path(chunk_sub_dir).stem
    previous_transcription: str = ""
    for chunk_wav in iterate_over(chunk_sub_dir, ".wav"):
        transcript_filepath = transcript_sub_dir / (chunk_wav.stem + ".json")
        transcript_filepath.parent.mkdir(parents=True, exist_ok=True)
        previous_transcription = AudioTranscriptor(
            chunk_wav, str(transcript_filepath)
        ).transcribe(previous_transcription)
    return transcript_sub_dir


def correct_transcripts(transcript_sub_dir: Path):
    corrections_sub_dir = Path(corrections_dir) / Path(transcript_sub_dir).stem
    transcript_edited_so_far: str = ""
    for chunk_json in iterate_over(transcript_sub_dir, ".json"):
        correction_filepath = corrections_sub_dir / (chunk_json.stem + ".txt")
        correction_filepath.parent.mkdir(parents=True, exist_ok=True)
        if correction_filepath.exists():
            print(f"File {correction_filepath} already exists, skipping correction")
            continue
        print(f"Correcting transcript {chunk_json}")
        with open(chunk_json) as chunk_json_file:
            chunk_text = json.loads(chunk_json_file.read())["text"]
        corrected_text = TextCorrector(transcript_edited_so_far).correct(chunk_text)
        transcript_edited_so_far += corrected_text
        with open(correction_filepath, "w") as correction_file:
            correction_file.write(corrected_text)
    return corrections_sub_dir


for video_filepath in iterate_over(video_dir, ".mp4"):
    audio_filepath = extract_audio(video_filepath)
    chunk_sub_dir = split_audio(audio_filepath)
    transcript_sub_dir = transcribe_audio(chunk_sub_dir)
    corrections_sub_dir = correct_transcripts(transcript_sub_dir)
