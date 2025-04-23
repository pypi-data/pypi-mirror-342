import os
import json
import shutil
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from .functions import logger, format_timestamp, safe_dump_to_file
import whisper
from pathlib import Path
def transcribe_audio_file_clean(
    audio_path: str,
    json_data: str = None,
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
    
    json_data["audio_text"] = []
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

        json_data["audio_text"].append({
            "start_time": format_timestamp(start_ms),
            "end_time": format_timestamp(end_ms),
            "text": text
        })
        os.remove(chunk_path)

    # 3) Optionally write out the JSON

        full_text = [ entry["text"] 
                for entry in json_data.get("audio_text", []) 
                if entry.get("text") ]
        full_text = " ".join(full_text).strip()
        json_data["full_text"] = full_text
        safe_dump_to_file(json_data, json_data['info_path'])
    
    return json_data
def transcribe_with_whisper_local(
    json_data,
    audio_path: str,
    model_size: str = "medium",           # one of "tiny", "base", "small", "medium", "large"
    language: str = None
) -> str:
    """
    Returns the full transcript as a string.
    """
    model = whisper.load_model(model_size)           # loads to GPU if available
    # options: you can pass `task="translate"` for translating to English
 
    result = model.transcribe(audio_path, language=language)
    with open(json_data['info_path'], "r+", encoding="utf-8") as f:
        json_data = json.load(f)
        json_data["whisper_result"] = result
        f.seek(0); f.truncate()
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    return json_data
