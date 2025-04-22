from .text_utils import *
from .audio_utils import *
from .seo_utils import *
from .functions import *

# Clear root logger handlers to prevent duplicate console output
logging.getLogger('').handlers.clear()

def transcribe_all_video_paths(directory=None,
                               output_dir=None,
                               remove_phrases=None,
                               summarizer=None,
                               kw_model=None,
                               get_vid_data=None,
                               uploader=None,
                               domain=None,
                               categories=None,
                               video_url=None):
    logger.info(f"Entering transcribe_all_video_paths")
    get_vid_data = get_vid_data or False
    remove_phrases = remove_phrases or []
    directory = directory or os.getcwd()
    output_dir = output_dir if output_dir else make_dirs(directory, 'text_dir')
    paths = glob.glob(path_join(directory, '**', '**'), recursive=True)
    paths = [file_path for file_path in paths if confirm_type(file_path, media_types=get_media_types(['video']))]
    video_paths = get_all_file_types(directory=directory, types='video') or get_all_file_types(directory=abs_dirname, types='videos')
    for video_path in video_paths:
        logger.info(f"Processing video: {video_path}")
        info = get_info_data(video_path, output_dir=output_dir, remove_phrases=remove_phrases)
        if not os.path.isfile(info['audio_path']):
            extract_audio_from_video(video_path=info['video_path'], audio_path=info['audio_path'])
        info = transcribe_audio_file(audio_path=info['audio_path'], json_data=info)
        info = get_text_and_keywords(info,summarizer=summarizer,kw_model=kw_model)
        info = get_seo_data(info,
                            uploader=uploader,
                            domain=domain,
                            categories=categories,
                            video_url=video_url)
        safe_dump_to_file(data=info, file_path=info['info_path'])
    logger.info(f"Exiting transcribe_all_video_paths")

def get_info_data(video_path, output_dir=None, remove_phrases=None):
    remove_phrases = remove_phrases or []
    dirname = os.path.dirname(video_path)
    basename = os.path.basename(video_path)
    filename, ext = os.path.splitext(basename)
    video_directory = make_dirs(output_dir, filename)
    info_path = os.path.join(video_directory, 'info.json')
    video_text_path = os.path.join(video_directory, 'video_text.json')
    audio_path = os.path.join(video_directory, 'audio.wav')
    video_json_path = os.path.join(video_directory, 'video_json.json')
    info = {}
    if os.path.isfile(info_path):
        info = safe_read_from_json(info_path)
    info['video_path'] = video_path
    info['video_directory'] = video_directory
    info['info_path'] = info_path
    info['filename'] = filename
    info['ext'] = ext
    info['remove_phrases'] = remove_phrases
    info['audio_path'] = audio_path
    info['video_json'] = video_json_path
    safe_dump_to_file(data=info, file_path=info['info_path'])
    return info

