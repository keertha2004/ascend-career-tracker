import re
from sentence_transformers import SentenceTransformer
from fuzzywuzzy import fuzz

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def extract_section(resume_text, section_title, next_section_titles):
    pattern = rf"{section_title}[\s\S]*?(?=(" + "|".join(next_section_titles) + r")|$)"
    match = re.search(pattern, resume_text, re.IGNORECASE)
    return clean_text(match.group()) if match else ""

def extract_sections(resume_text):
    sections = {}
    headers = [
        "contact", "career summary", "skills", "projects", "education",
        "certifications", "languages"
    ]
    for i, header in enumerate(headers):
        next_headers = headers[i+1:]
        section_text = extract_section(resume_text, header, next_headers)
        sections[header.title()] = section_text
    return sections

def generate_career_summary(skills, education, projects):
    summary = []
    intro = "Detail-oriented and passionate B.Tech student"

    if "Artificial Intelligence" in education or "Data Science" in education:
        intro += " in Artificial Intelligence & Data Science"

    if "Reva" in education:
        intro += " from Reva University."
    summary.append(intro)

    tech_skills = []
    for skill in ['Python', 'C', 'Machine Learning', 'Web Technologies', 'HTML', 'CSS', 'Data Visualization', 'Predictive Analytics']:
        if skill.lower() in skills.lower():
            tech_skills.append(skill)
    if tech_skills:
        summary.append(f"Proficient in {', '.join(tech_skills)}.")

    if any(kw in projects.lower() for kw in ['health', 'grievance', 'finance']):
        summary.append("Keen interest in real-world AI applications, healthcare innovation, and data-driven solutions.")

    return summary

def bulletize(text):
    lines = [line.strip() for line in re.split(r'[\n\-•]', text) if line.strip()]
    return '\n• ' + '\n• '.join(lines)

def generate_improved_resume(resume_text, jd_text=None):
    resume_text = resume_text.lower()
    sections = extract_sections(resume_text)

    skills = sections.get("Skills", "")
    education = sections.get("Education", "")
    projects = sections.get("Projects", "")

    career_summary_lines = generate_career_summary(skills, education, projects)

    improved = "\n"
    improved += "Career Summary:\n"
    improved += "\n".join([f"• {line}" for line in career_summary_lines]) + "\n\n"
    improved += "────────────────────────────────────────────────────────────────────────────────\n"

    contact = sections.get("Contact", "").strip()
    if contact:
        improved += "Contact:\n" + bulletize(contact) + "\n\n"
        improved += "────────────────────────────────────────────────────────────────────────────────\n"

    if skills:
        improved += "Skills:" + bulletize(skills) + "\n\n"
        improved += "────────────────────────────────────────────────────────────────────────────────\n"

    if projects:
        improved += "Projects:\n"
        for proj in re.split(r"\n?•", projects):
            proj = proj.strip("- ").strip()
            if proj:
                lines = proj.split(". ")
                title = lines[0].strip()
                desc = ". ".join(lines[1:]).strip()
                improved += f"• **{title}**\n  {bulletize(desc)}\n\n"
        improved += "────────────────────────────────────────────────────────────────────────────────\n"

    if education:
        improved += "Education:" + bulletize(education) + "\n\n"
        improved += "────────────────────────────────────────────────────────────────────────────────\n"

    if sections.get("Certifications"):
        improved += "Certifications:" + bulletize(sections["Certifications"]) + "\n\n"
        improved += "────────────────────────────────────────────────────────────────────────────────\n"

    if sections.get("Languages"):
        improved += "Languages:" + bulletize(sections["Languages"]) + "\n\n"
        improved += "────────────────────────────────────────────────────────────────────────────────"

    return improved.strip()
