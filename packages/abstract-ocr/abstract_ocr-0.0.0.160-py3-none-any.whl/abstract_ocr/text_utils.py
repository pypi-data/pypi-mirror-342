from .functions import logger, create_key_value,cv2, pytesseract, os, shutil, spacy, json, re
from collections import Counter
from .ocr_utils import extract_text_from_image
from moviepy.editor import *
import numpy as np
nlp = spacy.load("en_core_web_sm")

def is_frame_analyzed(frame_file,video_text_data):
    for values in video_text_data:
        frame = values.get("frame")
        if frame_file == frame:
             return True
def determine_remove_text(text,remove_phrases=None):
    remove_phrases=remove_phrases or []
    found = False
    for remove_phrase in remove_phrases:
        if remove_phrase in text:
            found = True
            break
    if found == False:
        return text
def analyze_video_text(video_path,output_dir=None,video_text=None,remove_phrases=None):
    logger.info(f"analyze_video_text: {video_path}")
    remove_phrases=remove_phrases or []
    dirname = os.path.dirname(video_path)
    basename = os.path.basename(video_path)
    filename,ext = os.path.splitext(basename)
    video_text =video_text or []
    output_dir = output_dir or os.path.join(dirname,'./frames')
    os.makedirs(output_dir, exist_ok=True)

    # Load the video
    video = VideoFileClip(video_path)
    duration = video.duration

    # Extract frames every 1 second
    frame_interval = 1  # Adjust as needed
    for t in range(0, int(duration), frame_interval):
        
        frame_path = f"{output_dir}/{filename}_frame_{t}.jpg"
        if not os.path.isfile(frame_path):
            frame = video.get_frame(t)
            cv2.imwrite(frame_path, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))

    # Process all extracted frames
    for frame_file in os.listdir(output_dir):
        if frame_file.endswith(".jpg"):
            if is_frame_analyzed(frame_file,video_text) == False:
                
                image_dir = f"{output_dir}/{frame_file}"
                text = extract_text_from_image(image_dir)
                text = determine_remove_text(text,remove_phrases=remove_phrases)

                
                video_text.append({"frame": frame_file, "text": text})
                
    # Clean up (optional)
    return video_text

def extract_keywords_nlp(text, top_n=10):
    if not isinstance(text,str):
        logger.info(f"this is not a string: {text}")
    doc = nlp(str(text))
    word_counts = Counter(token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2)
    entity_counts = Counter(ent.text.lower() for ent in doc.ents if len(ent.text.split()) > 1)
    top_keywords = [word for word, _ in (word_counts + entity_counts).most_common(top_n)]
    return top_keywords
def calculate_keyword_density(text, keywords):
    words = text.lower().split()
    return {kw: (words.count(kw.lower()) / len(words)) * 100 for kw in keywords if len(words) > 0}
def get_text_and_keywords(json_data, summarizer=None, kw_model=None):
    # 1) Assemble full text

    full_text = json_data['whisper_result'].get('text')
    # 2) Keyword extraction (unchanged)
    json_data["keywords"] = extract_keywords_nlp(full_text, top_n=10)
    if kw_model:
        keybert = kw_model.extract_keywords(
            full_text,
            keyphrase_ngram_range=(1,3),
            stop_words="english",
            top_n=10,
            use_mmr=True,
            diversity=0.5
        )
        combined = list({kw for kw,_ in keybert} | set(json_data["keywords"]))[:10]
        json_data["combined_keywords"] = combined
        json_data["keyword_density"] = calculate_keyword_density(full_text, combined)

    # 3) Summarization with chunking + truncation
    json_data["summary"] = None
    if full_text and summarizer:
        # split into sentence-ish bits
        sentences = full_text.split(". ")
        chunks, buf = [], ""
        max_words = 300  # safe floor for ~512 tokens
        for sent in sentences:
            # +1 for the “. ” we removed
            if len((buf + sent).split()) <= max_words:
                buf += sent + ". "
            else:
                chunks.append(buf.strip())
                buf = sent + ". "
        if buf:
            chunks.append(buf.strip())

        summaries = []
        for idx, chunk in enumerate(chunks):
            try:
                out = summarizer(
                    chunk,
                    max_length=160,
                    min_length=40,
                    truncation=True  # >>> explicitly drop over‑long parts if still above model limit
                )
                summaries.append(out[0]["summary_text"])
            except Exception as e:
                logger.warning(f"Summarizer failed on chunk {idx}: {e}")
        # stitch back together
        json_data["summary"] = " ".join(summaries).strip()

    return json_data
