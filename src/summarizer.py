from transformers import pipeline

summarizer = pipeline("summarization", model="google/flan-t5-base")


def chunk_text(text, max_words=250):

    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))

    return chunks


def generate_notes(text):

    chunks = chunk_text(text)

    notes = []

    for chunk in chunks:

        prompt = "Create clear bullet point study notes from this text:\n\n" + chunk

        summary = summarizer(
            prompt,
            max_length=200,
            min_length=80,
            do_sample=False
        )

        notes.append(summary[0]["summary_text"])

    return "\n\n".join(notes)


def detect_chapters(text):

    prompt = "Divide the following lecture into logical chapters with titles:\n\n" + text[:3000]

    result = summarizer(
        prompt,
        max_length=200,
        min_length=60,
        do_sample=False
    )

    return result[0]["summary_text"]


def generate_mindmap(text):

    prompt = "Extract the key concepts as a mind map list:\n\n" + text[:3000]

    result = summarizer(
        prompt,
        max_length=150,
        min_length=50,
        do_sample=False
    )

    return result[0]["summary_text"]