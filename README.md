# AI YouTube Notes Generator – Project Summary

## Overview

The AI YouTube Notes Generator is an NLP-based application that converts YouTube lecture videos into structured study material. It extracts the transcript, processes the text, and uses a pretrained transformer model (FLAN-T5) to generate notes, chapters, and key concepts.


## Working Pipeline

1. **User Input**
   The user enters a YouTube video URL through a Streamlit interface.

2. **Transcript Extraction**
   The system extracts the video ID and fetches the transcript using the YouTube Transcript API. The transcript is stored as text with timestamps.

3. **Text Preprocessing**
   The transcript is cleaned by removing punctuation, extra spaces, and converting it to lowercase to improve model performance.

4. **Translation**
   If the transcript is not in English, it is translated into English using a translation API.

5. **Chunking**
   Since transformer models have input size limits, the text is divided into smaller chunks (around 250 words each).

6. **Notes Generation (Core Logic)**
   Each chunk is passed to a pretrained FLAN-T5 model with a prompt like:
   *"Create clear bullet point study notes from this text"*
   The summaries from all chunks are combined to form final notes.

7. **Chapter Detection**
   The model is prompted to divide the lecture into logical sections with titles.

8. **Mind Map Generation**
   The model extracts key concepts and presents them in a structured format.

9. **Output & Export**
   The results (notes, chapters, mind map) are displayed using Streamlit, and notes can be downloaded as a PDF.


## Tools Used

* Python
* Streamlit (UI)
* Hugging Face Transformers (FLAN-T5)
* YouTube Transcript API
* deep_translator (Google Translator)
* ReportLab (PDF generation)


## Key Highlights

* Uses pretrained LLM (no training required)
* Handles long text using chunking
* Applies prompt engineering for structured outputs
* End-to-end pipeline from video to notes


This project converts YouTube lectures into structured notes by extracting transcripts and processing them through a pretrained transformer model using prompt-based summarization.
