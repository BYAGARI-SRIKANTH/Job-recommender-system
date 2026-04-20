# AI Job Recommender System

A Streamlit-powered web application that recommends relevant jobs based on your resume and skills. Upload your PDF resume, get AI-powered analysis, and discover matching opportunities from LinkedIn and Naukri.

## Overview

Finding the right job can be overwhelming with thousands of listings across multiple platforms. This AI Job Recommender System simplifies the process by:

- Analyzing your resume using AI (OpenAI / Google Gemini)
- Extracting key skills and experience from your CV
- Fetching relevant job listings from LinkedIn and Naukri via Apify
- Displaying personalized job recommendations in a clean web interface

## Features

- Resume Parsing: Upload your resume as PDF and extract text automatically using PyMuPDF
- AI-Powered Analysis: Get a skills summary using OpenAI or Google Generative AI
- Job Matching: Fetch jobs from LinkedIn and Naukri based on extracted keywords
- Web Interface: Built with Streamlit for an intuitive user experience
- Environment Variables: Secure API key management using python-dotenv
- MCP Integration: Modular server architecture for extensibility

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI/LLM | OpenAI API, Google Generative AI |
| Resume Parsing | PyMuPDF (fitz) |
| Job APIs | Apify Client (LinkedIn & Naukri actors) |
| Environment | python-dotenv |
| Language | Python 3.x |

## Project Structure

```
Job-recommender-system/
├── app.py                 # Main Streamlit application
├── mcp_server.py          # MCP server component
├── inspect_genai.py       # GenAI inspection utility
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── src/
    ├── __init__.py        # Package initializer
    ├── helper.py          # Core helper functions (resume parsing, AI, job fetching)
    └── job_api.py         # Job API module with LinkedIn & Naukri fetchers
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BYAGARI-SRIKANTH/Job-recommender-system.git
   cd Job-recommender-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root with the following:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   APIFY_API_TOKEN=your_apify_api_token_here
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## How It Works

1. **Resume Upload**: The user uploads their resume as a PDF file
2. **Text Extraction**: PyMuPDF extracts text from the PDF
3. **AI Summarization**: OpenAI or Google Gemini analyzes the resume and extracts key skills
4. **Job Search**: Using Apify actors, the app fetches relevant job listings from LinkedIn and Naukri based on extracted keywords
5. **Results Display**: Matching jobs are displayed with title, company, location, and direct application links

## Requirements

- Python 3.8 or higher
- OpenAI API Key (for AI analysis)
- Google Generative AI API Key (alternative AI option)
- Apify API Token (for job fetching)

## Dependencies

```
streamlit
openai
pymupdf
python-dotenv
apify-client
```

## Future Improvements

- [ ] Add user authentication and saved preferences
- [ ] Implement skill-based filtering and scoring
- [ ] Add email notifications for new matching jobs
- [ ] Integrate more job platforms (Indeed, Glassdoor)
- [ ] Add a chatbot for career guidance
- [ ] Deploy on Streamlit Cloud for public access

## License

This project is open source and available under the MIT License.

## Author

**Byagari Srikanth**  
Aspiring AI/ML Developer | Data Science Enthusiast  
Hyderabad, Telangana, India

- GitHub: [BYAGARI-SRIKANTH](https://github.com/BYAGARI-SRIKANTH)
