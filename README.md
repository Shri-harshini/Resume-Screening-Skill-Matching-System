# Resume-Screening-Skill-Matching-System
Resume Screening &amp; Skill Matching System An NLP-based system that automatically analyzes resumes and matches candidates to job descriptions using Sentence Transformers. It extracts key skills, computes semantic similarity, and ranks candidates to streamline hiring decisions efficiently.

# 📄 Resume Screening System

An intelligent resume screening system that helps recruiters and hiring managers quickly filter and rank job applicants based on how well their resumes match a given job description. The system uses Natural Language Processing (NLP) and Machine Learning (ML) techniques to analyze and score resumes.

## ✨ Features

- **Multiple Format Support**: Parse resumes in PDF and DOCX formats
- **Intelligent Matching**: Advanced NLP techniques to match resumes with job descriptions
- **Keyword Analysis**: Identify and highlight relevant skills and qualifications
- **Scoring System**: Comprehensive scoring based on content similarity and keyword coverage
- **User-Friendly Interface**: Clean and intuitive web interface built with Streamlit
- **Detailed Reports**: View and download detailed analysis reports

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/resume-screening-system.git
   cd resume-screening-system
   ```

2. **Set up a virtual environment (recommended)**:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the setup script** (this will install required models and data):
   ```bash
   python setup.py
   ```

### Running the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Then open your web browser and navigate to:
```
http://localhost:8501
```

## 🛠️ How It Works

1. **Upload Resumes**: Upload multiple resumes in PDF or DOCX format
2. **Enter Job Description**: Paste the job description you're hiring for
3. **Analyze**: Click "Analyze Resumes" to process the applications
4. **Review Results**: View ranked results with match scores and detailed analysis

## 📊 Features in Detail

### Resume Parsing
- Extracts text from PDF and DOCX files
- Handles various resume formats and layouts
- Cleans and preprocesses text for analysis

### Text Analysis
- Tokenization and lemmatization
- Stop word removal
- Keyword extraction using TF-IDF
- Semantic similarity scoring

### Matching Algorithm
- Calculates content similarity using cosine similarity
- Analyzes keyword coverage
- Provides an overall match score
- Identifies matched and missing keywords

## 📁 Project Structure

```
resume-screening-system/
├── app.py                # Main Streamlit application
├── setup.py              # Setup script for environment
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── uploads/              # Directory for uploaded resumes
├── data/                 # Directory for storing data
└── src/                  # Source code
    ├── __init__.py
    ├── resume_parser.py  # Resume parsing functionality
    └── resume_matcher.py # Resume matching algorithms
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using Python, Streamlit, spaCy, and scikit-learn
- Inspired by the need for efficient resume screening in recruitment processes
