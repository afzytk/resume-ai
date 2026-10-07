import re

ROLE_SKILLS = {
    "frontend developer": [
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "next.js",
        "tailwind css",
        "git",
    ],
    "backend developer": [
        "python",
        "fastapi",
        "django",
        "node.js",
        "express.js",
        "rest api",
        "postgresql",
        "git",
    ],
}

#check skill
def detect_skills(resume_text:str,job_role:str):
    normalised_text = resume_text.lower()
    normalised_job_role = job_role.lower()
    skills = ROLE_SKILLS[normalised_job_role]
    detected_skills = []
    missing_skills = []

    for skill in skills:
        if skill in normalised_text:
            detected_skills.append(skill)
        else:
            missing_skills.append(skill)

    return detected_skills, missing_skills




#skill score
def calculate_skill_score(detected_skills, job_role):
    detected_skills_count = len(detected_skills)

    normalized_job_role = job_role.lower()
    expected_skills_score = len(ROLE_SKILLS[normalized_job_role])

    final_score = (detected_skills_count / expected_skills_score) * 40

    return final_score



ROLE_KEYWORDS = {
    "frontend developer": [
        "responsive",
        "api",
        "rest",
        "git",
        "component",
        "accessibility",
        "performance",
    ],
}

#check keywords
def match_keywords(resume_text: str, job_role: str):
    normalised_text = resume_text.lower()
    normalised_job_role = job_role.lower()

    keywords = ROLE_KEYWORDS[normalised_job_role]

    matched_keywords = []
    missing_keywords = []

    for keyword in keywords:
        if keyword in normalised_text:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    return matched_keywords, missing_keywords



#keyword score
def calculate_keyword_score(matched_keywords, job_role):
    normalised_job_role = job_role.lower()
    keyword_score = (len(matched_keywords)/len(ROLE_KEYWORDS[normalised_job_role])*25)
    return keyword_score

#check resume section
def resume_section(resume_text: str):
    normalised_resume_text = resume_text.lower()
    sections = ["contact information","skills","projects", "education","experience"]
    section_status = {}
    for section in sections:
        if section in normalised_resume_text:
            section_status[section] = True
        else:
            section_status[section]  = False
    return section_status

#section score
def calculate_section_score(section_status):
    detected_sections = sum(section_status.values())
    total_sections = len(section_status)

    section_score = (detected_sections / total_sections) * 20

    return section_score


#check content quality
def analyze_content_quality(resume_text: str):
    normalized_text = resume_text.lower()

    action_verbs = [
        "built",
        "developed",
        "designed",
        "implemented",
        "integrated",
        "optimized",
        "architected",
        "created",
        "deployed",
    ]

    found_action_verbs = []

    for verb in action_verbs:
        if verb in normalized_text:
            found_action_verbs.append(verb)
    has_metrics = bool(re.search(r"\d+%|\d+x|\d+", normalized_text))

    return {
        "action_verbs": found_action_verbs,
         "has_metrics": has_metrics
    }

#content score
def calculate_content_score(content_quality):
    score = 0

    action_verbs = content_quality["action_verbs"]
    has_metrics = content_quality["has_metrics"]

    if len(action_verbs) >= 3:
        score += 8
    elif len(action_verbs) > 0:
        score += 4

    if has_metrics:
        score += 7

    return score

def analyze_resume(resume_text: str, job_role: str):
    detected_skills, missing_skills = detect_skills(
        resume_text,
        job_role
    )

    skill_score = calculate_skill_score(
        detected_skills,
        job_role
    )

    matched_keywords, missing_keywords = match_keywords(
        resume_text,
        job_role
    )

    keyword_score = calculate_keyword_score(
        matched_keywords,
        job_role
    )

    sections = resume_section(resume_text)

    section_score = calculate_section_score(
        sections
    )

    content_quality = analyze_content_quality(
        resume_text
    )

    content_score = calculate_content_score(
        content_quality
    )

    suggestions = generate_suggestions(
    missing_skills,
    missing_keywords,
    sections,
    content_quality
)

    total_score = (
        skill_score
        + keyword_score
        + section_score
        + content_score
    )

    return {
        "ats_score": round(total_score),
        "skill_score": skill_score,
        "keyword_score": keyword_score,
        "section_score": section_score,
        "content_score": content_score,
        "skills_detected": detected_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "sections": sections,
        "content_quality": content_quality,
        "suggestions": suggestions,
    }


#provide suggestions
def generate_suggestions(
    missing_skills,
    missing_keywords,
    sections,
    content_quality
):
    suggestions = []

    if missing_skills:
        suggestions.append(
            f"Consider adding these skills if you have experience with them: "
            f"{', '.join(missing_skills)}."
        )

    if missing_keywords:
        suggestions.append(
            f"Consider including relevant keywords such as: "
            f"{', '.join(missing_keywords)}."
        )

    missing_sections = [
        section
        for section, present in sections.items()
        if not present
    ]

    if missing_sections:
        suggestions.append(
            f"Consider adding these resume sections: "
            f"{', '.join(missing_sections)}."
        )

    if len(content_quality["action_verbs"]) < 3:
        suggestions.append(
            "Use more strong action verbs to describe your project "
            "and work experience."
        )

    if not content_quality["has_metrics"]:
        suggestions.append(
            "Add measurable results such as percentages, time saved, "
            "performance improvements, or number of users."
        )

    return suggestions