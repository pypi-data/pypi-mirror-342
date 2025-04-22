#!/usr/bin/env python3
import os
import glob
import logging
import json
import os,sys
from multiprocessing import Process
import speech_recognition as sr
from abstract_utilities import *
from moviepy.editor import *
import moviepy.editor as mp
from pydub import AudioSegment
from datetime import timedelta
from .video_utils import derive_all_video_meta
logger = get_logFile('vid_to_aud')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vid_to_aud.log'),
        logging.StreamHandler()
    ]
)

# Initialize recognizer
r = sr.Recognizer()

def format_timestamp(ms):
    """Convert milliseconds to a formatted timestamp (HH:MM:SS.mmm)."""
    td = timedelta(milliseconds=ms)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def extract_audio_from_video(video_path, audio_path):
    """Extract audio from a video file using moviepy."""
    try:
        logging.info(f"Extracting audio from {video_path} to {audio_path}")
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

def transcribe_audio_file(audio_path, json_data, chunk_length_ms=60000):
    """Transcribe audio file in chunks and save as text and time-blocked JSON."""
    try:
        logging.info(f"Transcribing audio: {audio_path}")
        audio = AudioSegment.from_wav(audio_path)
        chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        full_text = ""
        json_data['audio_text'] = []

        for i, chunk in enumerate(chunks):
            start_time = i * chunk_length_ms
            end_time = min((i + 1) * chunk_length_ms, len(audio))
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            logging.info(f"Processing chunk {i+1}/{len(chunks)} ({format_timestamp(start_time)} - {format_timestamp(end_time)})")

            with sr.AudioFile(chunk_path) as source:
                r.adjust_for_ambient_noise(source)
                audio_data = r.record(source)
                try:
                    text = r.recognize_google(audio_data)
                    full_text += text + " "
                    json_data['audio_text'].append({
                        "start_time": format_timestamp(start_time),
                        "end_time": format_timestamp(end_time),
                        "text": text
                    })
                except sr.UnknownValueError:
                    logging.warning(f"Chunk {i+1} could not be transcribed.")
                    json_data['audio_text'].append({
                        "start_time": format_timestamp(start_time),
                        "end_time": format_timestamp(end_time),
                        "text": ""
                    })
                except sr.RequestError as e:
                    logging.error(f"API error for chunk {i+1}: {e}")
                    json_data['audio_text'].append({
                        "start_time": format_timestamp(start_time),
                        "end_time": format_timestamp(end_time),
                        "text": ""
                    })
            os.remove(chunk_path)  # Clean up chunk file

        # Save plain text
        if full_text:
            full_text = full_text.strip()
        text_result= get_voice(full_text, text=full_text)
        json_data['full_text']=text_result
        json_data['summary']=None
        if summarizer:
            try:
                json_data['summary'] = summarizer(text_result, max_length=160, min_length=40)
            except Exception as e:
                logging.error(f"Error getting summary for {json_data['filename']}: {e}")

        return json_data
    except Exception as e:
        logging.error(f"Error transcribing {audio_path}: {e}")
        return None, json_path

def get_voice(voice, text=None):
    """Save transcribed text to a file."""
    text = text or ''
    if voice:
        text = text + '\n' + str(voice) if text else str(voice)
        logging.info(f"Text saved to {voice_txt_path}")
    return text
    
def initiate_process(target,*args):
    p = Process(target=target, args=args)
    p.start()
    logging.info(f"Started process for: {args}")
def transcribe_all_video_paths(directory=None,output_dir=None,remove_phrases=None,summarizer=None):
    remove_phrases=remove_phrases or []
    directory = directory or os.getcwd()
    output_dir = output_dir if output_dir else make_dirs(directory,'text_dir')
    paths = glob.glob(path_join(directory, '**', '**'), recursive=True)
    paths = [file_path for file_path in paths if confirm_type(file_path,media_types=get_media_types(['video']))]
    video_paths = get_all_file_types(directory=directory,types='video') or get_all_file_types(directory=abs_dirname,types='videos')
    for video_path in video_paths:
        transcribe_audio(video_path,output_dir=output_dir,remove_phrases=remove_phrases,summarizer=summarizer)
def transcribe_audio(video_path,output_dir=None,remove_phrases=None,summarizer=None):
    remove_phrases=remove_phrases or []
    dirname = os.path.dirname(video_path)
    basename = os.path.basename(video_path)
    filename,ext = os.path.splitext(basename)
    video_directory = make_dirs(output_dir,filename)
    info_path = os.path.join(video_directory,'info.json')
    video_text_path = os.path.join(video_directory,'video_text.json')
    audio_path = os.path.join(video_directory,'audio.wav')
    video_json_path = os.path.join(video_directory,'video_json.json')
    args_tuple = (video_path, video_directory, video_json_path, [], '', filename,remove_phrases,summarizer)
    initiate_process(derive_all_video_meta, *args_tuple)
    info = {}
    info['video_path']=video_path
    info['info_directory']=video_directory
    info['info_path']=info_path
    info['filename']=filename
    info['ext']=ext
    info['audio_path']=audio_path
    info['video_json']=video_json_path
    extract_audio_from_video(video_path=info['video_path'],audio_path=info['audio_path'])
    info = transcribe_audio_file(audio_path=info['audio_path'],json_data=info)
    safe_dump_to_file(data=info,file_path=info['info_path']) 
   
    
