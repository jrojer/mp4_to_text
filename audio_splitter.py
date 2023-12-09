import os
from butter.checks import check_that, is_dir, is_file, is_non_empty_dir


class AudioSplitter:
    def __init__(self, audio_path: str, chunk_output_path: str):
        check_that(is_file(audio_path), f"File {audio_path} does not exist")
        check_that(
            is_dir(chunk_output_path), f"Directory {chunk_output_path} does not exist"
        )
        self.audio_path = audio_path
        self.chunk_output_path = chunk_output_path

    def split_on_silence(self):
        if is_non_empty_dir(self.chunk_output_path):
            print(
                f"Directory {self.chunk_output_path} is not empty, skipping splitting"
            )
            return
        os.system('ffmpeg -i {} -af silenceremove=start_periods=1:start_duration=3:start_threshold=-44.69dB -f segment -segment_time 600 -segment_time_delta 10 -break_non_keyframes 1 {}/output_%03d.wav'
                  .format(self.audio_path, self.chunk_output_path))
