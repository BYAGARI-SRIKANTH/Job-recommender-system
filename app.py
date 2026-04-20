import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai, extract_job_keywords, extract_resume_summary, extract_skill_gaps, extract_roadmap
from src.job_api import fetch_linkedin_jobs,fetch_naukri_jobs

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("AI Job Recommender System")
st.markdown("Upload your resume and get job recommendations based on your skills and experience from LinkedIn and Naukri")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)   
    with st.spinner("Summarizing your resume..."):
        summary = ask_openai(f"Summarize this resume highlighting the skills, education and experience: \n\n{resume_text}",max_tokens=5000)
        if any(term in summary.lower() for term in ["failed", "error", "no valid ai", "no openai", "no gemini"]):
            summary = extract_resume_summary(resume_text)
        
    with st.spinner("Finding skill gaps..."):
        gaps = ask_openai(f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities: \n\n{resume_text}", max_tokens=400)
        if any(term in gaps.lower() for term in ["failed", "error", "no valid ai", "no openai", "no gemini"]):
            gaps = extract_skill_gaps(resume_text)
        
    with st.spinner("Creating future roadmap..."):
        roadmap = ask_openai(f"Based on this resume suggest a future roadmap to improve this person's prospects (skills to learn, certifications needed, industry exposure): \n\n{resume_text}", max_tokens=400)
        if any(term in roadmap.lower() for term in ["failed", "error", "no valid ai", "no openai", "no gemini"]):
            roadmap = extract_roadmap(resume_text)
        
    # Display nicely formatted results
    st.markdown("---")
    st.header("Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; color:white;'>{roadmap}</div>",unsafe_allow_html=True)
    
    st.success("Analysis completed successfully!")
    
    linkedin_jobs = []
    naukri_jobs = []
    search_keywords = ""
    location_options = [
        "India",
        "Bengaluru",
        "Mumbai",
        "Delhi",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Kolkata",
        "Gurugram",
        "Noida",
        "Other",
    ]
    preferred_location = st.selectbox("Preferred job location", options=location_options, index=0)
    if preferred_location == "Other":
        preferred_location = st.text_input("Enter a custom location", value="India")

    if st.button("Get Job Recommendations"):
        with st.spinner("Extracting job search keywords from the resume summary..."):
            keywords = ask_openai(
                f"Based on this resume summary and the preferred location '{preferred_location}', suggest the best job titles and keywords to search for jobs. Give a comma-separated list only, no explanation.: \n\nSummary: {summary}",
                max_tokens=100
            )
            
            search_keywords = keywords.strip()

        if not search_keywords or any(term in search_keywords.lower() for term in ["failed", "error", "no valid ai", "no openai", "no gemini"]):
            st.warning("AI keyword extraction failed due to quota or API error. Using local fallback keywords.")
            fallback_keywords = extract_job_keywords(resume_text)
            if not fallback_keywords:
                fallback_keywords = extract_job_keywords(summary)
            search_keywords = fallback_keywords or search_keywords
            if fallback_keywords:
                st.info(f"Fallback keywords: {fallback_keywords}")
            else:
                st.error("Unable to extract fallback keywords from the resume. Please try again later or update your .env API keys.")

        if search_keywords:
            st.success(f"Extracting jobs keywords: {search_keywords}")
            with st.spinner("Fetching jobs from LinkedIn and Naukri..."):
                linkedin_jobs = fetch_linkedin_jobs(search_keywords, location=preferred_location, rows=60)
                naukri_jobs = fetch_naukri_jobs(search_keywords, location=preferred_location, rows=60)
            
    st.markdown("---")
    st.header("Top LinkedIn Jobs")
    
    if linkedin_jobs:
        for job in linkedin_jobs:
            job_link = job.get('link') or job.get('url') or job.get('jobUrl') or job.get('profileUrl') or ""
            st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
            st.markdown(f"-{job.get('location')}")
            if job_link:
                st.markdown(f"-[View job]({job_link})")
            else:
                st.caption("(Link not available)")
            st.markdown("---")
    else:
        st.warning("No LinkedIn jobs found.")
        
    st.markdown("---")
    st.header("Top Naukri Jobs")
    
    if naukri_jobs:
        for job in naukri_jobs:
            job_link = job.get('url') or job.get('link') or job.get('jobUrl') or job.get('jobLink') or ""
            st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
            st.markdown(f"-{job.get('location')}")
            if job_link:
                st.markdown(f"-[View Job]({job_link})")
            else:
                st.caption("(Link not available)")
    