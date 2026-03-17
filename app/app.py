# Import system modules
# These help us manage file paths and project structure
import sys
import os

# Import Streamlit for building the web application UI
import streamlit as st

# Import reportlab to generate downloadable PDF files
from reportlab.pdfgen import canvas


# Add the project root directory to Python path
# This allows us to import modules from the src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Import custom project modules
# These modules handle transcript extraction, summarization, and text processing
from src.transcript import get_transcript
from src.summarizer import generate_notes, detect_chapters, generate_mindmap
from src.utils import clean_text, translate_to_english


# ---------------------------------------------------------
# Streamlit UI Title
# ---------------------------------------------------------
# Displays the main title of the web application
st.title("AI YouTube Notes Generator")


# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------
# Create a text input box where the user can paste a YouTube URL
url = st.text_input("Enter YouTube Video URL")


# ---------------------------------------------------------
# Button Action
# ---------------------------------------------------------
# When the user clicks the "Generate Notes" button,
# the following pipeline will execute.
if st.button("Generate Notes"):


    # ---------------------------------------------------------
    # Step 1: Extract Transcript
    # ---------------------------------------------------------
    # Fetch subtitle segments from the YouTube video
    transcript_data = get_transcript(url)


    # Convert transcript segments into a single text string
    # Each segment contains {"text": "...", "start": timestamp}
    text = " ".join([i["text"] for i in transcript_data])


    # ---------------------------------------------------------
    # Step 2: Text Preprocessing
    # ---------------------------------------------------------
    # Clean punctuation, extra spaces, etc.
    text = clean_text(text)

    # Translate transcript into English if needed
    text = translate_to_english(text)


    # ---------------------------------------------------------
    # Step 3: Generate AI Notes
    # ---------------------------------------------------------
    # Use the AI summarization model to generate study notes
    with st.spinner("Generating Notes..."):
        notes = generate_notes(text)


    # ---------------------------------------------------------
    # Step 4: Detect Lecture Chapters
    # ---------------------------------------------------------
    # AI identifies logical sections of the lecture
    with st.spinner("Detecting Chapters..."):
        chapters = detect_chapters(text)


    # ---------------------------------------------------------
    # Step 5: Generate Mind Map
    # ---------------------------------------------------------
    # Extract key concepts and present them as a mind map
    with st.spinner("Creating Mind Map..."):
        mindmap = generate_mindmap(text)


    # ---------------------------------------------------------
    # Step 6: Display Results
    # ---------------------------------------------------------

    # Display generated notes
    st.subheader("📌 Notes")
    st.write(notes)

    # Display detected chapters
    st.subheader("📚 Chapters")
    st.write(chapters)

    # Display mind map
    st.subheader("🧠 Mind Map")
    st.write(mindmap)


    # ---------------------------------------------------------
    # Step 7: Display Transcript with Timestamps
    # ---------------------------------------------------------
    st.subheader("⏱ Timestamp Transcript")

    # Show first 20 transcript segments with timestamps
    for seg in transcript_data[:20]:
        st.write(f"{seg['start']}s : {seg['text']}")


    # ---------------------------------------------------------
    # Step 8: Generate PDF File
    # ---------------------------------------------------------

    # Define the PDF file name
    pdf_path = "notes.pdf"

    # Create a PDF canvas
    c = canvas.Canvas(pdf_path)

    # Start writing text at position (x=40, y=800)
    text_obj = c.beginText(40, 800)

    # Set font style and size
    text_obj.setFont("Helvetica", 10)

    # Write each line of notes into the PDF
    for line in notes.split("\n"):
        text_obj.textLine(line)

    # Draw the text object onto the PDF canvas
    c.drawText(text_obj)

    # Save the PDF file
    c.save()


    # ---------------------------------------------------------
    # Step 9: Provide Download Button
    # ---------------------------------------------------------

    # Open the generated PDF file in binary mode
    with open(pdf_path, "rb") as f:

        # Create a Streamlit download button
        st.download_button(
            "Download Notes PDF",
            f,
            file_name="youtube_notes.pdf"
        )