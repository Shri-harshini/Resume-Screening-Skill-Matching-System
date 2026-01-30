import re
import numpy as np
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from typing import List, Dict, Tuple, Any
import os

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

class ResumeMatcher:
    """Match resumes with job descriptions using NLP and ML techniques."""
    
    def __init__(self, nlp_model: str = 'en_core_web_sm'):
        """Initialize the ResumeMatcher with a spaCy model.
        
        Args:
            nlp_model: Name of the spaCy model to use (default: 'en_core_web_sm')
        """
        try:
            self.nlp = spacy.load(nlp_model)
        except OSError:
            # If model is not found, download it
            os.system(f"python -m spacy download {nlp_model}")
            self.nlp = spacy.load(nlp_model)
            
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.punctuation = set(string.punctuation)
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess the input text by tokenizing, lemmatizing, and removing stopwords."""
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove punctuation and stopwords, and lemmatize
        processed_tokens = []
        for token in tokens:
            if token not in self.punctuation and token not in self.stop_words:
                lemma = self.lemmatizer.lemmatize(token)
                processed_tokens.append(lemma)
                
        return ' '.join(processed_tokens)
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """Extract top N keywords from the text using TF-IDF."""
        try:
            # Fit the vectorizer
            tfidf_matrix = self.vectorizer.fit_transform([text])
            
            # Get feature names (words)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores
            tfidf_scores = tfidf_matrix.toarray().flatten()
            
            # Sort by score in descending order
            sorted_indices = np.argsort(tfidf_scores)[::-1]
            
            # Get top N keywords
            top_keywords = [feature_names[i] for i in sorted_indices[:top_n] if tfidf_scores[i] > 0]
            
            return top_keywords
            
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate the cosine similarity between two texts."""
        try:
            # Preprocess both texts
            text1_processed = self.preprocess_text(text1)
            text2_processed = self.preprocess_text(text2)
            
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([text1_processed, text2_processed])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity
            
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def match_resume_to_job(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Match a resume to a job description and return a score and analysis."""
        try:
            # Calculate similarity score
            similarity_score = self.calculate_similarity(resume_text, job_description)
            
            # Extract keywords from job description
            job_keywords = self.extract_keywords(job_description)
            
            # Check for presence of job keywords in resume
            resume_tokens = set(self.preprocess_text(resume_text).split())
            matched_keywords = [kw for kw in job_keywords if kw in resume_tokens]
            
            # Calculate keyword coverage
            keyword_coverage = len(matched_keywords) / len(job_keywords) if job_keywords else 0
            
            # Calculate final score (weighted average of similarity and keyword coverage)
            final_score = (0.6 * similarity_score) + (0.4 * keyword_coverage)
            final_score = min(max(final_score, 0), 1)  # Ensure score is between 0 and 1
            
            return {
                'score': final_score * 100,  # Convert to percentage
                'similarity_score': similarity_score * 100,
                'keyword_coverage': keyword_coverage * 100,
                'matched_keywords': matched_keywords,
                'total_keywords': len(job_keywords)
            }
            
        except Exception as e:
            print(f"Error in resume-job matching: {str(e)}")
            return {
                'score': 0.0,
                'similarity_score': 0.0,
                'keyword_coverage': 0.0,
                'matched_keywords': [],
                'total_keywords': 0,
                'error': str(e)
            }
