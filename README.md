# Resume Screening & Skill Matching System

The **Resume Screening & Skill Matching System** is an NLP-based application that automatically analyzes resumes and matches them against job descriptions. It extracts relevant skills, computes semantic similarity, and ranks candidates to support efficient and data-driven hiring decisions.

This project is intended for recruiters, HR teams, and developers interested in applying Natural Language Processing and Machine Learning to real-world recruitment workflows.

---

## Features

* Support for multiple resume formats, including PDF and DOCX
* Automated resume-to-job-description matching using NLP techniques
* Skill and keyword extraction from resumes and job descriptions
* Semantic similarity scoring and candidate ranking
* Clean and intuitive web interface built using Streamlit
* Generation of detailed analysis reports for review

---

## Tech Stack

* Python 3.8+
* Streamlit for the web interface
* NLP and ML libraries (TF-IDF, cosine similarity, sentence embeddings)
* Sentence Transformers for semantic similarity

---

## Getting Started

### Prerequisites

* Python 3.8 or higher
* pip (Python package manager)

### Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/resume-screening-system.git
cd resume-screening-system
```

Set up a virtual environment (recommended):

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the setup script to install required models and resources:

```bash
python setup.py
```

---

## Usage

Start the Streamlit application:

```bash
streamlit run app.py
```

Access the application in your browser at:

```
http://localhost:8501
```

---

## How It Works

1. Upload multiple resumes in PDF or DOCX format
2. Provide the target job description
3. Trigger analysis to process and compare resumes
4. Review ranked candidates with match scores and detailed insights

---

## Core Components

### Resume Parsing

* Extracts textual content from PDF and DOCX files
* Handles varied resume structures and layouts
* Cleans and preprocesses text for downstream analysis

### Text Analysis

* Tokenization, lemmatization, and stop-word removal
* Keyword extraction using TF-IDF
* Semantic similarity computation using sentence embeddings

### Matching and Scoring

* Cosine similarity-based content matching
* Keyword coverage analysis
* Overall match score computation
* Identification of matched and missing skills

---

## Project Structure

```
resume-screening-system/
├── app.py                
├── setup.py              
├── requirements.txt      
├── .env                  
├── uploads/              
├── data/                 
└── src/                  
    ├── __init__.py
    ├── resume_parser.py  
    └── resume_matcher.py # Matching and scoring algorithms
```
