from .text_utils import *
from .audio_utils import *
from .seo_utils import *
from .ocr_utils import *
from .functions import *

# Clear root logger handlers to prevent duplicate console output
logging.getLogger('').handlers.clear()
###json_data,chunk_length_ms=10000,renew=False
def transcribe_all_video_paths(directory=None,
                               output_dir=None,
                               remove_phrases=None,
                               summarizer=None,
                               kw_model=None,
                               uploader=None,
                               domain=None,
                               categories=None,
                               video_url=None,
                               chunk_length_ms=None,
                               chunk_length_diff=None,
                               renew=None):
    logger.info(f"Entering transcribe_all_video_paths")
    directory = directory or os.getcwd()
    paths = glob.glob(path_join(directory, '**', '**'), recursive=True)
    paths = [file_path for file_path in paths if confirm_type(file_path,
                                                              media_types=get_media_types(['video']))]
    video_paths = get_all_file_types(directory=directory, types='video') or get_all_file_types(directory=abs_dirname, types='videos')
    for video_path in video_paths:
        transcribe_video_path(video_path=video_path,
                              output_dir=output_dir,
                              remove_phrases=remove_phrases,
                              summarizer=summarizer,
                              kw_model=kw_model,
                              uploader=uploader,
                              domain=domain,
                              categories=categories,
                              video_url=video_url,
                              chunk_length_ms=chunk_length_ms,
                              chunk_length_diff=chunk_length_diff,
                              renew=renew)
    logger.info(f"Exiting transcribe_all_video_paths")

def transcribe_video_path(video_path,
                          output_dir=None,
                          remove_phrases=None,
                          summarizer=None,
                          kw_model=None,
                          uploader=None,
                          domain=None,
                          categories=None,
                          video_url=None,
                          chunk_length_ms=None,
                          chunk_length_diff=None,
                          renew=None):
    remove_phrases = remove_phrases or []
    output_dir = output_dir if output_dir else make_dirs(directory, 'text_dir')
    logger.info(f"Processing video: {video_path}")
    info = get_info_data(video_path,
                         output_dir=output_dir,
                         remove_phrases=remove_phrases,
                         uploader=uploader,
                         domain=domain,
                         categories=categories,
                         video_url=video_url,
                         chunk_length_ms=chunk_length_ms,
                         chunk_length_diff=chunk_length_diff,
                         renew=renew)
    if not os.path.isfile(info['audio_path']):
        extract_audio_from_video(video_path=info['video_path'],
                                 audio_path=info['audio_path'])
    info = transcribe_audio_file(audio_path=info['audio_path'],
                                 json_data=info,
                                 chunk_length_ms=chunk_length_ms,
                                 chunk_length_diff=chunk_length_diff,
                                 renew=renew)
    info = analyze_video_text(video_path=video_path,
                       output_dir=output_dir,
                       json_data=info,
                       remove_phrases=remove_phrases)
    
    info = get_text_and_keywords(info,
                                 summarizer=summarizer,
                                 kw_model=kw_model)
    info = get_seo_data(info,
                        uploader=uploader,
                        domain=domain,
                        categories=categories,
                        video_url=video_url)
    safe_dump_to_file(data=info,
                      file_path=info['info_path'])
    return info

def get_info_data(video_path,
                  output_dir=None,
                  remove_phrases=None,
                  uploader=None,
                  domain=None,
                  categories=None,
                  video_url=None,
                  chunk_length_ms=None,
                  chunk_length_diff=None,
                  renew=None):
    remove_phrases = remove_phrases or []
    dirname = os.path.dirname(video_path)
    basename = os.path.basename(video_path)
    filename, ext = os.path.splitext(basename)
    video_directory = make_dirs(output_dir, filename)
    info_path = os.path.join(video_directory, 'info.json')
    video_text_path = os.path.join(video_directory, 'video_text.json')
    audio_path = os.path.join(video_directory, 'audio.wav')
    video_json_path = os.path.join(video_directory, 'video_json.json')
    categories = categories or {'ai': 'Technology', 'cannabis': 'Health', 'elon musk': 'Business'}
    uploader = uploader or 'The Daily Dialectics'
    domain = domain or 'https://thedailydialectics.com'
    video_url = video_url or url_join(domain,'videos')
    chunk_length_ms = if_none_get_def(chunk_length_ms, 50000)
    chunk_length_diff = if_none_get_def(chunk_length_diff, -5)
    renew = if_none_get_def(renew, False)
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
    info['categories'] = categories
    info['uploader'] = uploader
    info['domain'] = domain
    info['video_url'] = video_url
    info['chunk_length_ms'] = chunk_length_ms
    info['chunk_length_diff'] = chunk_length_diff
    info['renew'] = renew
    safe_dump_to_file(data=info, file_path=info['info_path'])
    return info

