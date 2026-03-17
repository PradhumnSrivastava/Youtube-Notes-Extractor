# Import the HuggingFace pipeline utility
# Pipeline provides an easy interface to use pretrained NLP models
from transformers import pipeline


# Load a pretrained summarization model
# We use Google's FLAN-T5 model which is good for instruction-based text tasks
summarizer = pipeline("summarization", model="google/flan-t5-base")


# ---------------------------------------------------------
# FUNCTION: chunk_text
# ---------------------------------------------------------
# This function splits long text into smaller chunks of words.
# Transformer models have input size limits, so we break the
# transcript into manageable pieces before sending them to the model.

def chunk_text(text, max_words=250):

    # Convert the text into a list of words
    words = text.split()

    # This list will store all the smaller text chunks
    chunks = []

    # Iterate through the word list in steps of max_words
    # Example: 0–250, 250–500, 500–750 ...
    for i in range(0, len(words), max_words):

        # Extract a slice of words and convert them back into a sentence
        # " ".join() merges the list of words into a single string
        chunks.append(" ".join(words[i:i + max_words]))

    # Return the list containing all text chunks
    return chunks


# ---------------------------------------------------------
# FUNCTION: generate_notes
# ---------------------------------------------------------
# This function generates study notes from the transcript.
# Each chunk is summarized separately and then all summaries
# are combined into the final notes output.

def generate_notes(text):

    # Split the long transcript into smaller chunks
    chunks = chunk_text(text)

    # List to store the generated notes
    notes = []

    # Process each chunk one by one
    for chunk in chunks:

        # Create a prompt to instruct the AI model
        # Prompt engineering helps guide the model output
        prompt = "Create clear bullet point study notes from this text:\n\n" + chunk

        # Send the prompt to the summarization model
        summary = summarizer(
            prompt,
            max_length=200,   # Maximum number of tokens in the summary
            min_length=80,    # Minimum length of the summary
            do_sample=False   # Disable randomness for consistent results
        )

        # The model returns a list of dictionaries
        # Example: [{'summary_text': 'Generated notes here'}]

        # Extract the actual summary text and add it to the notes list
        notes.append(summary[0]["summary_text"])

    # Combine all chunk summaries into a single text
    return "\n\n".join(notes)


# ---------------------------------------------------------
# FUNCTION: detect_chapters
# ---------------------------------------------------------
# This function uses the AI model to divide the lecture
# transcript into logical chapters with titles.

def detect_chapters(text):

    # Only the first 3000 characters are used to avoid model input limits
    prompt = "Divide the following lecture into logical chapters with titles:\n\n" + text[:3000]

    # Generate chapter suggestions using the summarization model
    result = summarizer(
        prompt,
        max_length=200,
        min_length=60,
        do_sample=False
    )

    # Extract and return the chapter structure text
    return result[0]["summary_text"]


# ---------------------------------------------------------
# FUNCTION: generate_mindmap
# ---------------------------------------------------------
# This function extracts the key ideas or concepts from the
# transcript and returns them in a mind-map style list.

def generate_mindmap(text):

    # Provide an instruction prompt to the AI model
    prompt = "Extract the key concepts as a mind map list:\n\n" + text[:3000]

    # Generate the key concept list using the model
    result = summarizer(
        prompt,
        max_length=150,
        min_length=50,
        do_sample=False
    )

    # Return the generated mind map text
    return result[0]["summary_text"]