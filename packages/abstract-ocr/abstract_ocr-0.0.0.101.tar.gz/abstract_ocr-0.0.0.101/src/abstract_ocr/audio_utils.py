from .functions import (logger,
                        create_key_value,
                        timestamp_to_milliseconds,
                        format_timestamp,
                        parse_timestamp,
                        get_time_now_iso,
                        shutil,
                        os,
                        safe_dump_to_file)
from moviepy.editor import *
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
r = sr.Recognizer()
def check_if_transcribed_block(audio_text, start_time, end_time):
    for entry in audio_text:
        entry_start = timestamp_to_milliseconds(entry.get("start_time", "0:00"))
        entry_end = timestamp_to_milliseconds(entry.get("end_time", "0:00"))
        if entry_start <= start_time and entry_end >= end_time and entry.get("text", "").strip():
            return True
    uncovered_start, uncovered_end = start_time, end_time
    for entry in audio_text:
        entry_start = parse_timestamp(entry.get("start_time", "0:00"))
        entry_end = parse_timestamp(entry.get("end_time", "0:00"))
        if not entry.get("text", "").strip():
            continue
        if entry_start <= uncovered_start < entry_end:
            uncovered_start = entry_end
        if entry_start < uncovered_end <= entry_end:
            uncovered_end = entry_start
    return (uncovered_start, uncovered_end)
def transcribe_audio_file(audio_path, json_data, chunk_length_ms=60000):
    logger.info(f"transcribe_audio_file: {audio_path}")
    audio = AudioSegment.from_wav(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    json_data = create_key_value(json_data, 'audio_text', [])
    video_directory = json_data['video_directory']
    file_path = json_data['info_path']
    temp_file_path = file_path.replace('.json', '_temp.json')
    full_text = ""
    chunk_path = f"{video_directory}/temp_chunk.wav"
    for i, chunk in enumerate(chunks):
        start_time = i * chunk_length_ms
        end_time = min((i + 1) * chunk_length_ms, len(audio))
        result = check_if_transcribed_block(json_data['audio_text'], start_time, end_time)
        if result is True:
            continue
        updated_start, updated_end = result
        chunk_path = f"{video_directory}/chunk_{i}_partial.wav"
        audio[updated_start:updated_end].export(chunk_path, format="wav")
        with sr.AudioFile(chunk_path) as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
            except:
                text = ""
        
        json_data['audio_text'].append({
            "start_time": format_timestamp(updated_start),
            "end_time": format_timestamp(updated_end),
            "text": text
        })
        safe_dump_to_file(json_data, temp_file_path)
        if os.path.isfile(chunk_path):
            os.remove(chunk_path)
    if os.path.isfile(chunk_path):
        os.remove(chunk_path)
    if os.path.isfile(temp_file_path):
        shutil.move(temp_file_path,file_path)
    return json_data
def export_srt(audio_text, output_path):
    logger.info(f"export_srt: {output_path}")
    with open(output_path, 'w') as f:
        for i, entry in enumerate(audio_text, 1):
            start = entry['start_time'].replace('.', ',')
            end = entry['end_time'].replace('.', ',')
            f.write(f"{i}\n{start} --> {end}\n{entry['text']}\n\n")
def extract_audio_from_video(video_path, audio_path):
    """Extract audio from a video file using moviepy."""
    try:
        logger.info(f"Extracting audio from {video_path} to {audio_path}")
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        video.close()
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file {audio_path} was not created.")
        logging.info(f"Audio extracted successfully: {audio_path}")
        return audio_path
    except Exception as e:
        logging.error(f"Error extracting audio from {video_path}: {e}")
        return None
def get_voice(voice, text=None):
    """Save transcribed text to a file."""
    text = text or ''
    if voice:
        text = text + '\n' + str(voice) if text else str(voice)
    return text
