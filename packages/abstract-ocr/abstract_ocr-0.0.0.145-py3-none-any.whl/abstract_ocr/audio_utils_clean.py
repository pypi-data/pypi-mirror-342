import os
import json
import shutil
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from .functions import logger, format_timestamp, safe_dump_to_file

def transcribe_audio_file_clean(
    audio_path: str,
    output_json: str = None,
    min_silence_len: int = 500,
    silence_thresh_delta: int = 16
):
    """
    Load `audio_path`, detect all non-silent ranges, transcribe each,
    and (optionally) dump to JSON at `output_json`.
    """
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)

    # 1) Calibrate once on the first second
    calib = audio[:1000]
    calib_path = os.path.join(os.path.dirname(audio_path), "_calib.wav")
    calib.export(calib_path, format="wav")
    with sr.AudioFile(calib_path) as src:
        recognizer.adjust_for_ambient_noise(src, duration=1)
    os.remove(calib_path)

    # 2) Compute dynamic silence threshold, then find real speech segments
    silence_thresh = audio.dBFS - silence_thresh_delta
    nonsilent = detect_nonsilent(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    results = []
    for idx, (start_ms, end_ms) in enumerate(nonsilent):
        logger.info(f"Transcribing segment {idx}: {start_ms}-{end_ms} ms")
        chunk = audio[start_ms:end_ms]

        chunk_path = f"_chunk_{idx}.wav"
        chunk.export(chunk_path, format="wav")

        with sr.AudioFile(chunk_path) as src:
            audio_data = recognizer.record(src)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = ""

        results.append({
            "start_time": format_timestamp(start_ms),
            "end_time": format_timestamp(end_ms),
            "text": text
        })
        os.remove(chunk_path)

    # 3) Optionally write out the JSON
    if output_json:
        payload = {"audio_text": results}
        safe_dump_to_file(payload, output_json)

    return results
