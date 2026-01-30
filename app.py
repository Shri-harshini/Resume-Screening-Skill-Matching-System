import os
import streamlit as st
from pathlib import Path
from typing import List, Dict, Any, Optional
import tempfile
import base64
import json
import pandas as pd
import time

# Add the src directory to the Python path
import sys
sys.path.append(str(Path(__file__).parent))

from src.resume_parser import ResumeParser
from src.resume_matcher import ResumeMatcher

# Set page config
st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stFileUploader>div>div>div {
        border: 2px dashed #4CAF50;
        border-radius: 5px;
        padding: 2rem;
    }
    .stTextArea>div>div>textarea {
        min-height: 200px;
    }
    .match-score {
        font-size: 3rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin: 1rem 0;
    }
    .keyword-match {
        background-color: #e6f7e6;
        padding: 0.3rem 0.5rem;
        border-radius: 4px;
        margin: 0.2rem;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

class ResumeScreeningApp:
    def __init__(self):
        self.resume_matcher = ResumeMatcher()
        self.uploaded_resumes = []
        self.job_description = ""
        self.results = []
        
        # Create necessary directories
        self.UPLOAD_DIR = Path("uploads")
        self.UPLOAD_DIR.mkdir(exist_ok=True)
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """Save uploaded file to the uploads directory."""
        file_path = self.UPLOAD_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return str(file_path)
    
    def process_resumes(self, resume_files) -> List[Dict[str, Any]]:
        """Process multiple resume files and return parsed data."""
        results = []
        
        for file in resume_files:
            try:
                # Save the uploaded file
                file_path = self.save_uploaded_file(file)
                
                # Parse the resume
                parser = ResumeParser(file_path)
                resume_data = parser.parse()
                
                # Add file info
                resume_data['file_name'] = file.name
                resume_data['file_size'] = f"{file.size / 1024:.1f} KB"
                
                results.append(resume_data)
                
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                continue
                
        return results
    
    def analyze_resumes(self, resumes: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
        """Analyze resumes against the job description."""
        results = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, resume in enumerate(resumes):
            status_text.text(f"Analyzing resume {i+1} of {len(resumes)}: {resume['file_name']}")
            
            try:
                # Match resume to job description
                match_result = self.resume_matcher.match_resume_to_job(
                    resume['clean_text'], job_description
                )
                
                # Combine resume data with match results
                result = {
                    'file_name': resume['file_name'],
                    'score': match_result['score'],
                    'similarity_score': match_result['similarity_score'],
                    'keyword_coverage': match_result['keyword_coverage'],
                    'matched_keywords': match_result['matched_keywords'],
                    'total_keywords': match_result['total_keywords'],
                    'file_size': resume.get('file_size', 'N/A')
                }
                
                results.append(result)
                
            except Exception as e:
                st.error(f"Error analyzing {resume['file_name']}: {str(e)}")
                continue
                
            # Update progress
            progress_bar.progress((i + 1) / len(resumes))
        
        status_text.empty()
        progress_bar.empty()
        
        # Sort results by score in descending order
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
    
    def display_results(self, results: List[Dict[str, Any]]):
        """Display the analysis results in a tabular format."""
        if not results:
            st.warning("No results to display.")
            return
        
        # Convert results to DataFrame for display
        df = pd.DataFrame([{
            'Resume': r['file_name'],
            'Score': f"{r['score']:.1f}%",
            'Similarity': f"{r['similarity_score']:.1f}%",
            'Keyword Match': f"{len(r['matched_keywords'])}/{r['total_keywords']}",
            'File Size': r['file_size']
        } for r in results])
        
        # Display the table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Resume": st.column_config.TextColumn("Resume"),
                "Score": st.column_config.ProgressColumn(
                    "Match Score",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Similarity": st.column_config.ProgressColumn(
                    "Content Similarity",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Keyword Match": st.column_config.TextColumn("Keyword Match"),
                "File Size": st.column_config.TextColumn("File Size")
            }
        )
        
        # Show detailed view for selected resume
        st.subheader("Detailed Analysis")
        selected_resume = st.selectbox(
            "Select a resume to view detailed analysis:",
            [r['file_name'] for r in results],
            index=0
        )
        
        if selected_resume:
            selected = next((r for r in results if r['file_name'] == selected_resume), None)
            if selected:
                self.display_resume_details(selected)
    
    def display_resume_details(self, resume: Dict[str, Any]):
        """Display detailed analysis for a single resume."""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.metric("Overall Match Score", f"{resume['score']:.1f}%")
            st.metric("Content Similarity", f"{resume['similarity_score']:.1f}%")
            
        with col2:
            st.metric("Keyword Coverage", f"{resume['keyword_coverage']:.1f}%")
            st.metric("Matched Keywords", f"{len(resume['matched_keywords'])} / {resume['total_keywords']}")
        
        # Display matched keywords
        st.subheader("Matched Keywords")
        if resume['matched_keywords']:
            st.write(" ".join([f"`{kw}`" for kw in resume['matched_keywords']]))
        else:
            st.warning("No keywords matched.")
        
        # Display score distribution
        st.subheader("Score Distribution")
        score_data = {
            'Metric': ['Overall Score', 'Content Similarity', 'Keyword Coverage'],
            'Score': [resume['score'], resume['similarity_score'], resume['keyword_coverage']]
        }
        st.bar_chart(pd.DataFrame(score_data).set_index('Metric'))
    
    def run(self):
        """Run the Streamlit application."""
        st.title("📄 Resume Screening System")
        st.markdown("---")
        
        # Sidebar for job description
        with st.sidebar:
            st.header("Job Description")
            self.job_description = st.text_area(
                "Paste the job description here:",
                height=300,
                placeholder="Enter job title, required skills, qualifications, and experience..."
            )
            
            st.markdown("---")
            st.header("Upload Resumes")
            uploaded_files = st.file_uploader(
                "Upload resume files (PDF/DOCX):",
                type=["pdf", "docx"],
                accept_multiple_files=True
            )
            
            analyze_button = st.button("Analyze Resumes", type="primary", use_container_width=True)
        
        # Main content area
        if uploaded_files and self.job_description and analyze_button:
            with st.spinner("Processing resumes..."):
                # Process resumes
                self.uploaded_resumes = self.process_resumes(uploaded_files)
                
                if not self.uploaded_resumes:
                    st.error("No valid resumes were processed. Please check the file formats and try again.")
                    return
                
                # Analyze resumes against job description
                self.results = self.analyze_resumes(self.uploaded_resumes, self.job_description)
                
                # Display results
                st.success("Analysis complete!")
                self.display_results(self.results)
                
                # Add download button for results
                self.download_results()
        
        elif analyze_button and (not uploaded_files or not self.job_description):
            st.warning("Please upload resume files and enter a job description to analyze.")
        
        else:
            # Show instructions if no analysis has been performed
            self.show_instructions()
    
    def download_results(self):
        """Add a download button for the analysis results."""
        if not self.results:
            return
        
        # Convert results to CSV
        df = pd.DataFrame([{
            'Resume': r['file_name'],
            'Score': r['score'],
            'Similarity': r['similarity_score'],
            'Keyword_Coverage': r['keyword_coverage'],
            'Matched_Keywords': ", ".join(r['matched_keywords']),
            'Total_Keywords': r['total_keywords'],
            'File_Size': r['file_size']
        } for r in self.results])
        
        # Create download link
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="resume_analysis_results.csv">Download Full Results (CSV)</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    def show_instructions(self):
        """Show usage instructions."""
        st.info("""
            ### How to use this tool:
            1. **Enter a job description** in the sidebar
            2. **Upload resume files** (PDF or DOCX)
            3. Click **"Analyze Resumes"** to start the analysis
            
            The system will analyze each resume and provide:
            - Overall match score
            - Content similarity
            - Keyword coverage
            - Detailed analysis of each resume
            
            ---
            *Note: For best results, provide a detailed job description with specific skills and requirements.*
        """)

if __name__ == "__main__":
    app = ResumeScreeningApp()
    app.run()
