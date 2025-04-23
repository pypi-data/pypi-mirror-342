from .text_utils import *
from .audio_utils import *
from .functions import (logger,
                        create_key_value,
                        os,
                        timestamp_to_milliseconds,
                        format_timestamp,
                        get_time_now_iso,
                        parse_timestamp,
                        url_join)
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

def update_sitemap(video_data,
                   sitemap_path):
    with open(sitemap_path, 'a') as f:
        f.write(f"""
<url>
    <loc>{video_data['canonical_url']}</loc>
    <video:video>
        <video:title>{video_data['seo_title']}</video:title>
        <video:description>{video_data['seo_description']}</video:description>
        <video:thumbnail_loc>{video_data['thumbnail']['file_path']}</video:thumbnail_loc>
        <video:content_loc>{video_data['video_path']}</video:content_loc>
    </video:video>
</url>
""")
import math
from .functions import logger

def _format_srt_timestamp(seconds: float) -> str:
    """
    Convert seconds (e.g. 3.2) into SRT timestamp "HH:MM:SS,mmm"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - math.floor(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def export_srt_whisper(whisper_json: dict, output_path: str):
    """
    Write an .srt file from Whisper's verbose_json format.
    `whisper_json["segments"]` should be a list of {start,end,text,...}.
    """
    logger.info(f"export_srt_whisper: {output_path}")
    segments = whisper_json.get("segments", [])
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, seg in enumerate(segments, start=1):
            start_ts = _format_srt_timestamp(seg["start"])
            end_ts   = _format_srt_timestamp(seg["end"])
            text     = seg["text"].strip()
            f.write(f"{idx}\n")
            f.write(f"{start_ts} --> {end_ts}\n")
            f.write(f"{text}\n\n")
def export_srt(audio_text, output_path):
    logger.info(f"export_srt: {output_path}")
    with open(output_path, 'w') as f:
        for i, entry in enumerate(audio_text, 1):
            start = entry['start_time'].replace('.', ',')
            end = entry['end_time'].replace('.', ',')
            f.write(f"{i}\n{start} --> {end}\n{entry['text']}\n\n")

def pick_optimal_thumbnail(video_text,
                           combined_keywords):
    scores = []
    for entry in video_text:
        
        text = entry['text'].lower()
        
        keyword_score = sum(1 for kw in combined_keywords if kw.lower() in text)
        
        clarity_score = 1 if len(text.strip()) > 20 else 0  # basic clarity check
        
        end_phrase_penalty = -1 if "thanks for watching" in text else 0
        
        total_score = keyword_score + clarity_score + end_phrase_penalty
        
        scores.append((entry['frame'],
                       total_score,
                       text.strip()))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[0] if scores else None


def pick_optimal_thumbnail(whisper_result, combined_keywords, thumbnail_dir):
    """
    Pick the optimal thumbnail based on Whisper captions and associate with thumbnail images.
    
    Args:
        whisper_result: Dict containing Whisper transcription with segments.
        combined_keywords: List of keywords to score captions.
        thumbnail_dir: Path to directory containing thumbnails (e.g., frame_1.jpg, frame_2.jpg).
    
    Returns:
        Tuple (thumbnail_path, score, caption) for the best thumbnail, or None if no valid options.
    """
    scores = []
    
    # Get list of thumbnails from directory
    thumbnails = sorted(
        [f for f in os.listdir(thumbnail_dir) if f.startswith("frame_") and f.endswith(".jpg")],
        key=lambda x: int(x.split("_")[1].split(".")[0])  # Sort by frame number
    )
    
    # Process each Whisper segment
    for segment in whisper_result["segments"]:
        text = segment["text"].lower().strip()
        start_time = segment["start"]
        
        # Find the closest thumbnail based on start time
        # Assuming thumbnails are 1 per second, frame_N.jpg corresponds to N seconds
        frame_number = math.floor(start_time)  # or use math.ceil or round for different behavior
        thumbnail_name = f"frame_{frame_number}.jpg"
        
        # Check if thumbnail exists
        if thumbnail_name not in thumbnails:
            continue  # Skip if no matching thumbnail
        
        # Score the caption
        keyword_score = sum(1 for kw in combined_keywords if kw.lower() in text)
        clarity_score = 1 if len(text) > 20 else 0  # Basic clarity check
        end_phrase_penalty = -1 if "thanks for watching" in text else 0
        total_score = keyword_score + clarity_score + end_phrase_penalty
        
        # Store thumbnail path, score, and caption
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_name)
        scores.append((thumbnail_path, total_score, text))
    
    # Sort by score (highest first)
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    # Return the best result or None if no valid thumbnails
    return scores[0] if scores else None



def get_from_list(list_obj=None,length=1):
    list_obj = list_obj or []
    if len(list_obj) >= length:
        list_obj = list_obj[:length]
    return list_obj
def get_seo_data(info,
                 uploader=None,
                 domain=None,
                 categories=None,
                 videos_url=None):
    
    info = create_key_value(info,
                            'categories',
                            categories or {'ai': 'Technology', 'cannabis': 'Health', 'elon musk': 'Business'})
    
    info = create_key_value(info,
                            'uploader',
                            uploader or 'The Daily Dialectics')
    
    info = create_key_value(info,
                            'domain',
                            domain or 'https://thedailydialectics.com')
    
    info = create_key_value(info,
                            'videos_url',
                            videos_url or f"{info['domain']}/videos")
    
    for keyword_key in ['combined_keywords','keywords']:
        keywords = info.get(keyword_key,[])
        if keywords and len(keywords)>0:
            break
    primary_keyword = keywords[0] if keywords and len(keywords)>0 else info['filename']
    seo_title = f"{primary_keyword} - {info['filename']}"
    info['seo_title'] = get_from_list(seo_title,length=70)
    summary = info.get('summary','')
    summary_desc = get_from_list(summary,length=150)
    keywords_str = ', '.join(get_from_list(keywords,length=3))
    seo_desc = f"{summary_desc} Explore {keywords_str}. Visit thedailydialectics.com for more!"
    info['seo_description'] = get_from_list(seo_desc,length=300)
    
    info['seo_tags'] = [kw for kw in keywords if kw.lower() not in ['video','audio','file']]
    video_text = info.get('video_text')
    info['thumbnail']={}
    if video_text and len(video_text)>0:
        thumnail_data = video_text[0]
        info['thumbnail']['file_path']= os.path.join(info['thumbnails_directory'],
                                                     thumnail_data.get("frame"))
        
        info['thumbnail']['alt_text']= thumnail_data.get("text")
    whisper_json = info["whisper_result"]
    thumbnail_score = pick_optimal_thumbnail(whisper_json,
                                               keywords,
                                              info["thumbnails_directory"])
    if thumbnail_score:
        best_frame, score, matched_text = thumbnail_score
        
        info['thumbnail']['file_path']= os.path.join(info['thumbnails_directory'],
                                                     best_frame)
        
        info['thumbnail']['alt_text']= get_from_list(matched_text,length=100)
        
    audio = AudioSegment.from_wav(info['audio_path'])
    
    info['duration_seconds'] = len(audio) / 1000
    
    info['duration_formatted'] = format_timestamp(len(audio))
    
    

    export_srt_whisper(
        whisper_json,
        os.path.join(info["info_directory"], "captions.srt")
    )
    
    info['captions_path'] = os.path.join(info['info_directory'],
                                         "captions.srt")
    
    info['schema_markup'] = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": info['seo_title'],
        "description": info['seo_description'],
        "thumbnailUrl": info['thumbnail']['file_path'],
        "duration": f"PT{int(info['duration_seconds'] // 60)}M{int(info['duration_seconds'] % 60)}S",
        "uploadDate": get_time_now_iso(),
        "contentUrl": info['video_path'],
        "keywords": info['seo_tags']
    }
    
    info['social_metadata'] = {
        "og:title": info['seo_title'],
        "og:description": info['seo_description'],
        "og:image": info['thumbnail']['file_path'],
        "og:video": info['video_path'],
        "twitter:card": "player",
        "twitter:title": info['seo_title'],
        "twitter:description": info['seo_description'],
        "twitter:image": info['thumbnail']['file_path']
    }
    
    info['category'] = next((v for k, v in info['categories'].items() if k in ' '.join(info['seo_tags']).lower()), 'General')
    
    info['uploader'] = {"name": info['uploader'],
                        "url": info['domain']}
    
    info['publication_date'] = get_time_now_iso()
    
    video = mp.VideoFileClip(info['video_path'])
    
    info['file_metadata'] = {
        'resolution': f"{video.w}x{video.h}",
        'format': 'MP4',
        'file_size_mb': os.path.getsize(info['video_path']) / (1024 * 1024)
    }
    
    video.close()
    
    update_sitemap(info,
                   f"{info['parent_dir']}/../sitemap.xml")
    
    return info
