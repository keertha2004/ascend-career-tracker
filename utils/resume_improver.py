import re

def generate_improved_resume(resume_text, job_desc):
    resume_text = resume_text.strip()
    job_desc = job_desc.strip()

    # === ✨ Replace Common Phrases with Professional Equivalents ===
    replacements = {
        r"\bgood at\b": "proficient in",
        r"\bworked on\b": "developed and implemented",
        r"\bhelped with\b": "contributed to",
        r"\bused\b": "leveraged",
        r"\bdid\b": "executed",
        r"\blearnt\b": "gained hands-on experience in",
        r"\bmade\b": "designed and built",
        r"\btrying to\b": "actively pursuing",
        r"\bpart of\b": "collaborated with",
        r"\bI\b": "",
        r"\bresponsible for\b": "accountable for",
        r"\bhandled\b": "managed",
        r"\bteam\b": "cross-functional team",
        r"\bproject\b": "solution",
        r"\btask\b": "objective",
        r"\bgood knowledge\b": "strong foundation",
        r"\bbasic understanding\b": "introductory knowledge of",
    }

    for pattern, replacement in replacements.items():
        resume_text = re.sub(pattern, replacement, resume_text, flags=re.IGNORECASE)

    # === 🔧 Upgrade Verb Usage in Bullet Points ===
    resume_text = upgrade_bullet_formatting(resume_text)

    # === 🎓 Add Career Summary if Not Present ===
    if "career objective" not in resume_text.lower() and "career summary" not in resume_text.lower():
        summary = f"""Career Summary:
Enthusiastic and dedicated AI/Data Science undergraduate with a passion for solving real-world problems through data. Skilled in Python, machine learning, and data visualization, with strong interest in roles like {extract_job_title(job_desc)}.
────────────────────────────────────────
"""
    else:
        summary = ""

    # === 📌 Highlight Missing JD Keywords ===
    extracted_keywords = extract_keywords(job_desc)
    missing = [kw for kw in extracted_keywords if kw.lower() not in resume_text.lower()]

    keyword_section = ""
    if missing:
        keyword_section += "\n────────────────────────────────────────\n"
        keyword_section += "📌 Keywords You Can Add (from Job Description):\n"
        keyword_section += "\n".join(f"• {kw}" for kw in set(missing))

    # === 🧹 Remove Redundancy & Clean Whitespace ===
    resume_text = re.sub(r'\n{3,}', '\n\n', resume_text)
    resume_text = remove_duplicate_lines(resume_text)

    # === 🏷️ Add Section Headers if Missing ===
    resume_text = add_missing_headers(resume_text)

    return summary + resume_text + keyword_section


# === 👀 Extract Role Title from JD
def extract_job_title(job_desc):
    match = re.search(r"(Data Scientist|ML Engineer|AI Engineer|Python Developer|.*Engineer|.*Scientist)", job_desc, re.IGNORECASE)
    return match.group(0) if match else "AI/ML Intern"

# === 🧠 Extract Skills from JD
def extract_keywords(text):
    keyword_list = [
        'Python', 'SQL', 'Machine Learning', 'AI', 'Statistical Analysis', 'Data Visualization',
        'Power BI', 'Pandas', 'NumPy', 'Matplotlib', 'Scikit-learn', 'TensorFlow',
        'Model Deployment', 'EDA', 'Data Cleaning', 'Recommendation Engine', 'Automation',
        'NLP', 'Data Preprocessing', 'Predictive Modeling', 'CrewAI', 'LangChain', 'OpenAI', 'Tkinter', 'GitHub'
    ]
    return [word for word in keyword_list if word.lower() in text.lower()]

# === 🔨 Upgrade Bullet Point Language
def upgrade_bullet_formatting(text):
    replacements = {
        r"(?i)\bbuilt\b": "Designed and developed",
        r"(?i)\bcreated\b": "Developed",
        r"(?i)\bworked with\b": "Collaborated with",
        r"(?i)\bparticipated in\b": "Contributed to",
        r"(?i)\bteam\b": "cross-functional team",
        r"(?i)\bsuccessfully\b": "",
        r"(?i)\bworked\b": "Engineered",
        r"(?i)\bdeveloped\b": "Implemented",
        r"(?i)\bhelped\b": "Assisted in delivering",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return text

# === 🔁 Remove Duplicate Lines
def remove_duplicate_lines(text):
    lines = text.split("\n")
    seen = set()
    new_lines = []
    for line in lines:
        cleaned = line.strip()
        if cleaned and cleaned not in seen:
            new_lines.append(cleaned)
            seen.add(cleaned)
    return "\n".join(new_lines)

# === 🧱 Add Headings if missing (basic heuristic)
def add_missing_headers(text):
    headings = {
        "Education": r"(B\.Tech|Bachelor|University|Degree|Education)",
        "Projects": r"(Project|Developed|Built|Tkinter|Churn|LangChain|Resume)",
        "Skills": r"(Python|SQL|Power BI|NumPy|Pandas|Tools|Matplotlib|Scikit|Git)",
        "Certifications": r"(Certificate|Certified|NPTEL|IBM|Hadoop)",
    }
    for heading, pattern in headings.items():
        if not re.search(rf"{heading}", text, re.IGNORECASE) and re.search(pattern, text, re.IGNORECASE):
            text += f"\n\n{heading}:\n"
    return text
