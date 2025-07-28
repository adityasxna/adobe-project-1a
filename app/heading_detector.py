import re
from collections import Counter

# --- Multilingual & Symbolic Patterns ---
HEADING_KEYWORDS = {
    'en': ['chapter', 'section', 'appendix', 'introduction', 'conclusion'],
    'hi': ['अध्याय', 'अनुभाग'],
    'es': ['capítulo', 'sección'],
    'de': ['kapitel', 'abschnitt'],
}
ALL_KEYWORDS_PATTERN = '|'.join([word for lang_words in HEADING_KEYWORDS.values() for word in lang_words])
NUMBERING_PATTERN = r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.|(\d+\.)+\d*|[A-Z]\.|\d+\)|[०-९]+\.?)'
JAPANESE_MARKER_PATTERN = r'^(【|「|第)'
SYMBOL_PATTERN = r'^[#●■]\s'

def get_heading_score(line, prev_line_y1, most_common_size):
    """
    Calculates a 'heading score' for a line of text based on advanced heuristics,
    including vertical spacing, styling, and multilingual patterns.
    """
    score = 0
    text = line['text']
    font_flags = line['flags']
    is_bold = font_flags & 2**4
    is_italic = font_flags & 2**1

    # 1. Vertical Spacing (very strong signal)
    space_above = line['bbox'][1] - prev_line_y1
    if space_above > 5:
        score += space_above / 5

    # 2. Font Size
    if line['size'] > most_common_size + 1:
        score += (line['size'] - most_common_size) * 1.5

    # 3. Font Style (Bold, Italic)
    if is_bold:
        score += 4
    if is_italic:
        score += 1

    # 4. Multilingual & Symbolic Patterns
    # Reward numbered headings in reports, but not simple lists
    if re.search(NUMBERING_PATTERN, text, re.IGNORECASE) and len(text.split()) > 2:
        score += 5
    if re.search(ALL_KEYWORDS_PATTERN, text.lower(), re.IGNORECASE):
        score += 6
    if re.search(JAPANESE_MARKER_PATTERN, text) or re.search(SYMBOL_PATTERN, text):
        score += 6
        
    # 5. Penalties for non-headings
    if re.search(r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text.lower()):
        score -= 10
    if re.fullmatch(r'\d+\.?', text): # Penalize simple numbered list items
        score -= 10
    if len(text.split()) < 2 and len(text) < 10 and not re.search(NUMBERING_PATTERN, text): # Penalize very short, non-numbered text
        score -= 2

    return score

def analyze_and_find_headings(lines):
    if not lines:
        return {"title": "", "outline": []}

    all_font_sizes = [line['size'] for line in lines if line['size']]
    if not all_font_sizes:
        return {"title": "", "outline": []}
    most_common_size = Counter(all_font_sizes).most_common(1)[0][0]

    # Score all lines
    scored_lines = []
    prev_y1 = 0
    for line in lines:
        score = get_heading_score(line, prev_y1, most_common_size)
        if score > 4: # Use a fine-tuned threshold
            line['score'] = score
            scored_lines.append(line)
        prev_y1 = line['bbox'][3]

    if not scored_lines:
        return {"title": "No headings identified", "outline": []}

    # Identify Title and Headings
    title = ""
    title_span = None
    page1_candidates = [l for l in scored_lines if l['page'] == 1]
    if page1_candidates:
        title_span = max(page1_candidates, key=lambda x: x['score'])
        title = title_span['text']

    heading_candidates = [l for l in scored_lines if l != title_span]
    
    # *** OPTIMIZED: Filter out duplicates (case-insensitive) ***
    unique_headings = []
    seen_text_lower = set()
    for h in heading_candidates:
        # Normalize text to lowercase for comparison
        text_lower = h['text'].lower()
        if text_lower not in seen_text_lower:
            unique_headings.append(h)
            seen_text_lower.add(text_lower)
    
    # Cluster and assign levels
    outline = []
    if not unique_headings:
        return {"title": title, "outline": []}

    unique_styles = sorted(list(set((line['size'], line['font']) for line in unique_headings)), key=lambda x: x[0], reverse=True)
    style_to_level = {style: f"H{i+1}" for i, style in enumerate(unique_styles[:3])}

    for line in unique_headings:
        style = (line['size'], line['font'])
        if style in style_to_level:
            outline.append({
                "level": style_to_level[style],
                "text": line["text"],
                "page": line["page"]
            })
    
    return {
        "title": title,
        "outline": sorted(outline, key=lambda x: (x['page'], lines.index(next(l for l in lines if l['text'] == x['text'] and l['page'] == x['page']))))
    }