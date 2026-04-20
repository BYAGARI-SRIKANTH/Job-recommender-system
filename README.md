# Job Recommender System

An AI-powered job recommendation system that analyzes your resume and recommends relevant jobs from LinkedIn and Naukri.

## Features

- 📄 **Resume Analysis**: Upload PDF resumes and get AI-powered analysis
- 🎯 **Resume Summary**: Highlights skills, education, and experience
- 🔍 **Skill Gap Analysis**: Identifies missing skills and certifications
- 🛣️ **Career Roadmap**: Personalized future roadmap for career growth
- 💼 **Job Recommendations**: Fetches relevant jobs from LinkedIn and Naukri

## Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: OpenAI GPT
- **Web Scraping**: Apify
- **PDF Processing**: PyMuPDF
- **Python**: 3.11+

## Prerequisites

- Python 3.11+
- OpenAI API Key
- Apify API Token

## Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BYAGARI-SRIKANTH/Job-recommender-system.git
   cd Job-recommender-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The app will be available at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your repository (`Job-recommender-system`)
5. Set main file: `app.py`
6. Click "Deploy"
7. Add secrets in app settings:
   - `OPENAI_API_KEY`
   - `APIFY_API_TOKEN`

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Windows: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY="your-key"
   heroku config:set APIFY_API_TOKEN="your-token"
   git push heroku master
   ```

### Option 3: Docker + Cloud Run (Google Cloud)

1. **Build and test locally**
   ```bash
   docker build -t job-recommender .
   docker run -p 8501:8501 job-recommender
   ```

2. **Push to Google Cloud Run**
   ```bash
   gcloud run deploy job-recommender --source .
   ```

### Option 4: Docker + Other Cloud Providers

- **AWS**: ECS, Fargate, or App Runner
- **Azure**: Container Instances or App Service
- **DigitalOcean**: App Platform or App Runner

## Project Structure

```
job-recommender-mcp/
├── app.py                 # Main Streamlit application
├── mcp_server.py         # MCP server implementation
├── inspect_genai.py      # AI inspection utilities
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── Procfile             # Heroku configuration
├── setup.sh             # Streamlit setup script
├── .env.example         # Environment variables template
├── README.md            # This file
└── src/
    ├── __init__.py
    ├── helper.py        # Helper functions for PDF/AI processing
    ├── job_api.py       # Job fetching APIs (LinkedIn, Naukri)
```

## API Keys Required

1. **OpenAI API Key**
   - Get from: https://platform.openai.com/api-keys
   - Required for: Resume analysis, skill gap analysis, roadmap generation

2. **Apify API Token**
   - Get from: https://apify.com/
   - Required for: Web scraping job listings

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
APIFY_API_TOKEN=your_apify_api_token_here
```

## Usage

1. Upload your resume (PDF format)
2. Wait for the AI analysis to complete
3. Review:
   - Resume summary
   - Skill gaps
   - Career roadmap
   - Job recommendations

## Troubleshooting

- **"No valid AI provider"**: Check your OpenAI API key
- **"No jobs found"**: Check your Apify API token and internet connection
- **PDF parsing errors**: Ensure your PDF is not corrupted and is in a standard format

## Future Enhancements

- [ ] Multi-language support
- [ ] Interview preparation guides
- [ ] Salary predictions
- [ ] LinkedIn profile optimization tips
- [ ] Email notifications for matching jobs

## License

This project is open source and available under the MIT License.

## Contact

For questions or issues, please contact: [Your Email]
