import sys
import os
import streamlit as st
from reportlab.pdfgen import canvas

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.transcript import get_transcript
from src.summarizer import generate_notes, detect_chapters, generate_mindmap
from src.utils import clean_text, translate_to_english


# ---------------------------------------------------------
# STREAMLIT PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI YouTube Notes Generator",
    layout="wide"
)

st.title("AI YouTube Notes Generator")

st.write(
    "Generate structured study notes, chapters, and concept maps "
    "from any YouTube lecture automatically."
)

url = st.text_input("Enter YouTube Video URL")


# ---------------------------------------------------------
# MAIN PROCESS
# ---------------------------------------------------------

if st.button("Generate Notes"):

    if not url:
        st.warning("Please enter a valid YouTube URL.")
        st.stop()

    # Step 1: Fetch transcript
    with st.spinner("Fetching transcript from YouTube..."):
        transcript_data = get_transcript(url)

    if not transcript_data:
        st.error("Transcript could not be fetched. Try another video.")
        st.stop()

    # Convert transcript segments into text
    text = " ".join([item["text"] for item in transcript_data])

    # Step 2: Clean text
    text = clean_text(text)

    # Step 3: Translate to English if necessary
    text = translate_to_english(text)

    # Step 4: Generate notes
    with st.spinner("Generating study notes..."):
        notes = generate_notes(text)

    # Step 5: Detect chapters
    with st.spinner("Detecting lecture chapters..."):
        chapters = detect_chapters(text)

    # Step 6: Generate mind map
    with st.spinner("Extracting key concepts..."):
        mindmap = generate_mindmap(text)

    # ---------------------------------------------------------
    # DISPLAY OUTPUT
    # ---------------------------------------------------------

    st.subheader("Generated Study Notes")
    st.write(notes)

    st.subheader("Lecture Chapters")
    st.write(chapters)

    st.subheader("Concept Mind Map")
    st.write(mindmap)

    # ---------------------------------------------------------
    # TRANSCRIPT PREVIEW
    # ---------------------------------------------------------

    st.subheader("Transcript Preview (with timestamps)")

    for seg in transcript_data[:20]:
        st.write(f"{seg['start']}s : {seg['text']}")

    # ---------------------------------------------------------
    # PDF GENERATION
    # ---------------------------------------------------------

    pdf_path = "youtube_notes.pdf"

    c = canvas.Canvas(pdf_path)

    text_obj = c.beginText(40, 800)
    text_obj.setFont("Helvetica", 10)

    for line in notes.split("\n"):

        if text_obj.getY() < 40:
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText(40, 800)
            text_obj.setFont("Helvetica", 10)

        text_obj.textLine(line)

    c.drawText(text_obj)
    c.save()

    # ---------------------------------------------------------
    # DOWNLOAD BUTTON
    # ---------------------------------------------------------

    with open(pdf_path, "rb") as file:

        st.download_button(
            label="Download Notes as PDF",
            data=file,
            file_name="youtube_notes.pdf",
            mime="application/pdf"
        )