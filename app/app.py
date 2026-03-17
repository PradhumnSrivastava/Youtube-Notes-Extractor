import sys
import os
import streamlit as st
from reportlab.pdfgen import canvas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.transcript import get_transcript
from src.summarizer import generate_notes, detect_chapters, generate_mindmap
from src.utils import clean_text, translate_to_english


st.title("AI YouTube Notes Generator Using Transformers")

url = st.text_input("Enter YouTube Video URL")

if st.button("Generate Notes"):

    transcript_data = get_transcript(url)

    text = " ".join([i["text"] for i in transcript_data])

    text = clean_text(text)
    text = translate_to_english(text)

    with st.spinner("Generating Notes..."):
        notes = generate_notes(text)

    with st.spinner("Detecting Chapters..."):
        chapters = detect_chapters(text)

    with st.spinner("Creating Mind Map..."):
        mindmap = generate_mindmap(text)

    st.subheader("Notes")
    st.write(notes)

    st.subheader("Chapters")
    st.write(chapters)

    st.subheader("Mind Map")
    st.write(mindmap)

    st.subheader("Timestamp Transcript")

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