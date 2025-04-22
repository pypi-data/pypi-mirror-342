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
def update_sitemap(video_data, sitemap_path):
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
def pick_optimal_thumbnail(video_text, combined_keywords):
    scores = []

    for entry in video_text:
        text = entry['text'].lower()
        keyword_score = sum(1 for kw in combined_keywords if kw.lower() in text)
        clarity_score = 1 if len(text.strip()) > 20 else 0  # basic clarity check
        end_phrase_penalty = -1 if "thanks for watching" in text else 0
        total_score = keyword_score + clarity_score + end_phrase_penalty

        scores.append((entry['frame'], total_score, text.strip()))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[0] if scores else None
def get_seo_data(info,uploader=None,domain=None,categories=None,video_url=None):
    categories = categories or {'ai': 'Technology', 'cannabis': 'Health', 'elon musk': 'Business'}
    uploader = uploader or 'The Daily Dialectics'
    domain = domain or 'https://thedailydialectics.com'
    video_url = video_url or url_join(domain,videos)
    primary_keyword = info['combined_keywords'][0] if info['combined_keywords'] else info['filename']
    info['seo_title'] = f"{primary_keyword} - {info['filename']}"[:70]
    summary = info.get('summary', 'No summary available.')
    keywords_str = ', '.join(info['combined_keywords'][:3])
    info['seo_description'] = f"{summary[:150]} Explore {keywords_str}. Visit thedailydialectics.com for more!"[:300]
    info['seo_tags'] = [kw for kw in info['combined_keywords'] if kw.lower() not in ['video', 'audio', 'file']]
    best_frame, score, matched_text = pick_optimal_thumbnail(info['video_text'], info['combined_keywords'])
    info['thumbnail'] = {
        'file_path': os.path.join(info['thumbnails_dir'], best_frame),
        'alt_text': matched_text[:100]
    }
    audio = AudioSegment.from_wav(info['audio_path'])
    info['duration_seconds'] = len(audio) / 1000
    info['duration_formatted'] = format_timestamp(len(audio))
    export_srt(info['audio_text'], os.path.join(info['video_directory'],"captions.srt")
    info['captions_path'] = os.path.join(info['video_directory'],"captions.srt")
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
    
    info['category'] = next((v for k, v in categories.items() if k in ' '.join(info['seo_tags']).lower()), 'General')
    info['uploader'] = {"name": uploader, "url": domain}
    info['publication_date'] = get_time_now_iso()
    video = mp.VideoFileClip(info['video_path'])
    info['file_metadata'] = {
        'resolution': f"{video.w}x{video.h}",
        'format': 'MP4',
        'file_size_mb': os.path.getsize(info['video_path']) / (1024 * 1024)
    }
    video.close()
    video_id = info['filename'].replace(' ', '-').lower()
    info['canonical_url'] = url_join(video_url,video_id)
    update_sitemap(info, f"{info['video_directory']}/../sitemap.xml")
    return info
