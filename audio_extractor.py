import os

from butter.checks import check_that, is_file


class AudioExtractor:
    def __init__(self, video_path: str, audio_path: str):
        check_that(is_file(video_path), f"File {video_path} does not exist")
        self.video_path = video_path
        self.audio_path = audio_path

    def extract_audio(self):
        if is_file(self.audio_path):
            print(f"File {self.audio_path} already exists, skipping extraction")
            return
        os.system(
            f"ffmpeg -i {self.video_path} -acodec pcm_s16le -ac 1 -ar 16000 {self.audio_path}"
        )
