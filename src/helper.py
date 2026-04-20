import fitz #pymupdf
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
from apify_client import ApifyClient

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

def load_dotenv_var(name, path):
    value = os.getenv(name)
    if value:
        return value
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, raw_value = line.split("=", 1)
            if key.strip() == name:
                return raw_value.strip()
    return None

GEMINI_API_KEY = load_dotenv_var("GEMINI_API_KEY", dotenv_path) or load_dotenv_var("GOOGLE_API_KEY", dotenv_path)
OPENAI_API_KEY = load_dotenv_var("OPENAI_API_KEY", dotenv_path)
APIFY_API_KEY = load_dotenv_var("APIFY_API_TOKEN", dotenv_path)

model = None
gemini_error = None
gemini_model_name = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        supported_models = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",
        ]
        for candidate in supported_models:
            try:
                model = genai.GenerativeModel(model_name=candidate)
                gemini_model_name = candidate
                break
            except Exception:
                continue
        if model is None:
            raise RuntimeError(
                f"Could not configure any supported Gemini model. Tried: {supported_models}"
            )
    except Exception as exc:
        gemini_error = str(exc)

client = None
openai_error = None
if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as exc:
        openai_error = str(exc)

if APIFY_API_KEY:
    apify_client = ApifyClient(APIFY_API_KEY)
else:
    apify_client = None

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file.
    
    Args:
        uploaded_file: The uploaded file object (PDF).
        
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_job_keywords(text, max_keywords=8):
    """Extract job search keywords from resume text without calling AI."""
    if not text:
        return ""

    text_lower = text.lower()
    candidates = [
        "data analyst",
        "business analyst",
        "data scientist",
        "data engineer",
        "sql",
        "python",
        "excel",
        "power bi",
        "tableau",
        "powerbi",
        "dax",
        "visualization",
        "data visualization",
        "analytics",
        "reporting",
        "dashboard",
        "sql server",
        "ms sql server",
        "api",
        "machine learning",
        "etl",
        "business intelligence",
        "report generation",
        "jupyter notebook",
        "git",
        "github",
        "data cleaning",
        "data modeling",
        "data analysis",
        "visualization",
    ]

    keywords = []
    for keyword in candidates:
        if keyword in text_lower and keyword not in keywords:
            keywords.append(keyword)
            if len(keywords) >= max_keywords:
                break

    skills_section = ""
    skills_match = re.search(r"skills?[:\-]\s*(.+?)(?:\n\n|\n[A-Z]|$)", text, flags=re.I | re.S)
    if skills_match:
        skills_section = skills_match.group(1)

    if skills_section:
        tokens = re.split(r"[;,\n]", skills_section)
        for token in tokens:
            candidate = token.strip()
            if not candidate:
                continue
            candidate_lower = candidate.lower()
            if len(candidate_lower) > 1 and candidate_lower not in keywords:
                keywords.append(candidate_lower)
                if len(keywords) >= max_keywords:
                    break

    if not keywords:
        tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#\-]+", text_lower)
        stop_words = {
            "the", "and", "for", "with", "from", "that", "this", "will",
            "which", "uses", "using", "skills", "experience", "projects",
            "resume", "data", "analysis", "analysis", "tools", "including",
        }
        counts = {}
        for token in tokens:
            if token in stop_words or len(token) < 3:
                continue
            counts[token] = counts.get(token, 0) + 1
        sorted_tokens = sorted(counts, key=lambda k: counts[k], reverse=True)
        for token in sorted_tokens:
            if token not in keywords:
                keywords.append(token)
                if len(keywords) >= max_keywords:
                    break

    return ", ".join(keywords[:max_keywords])


def extract_resume_summary(text):
    """Generate a basic resume summary by extracting key sections without AI."""
    if not text:
        return "No resume content available."
    
    summary_parts = []
    
    # Extract education
    edu_match = re.search(r"(education|qualification)s?[:\-]?\s*(.+?)(?:\n\n|\nexp|\nexperience|$)", text, re.I | re.S)
    if edu_match:
        edu_text = edu_match.group(2).strip()[:200]
        summary_parts.append(f"**Education:** {edu_text}")
    
    # Extract skills
    skills_match = re.search(r"skills?[:\-]?\s*(.+?)(?:\n\n|\nexp|\nexperience|$)", text, re.I | re.S)
    if skills_match:
        skills_text = skills_match.group(1).strip()[:200]
        summary_parts.append(f"**Key Skills:** {skills_text}")
    
    # Extract experience
    exp_match = re.search(r"(experience|work)s?[:\-]?\s*(.+?)(?:\n\n|$)", text, re.I | re.S)
    if exp_match:
        exp_text = exp_match.group(2).strip()[:200]
        summary_parts.append(f"**Experience:** {exp_text}")
    
    if not summary_parts:
        return text[:300]
    
    return "\n\n".join(summary_parts)


