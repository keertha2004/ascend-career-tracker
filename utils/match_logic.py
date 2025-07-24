from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import fuzz
import re

# Load model
model = SentenceTransformer('all-mpnet-base-v2')

# Define relevant tech stack keywords
TECH_STACK_KEYWORDS = [
    'python', 'sql', 'r', 'machine learning', 'ml', 'classification', 'regression', 'clustering',
    'pandas', 'numpy', 'scikit-learn', 'nlp', 'llms', 'genai', 'aws', 'azure', 'cloud',
    'api', 'github', 'projects', 'technologies'
]

# Define weights
KEYWORD_WEIGHT = 0.6
SEMANTIC_WEIGHT = 0.4
SOFT_MATCH_THRESHOLD = 65
PARTIAL_MATCH_WEIGHT = 0.85


def clean_text(text):
    text = re.sub(r'[\n\r\t]+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower().strip()


def simple_sentence_split(text):
    return re.split(r'[.!?]\s+', text)


def compute_semantic_similarity(text1, text2):
    sents1 = [s for s in simple_sentence_split(text1) if s.strip()]
    sents2 = [s for s in simple_sentence_split(text2) if s.strip()]

    if not sents1 or not sents2:
        return 0.0

    emb_full_1 = model.encode(text1, convert_to_tensor=True)
    emb_full_2 = model.encode(text2, convert_to_tensor=True)
    full_score = util.pytorch_cos_sim(emb_full_1, emb_full_2).item() * 100

    emb1 = model.encode(sents1, convert_to_tensor=True)
    emb2 = model.encode(sents2, convert_to_tensor=True)
    sim_matrix = util.pytorch_cos_sim(emb1, emb2)

    max1 = sim_matrix.max(dim=1).values.mean().item()
    max2 = sim_matrix.max(dim=0).values.mean().item()
    sentence_score = ((max1 + max2) / 2) * 100

    final_score = 0.7 * full_score + 0.3 * sentence_score
    return round(final_score, 2)


def soft_keyword_match(text, keywords):
    text = clean_text(text)
    found = set()
    soft_found = set()

    for kw in keywords:
        if kw in text:
            found.add(kw)
        else:
            for word in text.split():
                if fuzz.partial_ratio(kw, word) >= SOFT_MATCH_THRESHOLD:
                    soft_found.add(kw)
                    break

    return found, soft_found


def is_meaningful(text):
    return len(text.split()) > 5


def calculate_match_score(resume_text, job_desc):
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_desc)

    if not clean_resume or not clean_jd or not is_meaningful(clean_resume):
        return 0.0, 0.0, 0.0, [], []

    # Semantic similarity
    sim_score = compute_semantic_similarity(resume_text, job_desc)

    # Keyword matching
    jd_keywords = set([kw.lower() for kw in TECH_STACK_KEYWORDS if kw.lower() in clean_jd])
    hard_matches, soft_matches = soft_keyword_match(clean_resume, jd_keywords)

    matched_keywords = hard_matches.union(soft_matches)
    missing_keywords = jd_keywords - matched_keywords

    hard_score = len(hard_matches)
    soft_score = PARTIAL_MATCH_WEIGHT * len(soft_matches)
    max_score = len(jd_keywords)
    keyword_score = ((hard_score + soft_score + 2) / (max_score + 2)) * 100 if max_score else 0.0

    final_score = (KEYWORD_WEIGHT * keyword_score) + (SEMANTIC_WEIGHT * sim_score)

    return (
        round(final_score, 2),
        round(sim_score, 2),
        round(keyword_score, 2),
        sorted(matched_keywords),
        sorted(missing_keywords)
    )
