import sys
import os
import streamlit as st
from reportlab.pdfgen import canvas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.transcript import get_transcript
from src.summarizer import generate_notes, detect_chapters, generate_mindmap
from src.utils import clean_text, translate_to_english


st.title("AI YouTube Notes Generator")

url = st.text_input("Enter YouTube Video URL")

if st.button("Generate Notes"):

    if not url:
        st.warning("Please enter a YouTube URL.")
        st.stop()

    # Step 1: Fetch transcript
    transcript_data = get_transcript(url)

    if not transcript_data:
        st.error("⚠ Could not fetch transcript. Try another video.")
        st.stop()

    # Convert transcript to plain text
    text = " ".join([i["text"] for i in transcript_data])

    # Text preprocessing
    text = clean_text(text)
    text = translate_to_english(text)

    # Generate notes
    with st.spinner("Generating Notes..."):
        notes = generate_notes(text)

    # Detect chapters
    with st.spinner("Detecting Chapters..."):
        chapters = detect_chapters(text)

    # Generate mind map
    with st.spinner("Creating Mind Map..."):
        mindmap = generate_mindmap(text)

    st.subheader("📌 Notes")
    st.write(notes)

    st.subheader("📚 Chapters")
    st.write(chapters)

    st.subheader("🧠 Mind Map")
    st.write(mindmap)

    st.subheader("⏱ Timestamp Transcript")

    for seg in transcript_data[:20]:
        st.write(f"{seg['start']}s : {seg['text']}")

    # PDF generation
    pdf_path = "notes.pdf"

    c = canvas.Canvas(pdf_path)

    text_obj = c.beginText(40, 800)
    text_obj.setFont("Helvetica", 10)

    for line in notes.split("\n"):
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.save()

    with open(pdf_path, "rb") as f:

        st.download_button(
            "Download Notes PDF",
            f,
            file_name="youtube_notes.pdf"
        )