def extract_skill_gaps(text):
    """Identify missing skills and areas for improvement based on current skills."""
    if not text:
        return "Unable to analyze resume."
    
    text_lower = text.lower()
    
    common_advanced_skills = [
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", 
        "Spark", "Hadoop", "Scala", "R", "Statistics",
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "DevOps", "CI/CD", "Jenkins", "Git", "Terraform",
        "Agile", "Scrum", "Leadership", "Communication",
        "Advanced Excel", "VBA", "SAP", "Oracle",
        "Communication", "Project Management", "Data Visualization"
    ]
    
    gaps = []
    for skill in common_advanced_skills:
        if skill.lower() not in text_lower:
            gaps.append(skill)
    
    gap_text = ", ".join(gaps[:10])
    recommendations = [
        "- Consider certification programs in cloud platforms (AWS, Azure, GCP)",
        "- Improve advanced data visualization and storytelling skills",
        "- Develop leadership and project management capabilities",
        "- Learn containerization and DevOps tools (Docker, Kubernetes)",
        "- Strengthen statistical analysis and hypothesis testing knowledge"
    ]
    
    return f"**Missing Skills:** {gap_text}\n\n**Recommendations:**\n" + "\n".join(recommendations[:3])


def extract_roadmap(text):
    """Generate a career roadmap based on current skills and experience."""
    if not text:
        return "Unable to generate roadmap."
    
    text_lower = text.lower()
    roadmap = []
    
    if "data" in text_lower and "python" in text_lower:
        roadmap.append("**Phase 1 (3-6 months):** Master advanced Python libraries (Pandas, NumPy, scikit-learn) and SQL optimization")
        roadmap.append("**Phase 2 (6-12 months):** Learn cloud platforms (AWS/GCP) and implement machine learning pipelines")
        roadmap.append("**Phase 3 (1-2 years):** Develop expertise in big data tools (Spark) and advanced analytics")
    elif "python" in text_lower:
        roadmap.append("**Phase 1 (3-6 months):** Strengthen core Python and web development frameworks")
        roadmap.append("**Phase 2 (6-12 months):** Learn cloud deployment and DevOps practices")
        roadmap.append("**Phase 3 (1-2 years):** Build full-stack expertise and system design knowledge")
    else:
        roadmap.append("**Phase 1 (3-6 months):** Identify key technical skills from job market (Python, SQL, or relevant tools)")
        roadmap.append("**Phase 2 (6-12 months):** Complete online certifications and build portfolio projects")
        roadmap.append("**Phase 3 (1-2 years):** Transition to desired role through strategic job moves")
    
    if "leadership" not in text_lower:
        roadmap.append("**Soft Skills:** Develop communication, leadership, and stakeholder management")
    
    return "\n\n".join(roadmap)


def ask_openai(prompt, max_tokens=500):
    """
    Sends a prompt to Gemini first, then falls back to OpenAI if Gemini is unavailable.
    
    Args:
        prompt (str): The prompt to send to the AI service.
        max_tokens (int): Requested maximum number of output tokens.
        
    Returns:
        str: The generated text response, or an error message.
    """
    if model is not None:
        try:
            generation_config = genai.GenerationConfig(max_output_tokens=max_tokens)
            response = model.generate_content(
                prompt,
                generation_config=generation_config,
            )
            return getattr(response, "text", str(response))
        except Exception as exc:
            model_name = gemini_model_name or "unknown Gemini model"
            gemini_issue = f"Gemini ({model_name}) failed: {exc}"
            if client is None and OPENAI_API_KEY is None:
                return f"Error communicating with Gemini: {exc}. No OpenAI fallback configured."
            if client is not None:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5,
                        max_tokens=max_tokens,
                    )
                    return response.choices[0].message.content
                except Exception as openai_exc:
                    return f"{gemini_issue}; OpenAI fallback also failed: {openai_exc}"
            return gemini_issue

    if client is not None:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as exc:
            return f"OpenAI failed: {exc}"

    if gemini_error:
        return f"Gemini not configured properly: {gemini_error}"
    if openai_error:
        return f"OpenAI not configured properly: {openai_error}"
    return "Error: No valid AI API key configured. Set GEMINI_API_KEY or OPENAI_API_KEY in .env."



def fetch_linkedin_jobs(search_query, location = "india", rows=60):
    run_input = {
            "title": search_query,
            "location": location,
            "rows": rows,
            "proxy":{           
                "useApifyProxy": True,
                "apifyproxyGroups": ["RESIDENTIAL"],
            }
        }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_naukri_jobs(search_query, location = "india", rows=60):
    run_input = {
        "keyword": search_query,
        "maxJobs": rows,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs