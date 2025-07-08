from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_desc):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_desc])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(score[0][0] * 100, 2)  # Convert to %
